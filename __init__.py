from flask import Flask, flash, request, jsonify, url_for, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from functools import wraps
from datetime import datetime


from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import Required, Email,Length
from flask import make_response
from functools import update_wrapper
import time
import random

from flask.ext.login import LoginManager, UserMixin, login_required,login_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash



POSTS_PER_PAGE = 20  # pagination
#app = Flask (__name__, static_url_path='\C:\Users\$$\Desktop\dredger_bootstrap-2march20\static')
app = Flask (__name__)



bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:aaggss@localhost/dredger'
app.secret_key = 'my secret key is this'
login_manager = LoginManager()
login_manager.session_protection ='strong'
login_manager.login_view = "/"
login_manager.init_app(app)



class LoginForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

class User(UserMixin, db.Model):
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
    
"""class dieselLevel(db.Model):
    __tablename__ = 'dieselLevel'
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(25))
    level = db.Column(db.Integer)
    mTime = db.Column(db.DateTime,unique=True)  # If not unique then there will be logical errors
    ip = db.Column(db.String(15))

    def __init__(self, id,device, level,mTime,ip):
        #self.id=id
        self.device = device
        self.level = level
        self.mTime = mTime
        self.ip = ip
    def __repr__(self):
        return str(self.device)+','+str(self.level)+','+str(self.mTime)+','+str(self.ip)+'\n'"""

class dredger(db.Model):
    __tablename__ = 'db'
    id                  = db.Column(db.Integer, primary_key=True)
    dredger_name       = db.Column(db.String(25))
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
        return self.dredger_name+ ',' +str(self.time)+ ',' +str(self.storage_tank_level)+ ',' +\
                self.storage_tank_cap+ ',' +str(self.service_tank_level)+ ',' +self.service_tank_cap+ ',' +\
                str(self.flowmeter_1_in)+ ',' +str(self.flowmeter_1_out)+ ',' +self.engine_1_status+ ',' +str(self.flowmeter_2_in)+ ',' +\
                str(self.flowmeter_2_out)+ ',' +str(self.engine_2_status)+'\n'

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



class database():

    def db_init(self):
        db.create_all()
    def drop_all(self):
        db.drop_all()

    def fetchAll(self,dredger_name="dredger1"):
        try:                                                # Will fail if table doesn't exist
            data = dredger.query.order_by(dredger.time.desc()).all() # Select * FROM TABLE ORDER BY time
        except Exception as e:
            flash('fetchAll: '+str(e))
            #print 'Error:' + str(e)
        #print data.__repr__()
        return data
    def insertDb(self,arg,dredger_name="dredger1"):
        try:
            data=dredger(arg)
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            flash('insertDb: '+str(e))
            #print 'insertDb: '+str(e)
        
    
    def filterRange(self,fromTime,toTime,page,dredger_name="dredger1"):
        #print "---------------------------"
        results = dredger.query.filter(dredger.time <= toTime).filter(dredger.time >= fromTime).\
                        filter_by(dredger_name = dredger_name).order_by(dredger.time.desc()).\
                        paginate(page, POSTS_PER_PAGE, False)
        #print results.__repr__()
        #print "---------------------------"
        return results
            


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/',methods=['GET','POST'])
def login():
    #form = LoginForm()
    if request.method == 'POST':
        userName=request.form['username']
        
        if 'checkbox' in request.form:
            checkbox = True
        else:
            checkbox = False

        #print '--------->((('+str(userName)+')))<--------, '+ str(checkbox) + ','+ str(type(checkbox))
        user = User.query.filter_by(username=userName).first()
        if user is not None and user.verify_password(request.form['password']):
            login_user(user,checkbox)
            return redirect(request.args.get('next') or url_for('home'))
        flash ('Invalid credentials!!')
    return render_template('login.html')


""" ((Test code))
@app.route('/',methods=['GET','POST'])
def login():
    #form = LoginForm()
    if request.method == 'POST':
        userName=request.form['username']
        
        if 'checkbox' in request.form:
            checkbox = True
        else:
            checkbox = False

        #print '--------->((('+str(userName)+')))<--------, '+ str(checkbox) + ','+ str(type(checkbox))
        #user = User.query.filter_by(email=userName).first()
        if True:
            #login_user(user,checkbox)
            return redirect(request.args.get('next') or url_for('home'))
        flash ('Invalid credentials!!')
    return render_template('login.html')
"""




@app.route ("/select", methods=['GET', 'POST'])
@login_required
def select():
    if request.method == 'POST':
        userName=request.form['username']
        
        if 'checkbox' in request.form:
            checkbox = True
        else:
            checkbox = False

            #print '--------->((('+str(userName)+')))<--------, '+ str(checkbox) + ','+ str(type(checkbox))
            user = User.query.filter_by(email=userName).first()
        if user is not None and user.verify_password(request.form['password']):
            login_user(user,checkbox)
            return redirect(request.args.get('next') or url_for('home'))
        flash ('Invalid credentials!!')
    return render_template('select.html')

################# DREDGER 1 Start #############################
@app.route ("/dredger1/home", methods=['GET', 'POST'])
@login_required
def dredger1_home():
    return render_template('dredger1/home.html')

@app.route ("/dredger1/filter", methods=['GET', 'POST'])
@app.route ("/dredger1/filter/", methods=['GET', 'POST'])
@app.route('/dredger1/filter/<int:page>', methods=['GET', 'POST'])

@login_required
def dredger1_filter(page=1,fromTime=None,toTime=None):

    
    dbObj=database()
    if request.method == 'POST':
        results=None
        fromDate=request.form['fromDate']
        fromHour=request.form['fromHour']
        fromMin=request.form['fromMin']

        toDate=request.form['toDate']
        toHour=request.form['toHour']
        toMin=request.form['toMin']

        #print 'From:'+ str(fromDate) +','+str(fromHour)+','+str(fromMin)
        #print 'From:'+ str(toDate) +','+str(toHour)+','+str(toMin)

        fromTime= fromDate+' '+fromHour+':'+fromMin+':00'
        toTime= toDate+' '+toHour+':'+toMin+':00'
        
        
        try:
            fromTime = datetime.strptime(fromTime, "%Y-%m-%d %H:%M:%S")
            #fromTime = fromTime.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            if 'format' in str(e):
                flash('Error in format! Invalid Entry:- "'+str(fromDate)+'".'+\
                    '  Use "yyyy-mm-dd" format for "From Date"')
            else:
                flash('(From, '+str(fromDate)+'): '+str(e))
            #print "------------>1: " + 'results= None, ' + str(len(results.items))
            return render_template('dredger1/filter.html',results=None,fromDate=fromDate,toDate=toDate)
        

        
        try:
            toTime = datetime.strptime(toTime, "%Y-%m-%d %H:%M:%S")
            #toTime = toTime.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            if 'format' in str(e):
                flash('Error in format! Invalid Entry:- "'+str(toDate)+'".'+\
                    '  Use "yyyy-mm-dd" format for "To Date"')
            else:
                flash('(To, '+str(toDate)+'): '+str(e))
            #print "------------>2: " + 'results= None, ' + str(len(results.items))
            return render_template('dredger1/filter.html',results=None,fromDate=fromDate,toDate=toDate)
        
        #print 'from:'+str(type(fromTime))+': '+str(fromTime)
        #print 'to:'+str(type(toTime))+': '+str(toTime)

        #results=dbObj.filterRange(fromTime,toTime,page)
        """fromTime='2008-02-16 00:00:00'
        toTime='2015-04-12 00:00:00'"""
        #1
        

        
        results = dbObj.filterRange(fromTime,toTime,1,"dredger2")
        #print 'fromTime='+str(fromTime)
        #print 'toTime='+str(toTime)
        #print 'results='+str(results)
        #print 'request.method='+str(request.method)
        
        if not results:
            results=None


        
        try:
            fromDate
            toDate
        except NameError:
            #print "------------>3: " + 'results= ' + str(len(results.items))
            return render_template('dredger1/filter.html',results=results,fromTime=fromTime,toTime=toTime)        # If fromDate and toDate doesn't exist, then the page is being loaded for the first time                          
            #return "Hello"
        else:
            #print "------------>4: " + 'results= ' + str(len(results.items))
            return render_template('dredger1/filter.html',results=results,fromDate=fromDate,toDate=toDate,fromTime=fromTime,toTime=toTime)  # To make sure the date and time data doesn't vanish when clicking accept
            #return render_template('dredger1/filter.html',results=results)
            #return "Hello World"
        
    fromTime=request.args.get('fromTime','')
    toTime=request.args.get('toTime','')
    #2
    #print '-----------------------------------------------------------'
    
    if fromTime and toTime:
        results = dbObj.filterRange(fromTime,toTime,page,"dredger1")
    else:
        results=None
    
        
    """print "------------>5: " + 'page= '+str(page)+'results= ' ,
                if results:
                    str(len(results.items))
                else:
                    print 'None'"""

    #print 'fromTime='+str(fromTime)
    #print 'toTime='+str(toTime)
    #print 'results='+str(results)
    #print 'request.method='+str(request.method)
    #print '-----------------------------------------------------------'
    return render_template('dredger1/filter.html',results=results,fromTime=fromTime,toTime=toTime)

################# DREDGER 1 End #############################

################# DREDGER 2 Start #############################
@app.route ("/dredger2/home", methods=['GET', 'POST'])
@login_required
def dredger2_home():
    return render_template('dredger2/home.html')

@app.route ("/dredger2/filter", methods=['GET', 'POST'])
@app.route ("/dredger2/filter/", methods=['GET', 'POST'])
@app.route('/dredger2/filter/<int:page>', methods=['GET', 'POST'])

@login_required
def dredger2_filter(page=1,fromTime=None,toTime=None):

    
    dbObj=database()
    if request.method == 'POST':
        results=None
        fromDate=request.form['fromDate']
        fromHour=request.form['fromHour']
        fromMin=request.form['fromMin']

        toDate=request.form['toDate']
        toHour=request.form['toHour']
        toMin=request.form['toMin']

        #print 'From:'+ str(fromDate) +','+str(fromHour)+','+str(fromMin)
        #print 'From:'+ str(toDate) +','+str(toHour)+','+str(toMin)

        fromTime= fromDate+' '+fromHour+':'+fromMin+':00'
        toTime= toDate+' '+toHour+':'+toMin+':00'
        
        
        try:
            fromTime = datetime.strptime(fromTime, "%Y-%m-%d %H:%M:%S")
            #fromTime = fromTime.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            if 'format' in str(e):
                flash('Error in format! Invalid Entry:- "'+str(fromDate)+'".'+\
                    '  Use "yyyy-mm-dd" format for "From Date"')
            else:
                flash('(From, '+str(fromDate)+'): '+str(e))
            #print "------------>1: " + 'results= None, ' + str(len(results.items))
            return render_template('dredger2/filter.html',results=None,fromDate=fromDate,toDate=toDate)
        

        
        try:
            toTime = datetime.strptime(toTime, "%Y-%m-%d %H:%M:%S")
            #toTime = toTime.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            if 'format' in str(e):
                flash('Error in format! Invalid Entry:- "'+str(toDate)+'".'+\
                    '  Use "yyyy-mm-dd" format for "To Date"')
            else:
                flash('(To, '+str(toDate)+'): '+str(e))
            #print "------------>2: " + 'results= None, ' + str(len(results.items))
            return render_template('dredger2/filter.html',results=None,fromDate=fromDate,toDate=toDate)
        
        #print 'from:'+str(type(fromTime))+': '+str(fromTime)
        #print 'to:'+str(type(toTime))+': '+str(toTime)

        #results=dbObj.filterRange(fromTime,toTime,page)
        """fromTime='2008-02-16 00:00:00'
        toTime='2015-04-12 00:00:00'"""
        #1
        

        
        results = dbObj.filterRange(fromTime,toTime,1,"dredger2")
        #print 'fromTime='+str(fromTime)
        #print 'toTime='+str(toTime)
        #print 'results='+str(results)
        #print 'request.method='+str(request.method)
        
        if not results:
            results=None


        
        try:
            fromDate
            toDate
        except NameError:
            #print "------------>3: " + 'results= ' + str(len(results.items))
            return render_template('dredger2/filter.html',results=results,fromTime=fromTime,toTime=toTime)        # If fromDate and toDate doesn't exist, then the page is being loaded for the first time                          
            #return "Hello"
        else:
            #print "------------>4: " + 'results= ' + str(len(results.items))
            return render_template('dredger2/filter.html',results=results,fromDate=fromDate,toDate=toDate,fromTime=fromTime,toTime=toTime)  # To make sure the date and time data doesn't vanish when clicking accept
            #return render_template('dredger2/filter.html',results=results)
            #return "Hello World"
        
    fromTime=request.args.get('fromTime','')
    toTime=request.args.get('toTime','')
    #2
    #print '-----------------------------------------------------------'
    
    if fromTime and toTime:
        results = dbObj.filterRange(fromTime,toTime,page,"dredger2")
    else:
        results=None
    
        
    """print "------------>5: " + 'page= '+str(page)+'results= ' ,
                if results:
                    str(len(results.items))
                else:
                    print 'None'"""

    #print 'fromTime='+str(fromTime)
    #print 'toTime='+str(toTime)
    #print 'results='+str(results)
    #print 'request.method='+str(request.method)
    #print '-----------------------------------------------------------'
    return render_template('dredger2/filter.html',results=results,fromTime=fromTime,toTime=toTime)

################# DREDGER 2 End #############################
@app.route("/logout",methods=["GET"])
@login_required
def logout():
    form = LoginForm()
    logout_user()
    flash("You've logged out!!")
    return redirect(url_for('login'))


if __name__ == "__main__":
    #dbObj=database()
    dbObj.db_init()
    #dbObj.randomPacket("2015-04-01 00:00:00", "2015-04-30 00:00:00",'192.168.1.1')             
    #db.create_all()
    app.run(host='0.0.0.0',debug=True)

