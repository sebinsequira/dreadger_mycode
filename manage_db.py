from flask import Flask, flash, request, jsonify, url_for, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask (__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:aaggss@localhost/dreadger'


class dreadger(db.Model):
    __tablename__ = 'table'
    id                  = db.Column(db.Integer, primary_key=True)
    dreadger_name       = db.Column(db.String(25))
    time                = db.Column(db.DateTime,unique=True)  # If not unique then there will be logical errors
    storage_tank_level  = db.Column(db.Integer)
    storage_tank_cap    = db.Column(db.String(25))
    fuel_tank_level     = db.Column(db.Integer)
    fuel_tank_cap       = db.Column(db.String(25))
    flowmeter_1_in      = db.Column(db.Integer)
    flowmeter_1_out     = db.Column(db.Integer)
    engine_1_status     = db.Column(db.String(25))
    flowmeter_2_in      = db.Column(db.Integer)
    flowmeter_2_out     = db.Column(db.Integer)
    engine_2_status     = db.Column(db.String(25))
    
    

    def __init__(self, arg):
    	#self.id=id
        self.dreadger_name       = arg['dreadger_name']
        self.time                = arg['time']
        self.storage_tank_level  = arg['storage_tank_level']
        self.storage_tank_cap    = arg['storage_tank_cap']
        self.fuel_tank_level     = arg['fuel_tank_level']
        self.fuel_tank_cap       = arg['fuel_tank_cap']
        self.flowmeter_1_in      = arg['flowmeter_1_in']
        self.flowmeter_1_out     = arg['flowmeter_1_out']
        self.engine_1_status     = arg['engine_1_status']
        self.flowmeter_2_in      = arg['flowmeter_2_in']
        self.flowmeter_2_out     = arg['flowmeter_2_out']
        engine_2_status          = arg['engine_2_status']
    

class database():

    def db_init(self):
        db.create_all()

    def fetchAll(self):
        try:                                                # Will fail if table doesn't exist
            data = dreadger.query.order_by(dreadger.time.desc()).all() # Select * FROM TABLE ORDER BY time
        except Exception as e:
            flash('fetchAll: '+str(e))
            #print 'Error:' + str(e)
        #print data.__repr__()
        return data
    def insertDb(self,arg):
        try:
            data=dreadger(arg)
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            flash('insertDb: '+str(e))
            #print 'insertDb: '+str(e)
        
    
    def filterRange(self,fromTime,toTime,page):
        #print "---------------------------"
        results = dreadger.query.filter(dreadger.time <= toTime).filter(dreadger.time >= fromTime).order_by(dreadger.time.desc()).paginate(page, POSTS_PER_PAGE, False)
        #print results.__repr__()
        #print "---------------------------"
        return results

    def dummyData(self):
        try:
            self.db_init()
            for i in range(1,50):
                res = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   #Converting to proper format in string
                res = datetime.strptime(res,"%Y-%m-%d %H:%M:%S")    # Converting to proper format in datetime
                self.insertDb('dev',i,res,'192.168.1.1')
        except Exception as e:
            flash('DB_init:'+str(e))
            #print 'DB_init:'+str(e)

    def randomDate(self,start, end, format, prop):
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
    #dbObj.db_init()
    arg={}
    arg['dreadger_name']        ='a'
    arg['time']                 = datetime.now()
    arg['storage_tank_level']   = random.randint()
    arg['storage_tank_cap']     = 'b'
    arg['fuel_tank_level']      = random.randint()
    arg['fuel_tank_cap']        = 'c' 
    arg['flowmeter_1_in']       = random.randint() 
    arg['flowmeter_1_out']      = random.randint()
    arg['engine_1_status']      = 'd'
    arg['flowmeter_2_in']       = random.randint()
    arg['flowmeter_2_out']      = random.randint()
    arg['engine_2_status']      = 'e'

    dbObj.insertDb(arg)