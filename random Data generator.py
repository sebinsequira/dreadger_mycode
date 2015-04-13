from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime


import time
import random

from werkzeug.security import generate_password_hash, check_password_hash




app = Flask (__name__)



db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:aaggss@localhost/dreadger'
app.secret_key = 'my secret key is this'




"""class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
    """
 
 


class database():

    def db_init(self):
        db.create_all()

    def fetchAll(self):
        try:                                                # Will fail if table doesn't exist
            data = dieselLevel.query.order_by(dieselLevel.mTime.desc()).all() # Select * FROM TABLE ORDER BY mTime
        except Exception as e:
            #flash('fetchAll: '+str(e))
            print 'Error:' + str(e)
        #print data.__repr__()
        return data
    def insertDb(self,id,device,level,currentTime,ip):
        try:
            data=dieselLevel(id,device,level,currentTime,ip)
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            #flash('insertDb: '+str(e))
            print 'insertDb: '+str(e)
        
    
    def filterRange(self,fromTime,toTime,page):
        #print "---------------------------"
        results = dieselLevel.query.filter(dieselLevel.mTime <= toTime).filter(dieselLevel.mTime >= fromTime).order_by(dieselLevel.mTime.desc()).paginate(page, POSTS_PER_PAGE, False)
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
            #flash('DB_init:'+str(e))
            print 'DB_init:'+str(e)

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
        while i in range(1,50):
            device='d'
            date=dbObj.randomDate(start,end,'%Y-%m-%d %H:%M:%S',random.random())
            level=str(random.randrange(100, 900, 2))
            dbObj.insertDb(i,device,level,date,ip)
            i=i+1
            



class dieselLevel(db.Model):
    __tablename__ = 'dieselLevel'
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(25))
    level = db.Column(db.Integer)
    mTime = db.Column(db.DateTime)
    ip = db.Column(db.String(15))

    def __init__(self,id,device, level,mTime,ip):
        #self.id=id
        self.device = device
        self.level = level
        self.mTime = mTime
        self.ip = ip
    def __repr__(self):
        return str(self.device)+','+str(self.level)+','+str(self.mTime)+','+str(self.ip)+'\n'




if __name__ == "__main__":
    dbObj=database()
    #dbObj.db_init()
    dbObj.randomPacket("2015-04-01 00:00:00", "2015-04-30 00:00:00",'192.168.1.1')              
    #db.create_all()
    

