import SocketServer
from sqlalchemy import *
from datetime import datetime

import logging


db = create_engine('mysql+mysqldb://admin:aaggss@localhost/dredger')


metadata = MetaData(db)


table = Table('db', metadata, autoload=True)

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        logger.info("Data: "+self.data)
        print 'Client: '+ self.data
        if len(self.data)>1:
            parsedata(self.data)
        
        # just send back the same data, but upper-cased
        #self.request.sendall("ACK_FROM_SERVER")


def insertDb(arg):
    try:
        i = table.insert()
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
        dictRow['dredger_name']        = data[0]
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
    PORT = 5000             

    logger      = logging.getLogger('serverLog1')
    hdlr        = logging.FileHandler('serverLog1.log')
    formatter   = logging.Formatter('%(asctime)s\t%(message)s',"%Y-%m-%d %H:%M:%S")
    
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)


    HOST, PORT = "", 5000

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print '\t\tINFO\t\t'+"Starting Server\n\n"
    logger.error('\t\tINFO\t\t'+'Starting Server\n\n')
    server.serve_forever()  
    
    
            
