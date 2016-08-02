# -*- coding: utf-8 -*-
import sqlite3
import os

def create_all_table():
    
    conn=sqlite3.connect('C:/DataBase/PortSRF.db')
    print"Create database successfully"
    
    
    conn.execute('''CREATE TABLE if not exists ELEC_DISTRIBUTION 
    (
      TERMINALID       INTEGER,
      CENTERFREQUENCY  REAL,
      BANDWIDTH        REAL,
      COUNTS           INTEGER,
      INTERVALTIME     REAL,
      NX               REAL,
      NY               REAL,
      DLETA            REAL,
      DTIME            DATE,
      LONGITUDE        DECIMAL(12,9),
      LATITUDE         DECIMAL(12,9),
      HEIGHT           DECIMAL(15,9),
      TRANSFERPOWER    REAL,
      TRANSINDEX       REAL
    );''')
    
    print '1'
    conn.execute('''
    
    CREATE TABLE if not exists ROUTE 
    (
      TERMINALID       INTEGER,
      CENTERFREQUENCY  REAL,
      BANDWIDTH        REAL,
      DTIME            DATE,
      LONGITUDE        DECIMAL(12,9),
      LATITUDE         DECIMAL(12,9),
      HEIGHT           DECIMAL(15,9),
      RECEIVEDPOWER    REAL
    );
    ''')
    
    print '2'
    conn.execute(''' CREATE TABLE if not exists ABNORMAL  
    (
      ABNORMALID        INTEGER,
      BELONGING         VARCHAR(20),
      LONGITUDE         DECIMAL(12,9),
      LATITUDE          DECIMAL(12,9),
      HEIGHT            DECIMAL(15,9),
      CENTERFREQUENCY   REAL,
      BANDWIDTH         REAL,
      PARAMETER         REAL,
      MODULATIONMODE    INTEGER,
      TRANSPOWER        REAL,
      TRANSINDEX        REAL,
      ACTIVITYDEGREE    REAL,
      SERVICEATTRIBUTE  INTEGER,
      ISILLEGAL         INTEGER
    );''')
    
    print '3'
    ###合法台站当前实际属性######
    conn.execute('''
    CREATE TABLE if not exists STATIONPROPERTY
    (
      STATIONID         INTEGER,
      BELONGING         VARCHAR(20),
      LONGITUDE         DECIMAL(12,9),
      LATITUDE          DECIMAL(12,9),
      HEIGHT            DECIMAL(15,9),
      CENTERFREQUENCY   REAL,
      TRANSPOWER        REAL,
      TRANSINDEX        REAL,
      BANDWIDTH         REAL,
      MODULATIONMODE    INTEGER,
      PARAMETER         REAL,
      SERVICEATTRIBUTE  VARCHAR(20),
      ACTIVITYDEGREE    REAL,
      ISILLEGALWORKING  INTEGER
    );
    ''')
    
    print '4'
    ##合法台站登记属性###
    conn.execute(''' CREATE TABLE if not exists REGISTEREDSTATION   
    (
      STATIONID         INTEGER,
      BELONGING         VARCHAR(20),
      LONGITUDE         DECIMAL(12,9),
      LATITUDE          DECIMAL(12,9),
      HEIGHT            DECIMAL(15,9),
      STARTFREQ         REAL,
      ENDFREQ           REAL,
      MAXTRANSPOWER     REAL,
      BANDWIDTH         REAL,
      MODULATIONMODE    INTEGER,
      PARAMETER         REAL,
      SERVICEATTRIBUTE  VARCHAR(20),
      COVERAGERADIUS    REAL,
      ACTIVITYDEGREE    REAL
    );
    ''')
    
    print '5'
    #####在网终端等级编号和等级名称###########
    conn.execute(''' 
    CREATE TABLE if not exists TERMINALGRADE
    (
      GRADE      INTEGER,
      GRADENAME  VARCHAR(20)
    );
     ''')
    
    print '6'
    #####在网终端##############
    conn.execute('''CREATE TABLE if not exists ONLINE_TERMINAL
    (
      TERMINALID      INT,
      TERMINAL_GRADE  INTEGER,
      LONGITUDE       DECIMAL(12,9),
      LATITUDE        DECIMAL(12,9),
      HEIGHT          DECIMAL(15,9),
      LOGINTIME       DATE
    );
    ''')
    
    print '7'
    ###注册终端表###############
    conn.execute('''CREATE TABLE if not exists TERMINALINFO
    (
      TERMINALID         INT,
      GRADE              INTEGER,
      LONGITUDE          DECIMAL(12,9),
      LATITUDE           DECIMAL(12,9),
      HEIGHT             DECIMAL(15,9),
      REGISTRATION_TIME  DATE,
      LOGINTIME          DATE,
      STATUS             INTEGER
    );
    ''')
    
    print '8'
    
    conn.execute('''
    
    CREATE TABLE if not exists LocalROUTE
    (
      LONGITUDE        DECIMAL(12,9),
      LATITUDE         DECIMAL(12,9)
    
  
    );
    ''')
    
    print '9'
    
    conn.execute('''
    
    CREATE TABLE if not exists Status
    (
     statusInsert  INTEGER
  
    );
    ''')
    
    print '10'
    
    
    
    
    conn.close()
    
# create_all_table()
