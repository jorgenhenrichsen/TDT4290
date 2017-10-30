import sqlite3
import csv
import codecs
import pyodbc
from meza import io
import numpy as np
import jaydebeapi




def csvread (file):
    reader = csv.reader(open(file))
    for row in reader:
        print(row)


def sqliteread(file):
    conn = sqlite3.connect(file)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

    rows = cur.fetchall()
    names = []
    for row in rows:
        names.append(row)
    print(names)
    #print(t)

    #cur.execute("SELECT * FROM (1938-1972 Oversikt - Resultater), ")

    #rows = cur.fetchall()
    #for row in rows:
     #   print(row)


def readData(file):
    with codecs.open(file, "r", encoding='utf-8') as f:

        data = f.read()
        print(data)

    con = sqlite3.connect(':memory:')

    with con:
        cur = con.cursor()

        #sql = readData(file)
        cur.executescript(data)

        cur.execute("SELECT * FROM res")

        rows = cur.fetchall()

        for row in rows:
            print(row)

def mdb():
    #cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='127.0.0.1', port='1433', user='sa',
    # ?? Maybe work?                     password='*****', database='****')
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb)};'
        r'DBQ=NVF_Historiske.mdb'
    )
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    for table_info in crsr.tables(tableType='TABLE'):
        print(table_info.table_name)

def meza():
    d = {}
    list = []
    records = io.read_mdb('NVF_Historiske.mdb', '1938-1972 Oversikt - Resultater')
    #for r in records:
        #list.extend(r)
        #np.save('my_file', )


    print(records)

def mdb2()
    ucanaccess_jars = [
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/"
    ]
    classpath = ":".join(ucanaccess_jars)
    cnxn = jaydebeapi.connect(
        "net.ucanaccess.jdbc.UcanaccessDriver",
        "jdbc:ucanaccess:///home/gord/test.accdb;newDatabaseVersion=V2010",
        ["", ""],
        classpath
    )
    crsr = cnxn.cursor()
    try:
        crsr.execute("DROP TABLE table1")
        cnxn.commit()
    except jaydebeapi.DatabaseError as de:
        if "user lacks privilege or object not found: TABLE1" in str(de):
            pass
        else:
            raise
    crsr.execute("CREATE TABLE table1 (id COUNTER PRIMARY KEY, fname TEXT(50))")
    cnxn.commit()
    crsr.execute("INSERT INTO table1 (fname) VALUES ('Gord')")
    cnxn.commit()
    crsr.execute("SELECT * FROM table1")
    for row in crsr.fetchall():
        print(row)
    crsr.close()
    cnxn.close()


meza()