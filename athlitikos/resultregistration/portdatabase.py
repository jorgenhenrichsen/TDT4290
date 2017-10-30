import sqlite3
import csv
import codecs
import pyodbc
from meza import io
import numpy as np

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
    records = io.read_mdb('NVF_Historiske.mdb', '1992-1997 Resultater')
    #for r in records:
        #np.save('my_file.npy', dictionary)


    print(records)

meza()