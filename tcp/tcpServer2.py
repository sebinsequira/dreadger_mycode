import socket
import time
import sys
"""from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from datetime import datetime


Base = declarative_base()
##creating a mysql database object object 
engine = create_engine('mysql://admin:aaggss@localhost/dredger')

# packet should be or the format given below
# "ABC123;1000;15/9/2014 13:10"




class dredger(Base):
    __tablename__ = 'db'
    id                  = Column(Integer, primary_key=True)
    dredger_name       = Column(String(25))
    time                = Column(DateTime,unique=True)  # If not unique then there will be logical errors
    storage_tank_level  = Column(Integer)
    storage_tank_cap    = Column(String(25))
    service_tank_level  = Column(Integer)
    service_tank_cap    = Column(String(25))
    flowmeter_1_in      = Column(Integer)
    flowmeter_1_out     = Column(Integer)
    engine_1_status     = Column(String(25))
    flowmeter_2_in      = Column(Integer)
    flowmeter_2_out     = Column(Integer)
    engine_2_status     = Column(String(25))
    error_code          = Column(String(25))

    def __repr__(self):
        return self.dredger_name+ ',' +str(self.time)+ ',' +str(self.storage_tank_level)+ ',' +\
                self.storage_tank_cap+ ',' +str(self.service_tank_level)+ ',' +self.service_tank_cap+ ',' +\
                str(self.flowmeter_1_in)+ ',' +str(self.flowmeter_1_out)+ ',' +self.engine_1_status+ ',' +str(self.flowmeter_2_in)+ ',' +\
                str(self.flowmeter_2_out)+ ',' +str(self.engine_2_status)+','+str(error_code)+'\n'

    def __init__(self, arg):
        
        self.dredger_name       = arg['dredger_name']
        self.time                = arg['time']
        self.storage_tank_level  = arg['storage_tank_level']
        self.storage_tank_cap    = arg['storage_tank_cap']
        self.service_tank_level  = arg['service_tank_level']
        self.service_tank_cap    = arg['service_tank_cap']
        self.flowmeter_1_in      = arg['flowmeter_1_in']
        self.flowmeter_1_out     = arg['flowmeter_1_out']
        self.engine_1_status     = arg['engine_1_status']
        self.flowmeter_2_in      = arg['flowmeter_2_in']
        self.flowmeter_2_out     = arg['flowmeter_2_out']
        self.engine_2_status     = arg['engine_2_status']
        self.error_code          = arg['error_code']
"""
from sqlalchemy import *
from datetime import datetime as dt

db = create_engine('mysql+mysqlconnector://admin:aaggss@localhost/dredger')
#FUll- PAth : sqlite:////tmp/tutorial/joindemo.db
# sudo apt-get install python3-mysql.connector


metadata = MetaData(db)


backfill = Table('db', metadata, autoload=True)




def insertDb(self,arg):
    try:
        i = backfill.insert()
        i.execute(dredger_name = arg['dredger_name'],
        time                = arg['time'],                  
        storage_tank_level  = arg['storage_tank_level'],
        storage_tank_cap    = arg['storage_tank_cap'],
        service_tank_level  = arg['service_tank_level'],
        service_tank_cap    = arg['service_tank_cap'],
        flowmeter_1_in      = arg['flowmeter_1_in'],
        flowmeter_1_out     = arg['flowmeter_1_out'],
        engine_1_status     = arg['engine_1_status'],
        flowmeter_2_in      = arg['flowmeter_2_in'],
        flowmeter_2_out     = arg['flowmeter_2_out'],
        engine_2_status     = arg['engine_2_status'],
        error_code          = arg['error_code'],

        )
    except Exception as e:
        print ('insertDb: '+str(e))


def parsedata(data):
    """ 
    This function splits the string into a tuple containing device, level, datetime 
    the function parameter should be a string 
    return type is a (devicename,level,datetime)
    """
    try:
        data = data.strip()     # It removes all the newline character from the string
        data = data.split(';')  # Splits the string at every ';' character
        
        s = session()
        

        dictRow={}
        dictRow['dredger_name']       = data[0]
        dictRow['time']                = datetime.strptime( data[1], "%d/%m/%Y %H:%M:%S")
        dictRow['storage_tank_level']  = int(data[2])
        dictRow['storage_tank_cap']    = data[3]
        dictRow['service_tank_level']  = int(data[4])
        dictRow['service_tank_cap']    = data[5]
        dictRow['flowmeter_1_in']      = int(data[6])
        dictRow['flowmeter_1_out']     = int(data[7])
        dictRow['engine_1_status']     = data[8]
        dictRow['flowmeter_2_in']      = int(data[9])
        dictRow['flowmeter_2_out']     = int(data[10])
        dictRow['engine_2_status']     = data[11]
        dictRow['error_code']          = data[12]

        """s.add(dredger(dictRow))
                                s.commit()
                                s.close()"""
        insertDb(dictRow)
    except Exception as e:
        print (e)

## Main function 
## Here the code for opening the port is written.
if __name__ == '__main__':
    HOST = ''              
    PORT = 5000             


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.settimeout(TIMEOUT)
    s.bind((HOST, PORT))
    s.listen(1)  
    #session = sessionmaker() 
    #session.configure(bind=engine)

    while 1:
        try:
            conn, addr = s.accept()         # Blocking statement, waits for a connection

            
            while 1:
                try:
                    conn.send('ACK_FROM_SERVER')          #Dummy send to make sure that connection is correct
                    data = conn.recv(1024)

                    if data:
                        print ('Client: '+ data)
                        parsedata(data)
                        
                except Exception as e:
                    print (e)
                    break                   # Break and wait for new conn, if dummy send fails

        except socket.timeout:
            print ("Timeout!!\nConnection lost. Listening for a new controller.")
            
