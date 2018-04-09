import csv, json, decimal, os
import boto3
import xml.etree.ElementTree as ET
ET.register_namespace('', "http://uniprot.org/uniprot")

def connect():
  conn = None
  cur = None
  try:
    conn = psycopg2.connect(host="localhost", database="gene_info", user="bhernandev", password="password123")
    cur = conn.cursor()
  except(Exception, psycopg2.DatabaseError) as error:
    print error

  return cur, conn


def create_tables():
  cur, conn = connect()
  try:
    cur.execute("""
      CREATE TABLE IF NOT EXISTS genesymbol(
        entrez_id INTEGER PRIMARY KEY,
        gene_symbol TEXT,
        gene_name TEXT
      )
      """)
    cur.execute("""
      CREATE TABLE IF NOT EXISTS uniprot(
        entrez_id INTEGER,
        uniprot_id TEXT PRIMARY KEY
      )
      """)
    cur.execute("""
      CREATE TABLE IF NOT EXISTS uniprot_xml(
        uniprot_id TEXT PRIMARY KEY,
        gene_xml TEXT
      )
      """)
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print error

def insert_data():
  cur, conn = connect()

  #genesymbol
  csv_reader = None
  gene_rows = []
  with open("../../../data/entrez_ids_genesymbol.csv") as genesymbol_file:
    genesymbol_file.readline()
    csv_reader = csv.reader(genesymbol_file)
    for row in csv_reader:
      temp_row = (int(row[0]), row[1], row[2])
      gene_rows.append(temp_row)
  insertion_sql = "INSERT INTO genesymbol(entrez_id, gene_symbol, gene_name) VALUES(%s, %s, %s)"
  cur.executemany(insertion_sql, gene_rows)
  conn.commit()
  print "genesymbol committed"

  #uniprot
  uniprot_rows = []
  with open("../../../data/entrez_ids_uniprot.txt") as uniprot_file:
    uniprot_file.readline()
    line = uniprot_file.readline()
    while line:
      row = line.split()
      temp_row = (int(row[0]), row[1])
      uniprot_rows.append(temp_row)
      line = uniprot_file.readline()
  insertion_sql = "INSERT INTO uniprot(entrez_id, uniprot_id) VALUES(%s, %s)"
  cur.executemany(insertion_sql, uniprot_rows)
  conn.commit()
  print "uniprot committed"

  #uniprot_xml
  insertion_sql = "INSERT INTO uniprot_xml(uniprot_id, gene_xml) VALUES(%s, %s)"
  xml_rows = []
  count = 0
  tree = ET.iterparse('../../../data/uniprot-human.xml')
  tree = iter(tree)
  for event, elem in tree:
    if count == 1000:
      cur.executemany(insertion_sql, xml_rows)
      conn.commit()
      print "uniprot_xml committed partially"
      count = 0
      xml_rows = []
    if elem.tag == '{http://uniprot.org/uniprot}entry':
      temp_xml = ET.tostring(elem)
      names = elem.iterfind('{http://uniprot.org/uniprot}name')
      for name in names:
        uniprot_id = name.text
        temp_xml_string = temp_xml.decode("utf-8")
        temp_xml_string = temp_xml_string.replace('\n', '')
        temp_row = (uniprot_id, temp_xml_string)
        xml_rows.append(temp_row)
        count = count + 1

  cur.executemany(insertion_sql, xml_rows)
  conn.commit()
  print "uniprot_xml committed"

def query_gene(entrez_id):
  query_results = []
  cur, conn = connect()
  cur.execute("SELECT genesymbol.entrez_id, genesymbol.gene_symbol, genesymbol.gene_name, uniprot.uniprot_id, uniprot_xml.gene_xml FROM genesymbol INNER JOIN uniprot ON genesymbol.entrez_id = uniprot.entrez_id INNER JOIN uniprot_xml ON uniprot.uniprot_id = uniprot_xml.uniprot_id WHERE genesymbol.entrez_id = " + str(entrez_id))
  rows = cur.fetchall()
  for row in rows:
    query_results.append({
        "entrez_id": row[0],
        "gene_symbol": row[1],
        "gene_name": row[2],
        "uniprot_id": row[3],
        "uniprot_xml": row[4],
        })
  return query_results

def drop_tables():
  cur, conn = connect()
  try:
    cur.execute("DROP TABLE IF EXISTS genesymbol")
    cur.execute("DROP TABLE IF EXISTS uniprot")
    cur.execute("DROP TABLE IF EXISTS uniprot_xml")
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print error

def convert_symbol_id(gene_symbol):
  cur, conn = connect()
  cur.execute("SELECT entrez_id FROM genesymbol WHERE gene_symbol = '" + gene_symbol + "'")
  entrez_id = cur.fetchone()[0]
  return entrez_id

if __name__ == '__main__':
  query = input()
  print query_gene(int(query))
