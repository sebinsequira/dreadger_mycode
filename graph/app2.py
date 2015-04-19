from flask import Flask, request,render_template,jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from random import randint

import time
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:aaggss@localhost/dreadger'
db = SQLAlchemy(app)

class dieselLevel(db.Model):
    __tablename__ = 'dieselLevel'
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(25))
    level = db.Column(db.Integer)
    mTime = db.Column(db.DateTime)
    ip = db.Column(db.String(15))

    def __init__(self, id,device, level,mTime,ip):
        #self.id=id
        self.device = device
        self.level = level
        self.mTime = mTime
        self.ip = ip
    def __repr__(self):
        return str(self.device)+','+str(self.level)+','+str(self.mTime)+','+str(self.ip)+'\n'


class database():

    def db_init(self):
        db.create_all()

    def fetchAll(self):
        try:                                                # Will fail if table doesn't exist
            data = dieselLevel.query.order_by(dieselLevel.mTime.desc()).all() # Select * FROM TABLE ORDER BY mTime
        except Exception as e:
            flash('fetchAll: '+str(e))
            #print 'Error:' + str(e)
        #print data.__repr__()
        return data
    def insertDb(self,device,level,currentTime,ip):
        try:
            data=dieselLevel(device,level,currentTime,ip)
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            flash('insertDb: '+str(e))
            #print 'insertDb: '+str(e)
        
    
    def filterRange(self,fromTime,toTime):
        #print "---------------------------"
        results = dieselLevel.query.filter(dieselLevel.mTime <= toTime).filter(dieselLevel.mTime >= fromTime).order_by(dieselLevel.mTime.desc())
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

@app.route('/')
def index(chartID = 'chart_ID', chart_type = 'spline', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    yAxis = {"title": {"text": 'yAxis Label'}}
    title = {"text": 'My Title'}
    results = dieselLevel.query.order_by(dieselLevel.mTime.desc()).limit(10)
    level=[]
    time=[]
    for result in results:
        level.append(int(result.level))
        #level.append(randint(0,100))
        time.append(result.mTime)


    series = [{"name": 'Diesel Level', "data": [x for x in level]}]
        
    xAxis = {"categories": [str(x) for x in time]}
    return render_template('graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

@app.route('/graph',methods=['GET','POST'])
def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):   #-------------Filter Page starts here--------------#  
    
    dbObj=database()
    results=None
    level=[]
    time=[]
    if request.method == 'POST':
        results=None
        fromDate=request.form['fromDate']
        toDate=request.form['toDate']
        
        fromTime= fromDate+' '+'00:00:00'
        toTime= toDate+' '+'00:00:00'

        fromTime = datetime.strptime(fromTime, "%Y-%m-%d %H:%M:%S")
        toTime = datetime.strptime(toTime, "%Y-%m-%d %H:%M:%S")

        results = dbObj.filterRange(fromTime,toTime)

        

        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
        title = {"text": 'My Title'}
        yAxis = {"title": {"text": 'Time'}}

        for result in results:
            level.append(int(result.level))
            time.append(result.mTime)
        

        series = [{"name": 'Diesel Level', "data": [x for x in level]}]
        
        xAxis = {"categories": [str(x) for x in time]}
        return render_template('index2.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
    return render_template('index2.html', results=None)
 
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)