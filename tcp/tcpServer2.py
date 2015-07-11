import socket
import time
import sys
from sqlalchemy import *
from datetime import datetime

import logging
logger = logging.getLogger('serverLog2')
hdlr = logging.FileHandler('serverLog2.log')
formatter = logging.Formatter('%(asctime)s\t%(message)s',"%Y-%m-%d %H:%M:%S")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

db = create_engine('mysql+mysqldb://admin:aaggss@localhost/dredger')


metadata = MetaData(db)


backfill = Table('db', metadata, autoload=True)




def insertDb(arg):
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
        error_gsm           = arg['error_gsm'],
        error_main          = arg['error_main'],
        error_timeout       = arg['error_timeout'],
        error_unknown       = arg['error_unknown'],


        )
    except Exception as e:
        if 'Duplicate entry' in str(e):
            logger.error('insertDb\t'+"Duplicate entry for time: "+\
                str(arg['time'])+'\n\t\t\t'+'data:\t\t'+str(arg)+'\n')
        else:
            logger.error('insertDb\t'+str(e)+'\n')
        print 'insertDb: '+str(e)


def parsedata(data):
    """ 
    This function splits the string into a tuple containing device, level, datetime 
    the function parameter should be a string 
    return type is a (devicename,level,datetime)
    """
    try:
        data = data.strip()     # It removes all the newline character from the string
        data = data.split(';')  # Splits the string at every ';' character

        dictRow={}
        dictRow['dredger_name']       = data[0]
        dictRow['time']                = datetime.strptime( data[1], "%Y-%m-%d %H:%M:%S")
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
        dictRow['error_gsm']           = data[12]
        dictRow['error_main']          = data[13]
        dictRow['error_timeout']       = data[14]
        dictRow['error_unknown']       = data[15]

        
        insertDb(dictRow)
    except Exception as e:
        logger.error('parsedata\t'+str(e)+'\n\t\t\t'+\
            'data:\t\t'+str(data)+'\n')
        print e

if __name__ == '__main__':
    HOST = ''              
    PORT = 5001             
    print '\t\tINFO\t\t'+"Starting Server\n\n"
    logger.error('\t\tINFO\t\t'+'Starting Server\n\n')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)  
    
    while 1:
        try:
            conn, addr = s.accept()         # Blocking statement, waits for a connection

            
            while 1:
                try:
                    conn.send('ACK_FROM_SERVER')          #Dummy send to make sure that connection is correct
                    data = conn.recv(1024)

                    if data:
                        print 'Client: '+ data
                        parsedata(data)
                        
                except Exception as e:
                    print e
                    break                   # Break and wait for new conn, if dummy send fails

        except socket.timeout:
            print "Timeout!!\nConnection lost. Listening for a new controller."