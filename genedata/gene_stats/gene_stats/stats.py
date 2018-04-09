import csv, json, decimal

import pandas as pd
import boto3
from botocore.exceptions import ClientError
from cassandra.cluster import Cluster
from cassandra.query import PreparedStatement, BatchStatement

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'config')))
try:
    from config import config
except:
    import config

def connect():
    cluster = Cluster(port=config.get_setting('cassandra','port'))
    session = cluster.connect()
    result = session.execute('SELECT cluster_name, listen_address FROM system.local;')
    session.execute("CREATE KEYSPACE IF NOT EXISTS genes WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};")
    session.execute("USE genes;")
    session.execute("CREATE TABLE IF NOT EXISTS gene_stats (id int, d int, p varchar, v double, primary key ((id, d), p));")

    session.execute("""
        CREATE OR REPLACE FUNCTION sd_state(state tuple<int, double, double>, current double)
        CALLED ON NULL INPUT
        RETURNS tuple<int, double, double>
        LANGUAGE java
        AS '
            int n = state.getInt(0);
    	    double mean = state.getDouble(1);
            double m2 = state.getDouble(2);

            n++;
            double delta = current - mean;
            mean += delta / n;
            m2 += delta * (current - mean);

            // Update the state
            state.setInt(0, n);
            state.setDouble(1, mean);
            state.setDouble(2, m2);

            return state;'
    """)
    session.execute("""
        CREATE OR REPLACE FUNCTION sd_final (state tuple<int,double,double>)
        CALLED ON NULL INPUT
        RETURNS double
        LANGUAGE java
        AS '
            int n = state.getInt(0);
            double m2 = state.getDouble(2);
            if (n < 1) return null;
            return Math.sqrt(m2 / (n - 1));
        '
    """)

    session.execute("""
        CREATE AGGREGATE IF NOT EXISTS stdev (double)
        SFUNC sd_state
        STYPE tuple<int,double,double>
        FINALFUNC sd_final INITCOND (0,0,0);
    """)

    return session

def populate():
    session = connect()
    df = pd.read_csv('../../../data/ROSMAP_RNASeq_entrez.csv')

    query = "INSERT INTO gene_stats (id, d, p, v) VALUES ({}, {}, '{}', {});"
    genes = list(df)[2:]
    diagnoses = df['DIAGNOSIS'].unique()[1:]
    for diagnosis in diagnoses:
        diag_genes = df[df['DIAGNOSIS'] == diagnosis]
        for gene in genes:
            filtered = diag_genes[gene]
            patients = diag_genes['PATIENT_ID']
            filtered = filtered.dropna()
            batch = BatchStatement()
            for val in filtered.iteritems():
                batch.add(query.format(int(gene), int(diagnosis), patients[val[0]], val[1]))
            session.execute(batch)

def query(entrez_id):
    session = connect()
    results = []
    for i in xrange(6):
        query = 'SELECT AVG(v), STDEV(v) FROM gene_stats WHERE id = {} AND d = {}'.format(entrez_id, i+1)
        result = session.execute(query)
        for row in result:
            results.append((row.system_avg_v, row.genes_stdev_v))
    return results
