import psycopg2
import csv
import xml.etree.ElementTree as ET
ET.register_namespace('', "http://uniprot.org/uniprot")

def connect():
  conn = None
  try:
    conn = psycopg2.connect(host="localhost", database="gene_info", user="bhernandev", password="mangocreator")
    cur = conn.cursor()
    drop_tables(cur, conn)
    create_tables(cur, conn)
    insert_data(cur, conn)
    cur.close()

  except(Exception, psycopg2.DatabaseError) as error:
    print(error)

  finally:
    if conn is not None:
      conn.close()
      print('Database connection closed')

def create_tables(cur, conn):
  #create the tables with the correct columns for the genes
  #one table for the entrez(primary), uniprot id, name
  #one table for the uniprot id + xml data (primary key is the uniprot_id and other column is just an XML dump of that specific entry)
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
    print(error)

def insert_data(cur, conn):
  #genesymbol
  csv_reader = None
  gene_rows = []
  with open("entrez_ids_genesymbol.csv") as genesymbol_file:
    genesymbol_file.readline()
    csv_reader = csv.reader(genesymbol_file)
    for row in csv_reader:
      temp_row = (int(row[0]), row[1], row[2])
      gene_rows.append(temp_row)
  insertion_sql = "INSERT INTO genesymbol(entrez_id, gene_symbol, gene_name) VALUES(%s, %s, %s)"
  #cur.executemany(insertion_sql, gene_rows)
  conn.commit()
  print("genesymbol committed")

  #uniprot
  uniprot_rows = []
  with open("entrez_ids_uniprot.txt") as uniprot_file:
    uniprot_file.readline()
    line = uniprot_file.readline()
    while line:
      row = line.split()
      temp_row = (int(row[0]), row[1])
      uniprot_rows.append(temp_row)
      line = uniprot_file.readline()
  insertion_sql = "INSERT INTO uniprot(entrez_id, uniprot_id) VALUES(%s, %s)"
  #cur.executemany(insertion_sql, uniprot_rows)
  conn.commit()
  print("uniprot committed")

  #uniprot_xml
  insertion_sql = "INSERT INTO uniprot_xml(uniprot_id, gene_xml) VALUES(%s, %s)"
  xml_rows = []
  count = 0
  tree = ET.iterparse('uniprot-human.xml')
  tree = iter(tree)
  for event, elem in tree:
    if count == 1000:
      cur.executemany(insertion_sql, xml_rows)
      conn.commit()
      count = 0
      xml_rows = []
    if elem.tag == '{http://uniprot.org/uniprot}entry':
      temp_xml = ET.tostring(elem)
      names = elem.iterfind('{http://uniprot.org/uniprot}name')
      for name in names:
        uniprot_id = name.text
        temp_xml_string = temp_xml.decode("utf-8")
        temp_row = (uniprot_id, temp_xml_string)
        xml_rows.append(temp_row)
        count = count + 1
        print(count)

  cur.executemany(insertion_sql, xml_rows)
  conn.commit()
  print("uniprot_xml committed")

def query_gene(entrez_id, cur, conn):
  return None

def drop_tables(cur, conn):
  try:
    cur.execute("DROP TABLE IF EXISTS genesymbol")
    cur.execute("DROP TABLE IF EXISTS uniprot")
    cur.execute("DROP TABLE IF EXISTS uniprot_xml")
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)

if __name__ == '__main__':
  connect()
