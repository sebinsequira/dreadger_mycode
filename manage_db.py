from flask import Flask, flash, request, jsonify, url_for, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import time
from sqlalchemy import event
from sqlalchemy import DDL

app = Flask (__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:aaggss@localhost/dreadger'


class dreadger(db.Model):
    __tablename__ = 'db'
    id                  = db.Column(db.Integer, primary_key=True)
    dreadger_name       = db.Column(db.String(25))
    time                = db.Column(db.DateTime,unique=True)  # If not unique then there will be logical errors
    storage_tank_level  = db.Column(db.Integer)
    storage_tank_cap    = db.Column(db.String(25))
    service_tank_level  = db.Column(db.Integer)
    service_tank_cap    = db.Column(db.String(25))
    flowmeter_1_in      = db.Column(db.Integer)
    flowmeter_1_out     = db.Column(db.Integer)
    engine_1_status     = db.Column(db.String(25))
    flowmeter_2_in      = db.Column(db.Integer)
    flowmeter_2_out     = db.Column(db.Integer)
    engine_2_status     = db.Column(db.String(25))

    def __repr__(self):
        return self.dreadger_name+ ',' +str(self.time)+ ',' +str(self.storage_tank_level)+ ',' +\
                self.storage_tank_cap+ ',' +str(self.service_tank_level)+ ',' +self.service_tank_cap+ ',' +\
                str(self.flowmeter_1_in)+ ',' +str(self.flowmeter_1_out)+ ',' +self.engine_1_status+ ',' +str(self.flowmeter_2_in)+ ',' +\
                str(self.flowmeter_2_out)+ ',' +str(self.engine_2_status)+'\n'

    def __init__(self, arg):
        
        self.dreadger_name       = arg['dreadger_name']
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
    

class database():
    def db_init(self):
        db.create_all()
    def drop_all(self):
        db.drop_all()

    def fetchAll(self):
        try:                                                # Will fail if table doesn't exist
            data = dreadger.query.order_by(dreadger.time.desc()).all() # Select * FROM TABLE ORDER BY time
        except Exception as e:
            #flash('fetchAll: '+str(e))
            print 'Error:' + str(e)
        print data.__repr__()
        
    def insertDb(self,arg):
        try:
            data=dreadger(arg)
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            #flash('insertDb: '+str(e))
            print 'insertDb: '+str(e)
        
    
    def filterRange(self,fromTime,toTime,page):
        #print "---------------------------"
        results = dreadger.query.filter(dreadger.time <= toTime).filter(dreadger.time >= fromTime).order_by(dreadger.time.desc()).paginate(page, POSTS_PER_PAGE, False)
        
        #print results.__repr__()
        #print "---------------------------"
        return results

    def dummyData(self,time=datetime.now()):
        """
            -Inserts a single row of values into db
            -Default value for time is datetime.now
        """
        storage_tank_cap = ['Open','Close']
        service_tank_cap = ['Open','Close']
        engine_1_status = ['ON','OFF']
        engine_2_status = ['ON','OFF']

        try:
            self.db_init()
            arg={}
            arg['dreadger_name']        = 'dreadger_name'
            arg['time']                 = time
            arg['storage_tank_level']   = random.randint(1,1000)
            arg['storage_tank_cap']     = storage_tank_cap[random.randint(0,1)]
            arg['service_tank_level']   = random.randint(1,1000)
            arg['service_tank_cap']     = service_tank_cap[random.randint(0,1)]
            arg['flowmeter_1_in']       = random.randint(1,1000) 
            arg['flowmeter_1_out']      = random.randint(1,1000)
            arg['engine_1_status']      = engine_1_status[random.randint(0,1)]
            arg['flowmeter_2_in']       = random.randint(1,1000)
            arg['flowmeter_2_out']      = random.randint(1,1000)
            arg['engine_2_status']      = engine_2_status[random.randint(0,1)]
            dbObj.insertDb(arg)
        except Exception as e:
            #flash('DB_init:'+str(e))
            print 'DB_init:'+str(e)
    
    def dummyRange(self,num=50,fromDate='2014-01-01 00:00:00',toDate='2014-12-30 00:00:00'):
        """
            - Inserts a range of random values into db for time between the specified 
                date range 
        """
        for x in range(0,num):
            seed=random.random()        # for creating randomness
            date=self.randomDate(fromDate,toDate,seed)
            self.dummyData(date)

    def randomDate(self,start, end, prop,format='%Y-%m-%d %H:%M:%S'):
        """
        Function returns a random date between start and end dates
        """

        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))

        ptime = stime + prop * (etime - stime)

        res = time.strftime(format, time.localtime(ptime))
        res = datetime.strptime(res,"%Y-%m-%d %H:%M:%S") 
        return res


        
    def randomPacket(self,start,end,ip):
        dbObj=database()
        i=1
        while i in range(1,10):
            device='d'
            date=dbObj.randomDate(start,end,'%Y-%m-%d %H:%M:%S',random.random())
            level=str(random.randrange(100, 900, 2))
            dbObj.insertDb(device,level,date,ip)
            i=i+1
if __name__ == '__main__':
    dbObj = database()
    #dbObj.dummyRange()
    #dbObj.fetchAll()
    dbObj.filterRange('2014-08-01 00:00:00','2014-12-30 00:00:00')

    