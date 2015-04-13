#from flask import Flask, flash, request, jsonify, url_for, render_template, redirect,send_from_directory
from flask import Flask, flash, request, jsonify, url_for, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from functools import wraps
from datetime import datetime


from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,PasswordField,BooleanField
#from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField,DateTimeField
from wtforms.validators import Required, Email,Length
from flask import make_response
from functools import update_wrapper
import time
import random

from flask.ext.login import LoginManager, UserMixin, login_required,login_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash

#from flask.ext.mysql import MySQL


POSTS_PER_PAGE = 5  # pagination
#app = Flask (__name__, static_url_path='\C:\Users\$$\Desktop\dreadger_bootstrap-2march20\static')
app = Flask (__name__)



bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:aaggss@localhost/dreadger'
app.secret_key = 'my secret key is this'
login_manager = LoginManager()
login_manager.session_protection ='strong'
login_manager.login_view = "/"
login_manager.init_app(app)

logInStatus =dict()
logInStatus['logged_in'] = False   			#Determines initial state, if false the logs out automatically when pgm restarts
											# Don't use true!! Might cause error when clicking back button

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
    
 
 


class database():

    def db_init(self):
        db.create_all()

    def fetchAll(self):
        try:												# Will fail if table doesn't exist
            data = dieselLevel.query.order_by(dieselLevel.mTime.desc()).all() # Select * FROM TABLE ORDER BY mTime
        except Exception as e:
            #flash('fetchAll: '+str(e))
            print 'Error:' + str(e)
        #print data.__repr__()
        return data
    def insertDb(self,device,level,currentTime,ip):
        try:
            data=dieselLevel(device,level,currentTime,ip)
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
        while i in range(1,10):
            device='d'
            date=dbObj.randomDate(start,end,'%Y-%m-%d %H:%M:%S',random.random())
            level=str(random.randrange(100, 900, 2))
            dbObj.insertDb(device,level,date,ip)
            i=i+1
            

def nocache(view):
	@wraps(view)
	def no_cache(*args, **kwargs):
		response = make_response(view(*args, **kwargs))
		response.headers['Last-Modified'] = datetime.now()
		response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
		response.headers['Pragma'] = 'no-cache'
		response.headers['Expires'] = '-1'
		return response
	return update_wrapper(no_cache, view) 


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


		


"""def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if logInStatus['logged_in']:
			return f(*args, **kwargs)
		else:
			flash('You need to login first')
			return redirect(url_for('login'))
	return decorated_function
"""

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
		user = User.query.filter_by(email=userName).first()
		if user is not None and user.verify_password(request.form['password']):
			login_user(user,checkbox)
			return redirect(request.args.get('next') or url_for('home'))
		flash ('Invalid credentials!!')
	return render_template('login.html')




@app.route("/logout",methods=["GET"])
@login_required
def logout():
	form = LoginForm()
	logout_user()
	flash("You've logged out!!")
	return redirect(url_for('login'))


"""@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'GET' and logInStatus['logged_in'] == True:   # TO remove bug when clicking back button while logged in
		return redirect(url_for('home'))

	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			#error = 'Invalid Credentials.'
			flash('The username or password you entered is incorrect.')

		else:
			#session['logged_in'] = True
			logInStatus['logged_in'] = True
			#flash('You have logged in')
			return redirect(url_for('home'))
	return render_template('login.html')
"""





@app.route ("/index", methods=['GET', 'POST'])
@app.route ("/index/", methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@nocache
@login_required
def home(page=1,fromTime=None,toTime=None):
	#-------------Filter Page starts here--------------#  
	
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
		
		"""
		try:
			fromTime = datetime.strptime(fromTime, "%Y-%m-%d %H:%M:%S")
			#fromTime = fromTime.strftime("%Y-%m-%d %H:%M:%S")
		except ValueError as e:
			if 'format' in str(e):
				flash('(From, '+str(fromDate)+'), '+"Use format: yyyy-mm-dd hh:mm:ss")
			else:
				flash('(From, '+str(fromDate)+'): '+str(e))
			print "------------>1: " + 'results= None, ' + str(len(results.items))
			return render_template('home.html',results=None,fromDate=fromDate,toDate=toDate)
		"""

		"""
		try:
			toTime = datetime.strptime(toTime, "%Y-%m-%d %H:%M:%S")
			#toTime = toTime.strftime("%Y-%m-%d %H:%M:%S")
		except ValueError as e:
			if 'format' in str(e):
				flash('(To, '+str(toDate)+'), '+"Use format: yyyy-mm-dd hh:mm:ss")
			else:
				flash('(To, '+str(toDate)+'): '+str(e))
			print "------------>2: " + 'results= None, ' + str(len(results.items))
			return render_template('Home.html',results=None,fromDate=fromDate,toDate=toDate)
		"""
		#print 'from:'+str(type(fromTime))+': '+str(fromTime)
		#print 'to:'+str(type(toTime))+': '+str(toTime)

		#results=dbObj.filterRange(fromTime,toTime,page)
		"""fromTime='2008-02-16 00:00:00'
		toTime='2015-04-12 00:00:00'"""
		#1
		

		results = dieselLevel.query.filter(dieselLevel.mTime <= toTime).filter(dieselLevel.mTime >= fromTime).order_by(dieselLevel.mTime.desc()).paginate(page, POSTS_PER_PAGE, True)
	
		print 'fromTime='+str(fromTime)
		print 'toTime='+str(toTime)
		print 'results='+str(results)
		print 'request.method='+str(request.method)
		"""
		if not results:
			results=None"""


		
		try:
			fromDate
			toDate
		except NameError:
			print "------------>3: " + 'results= ' + str(len(results.items))
			return render_template('Home.html',results=results,fromTime=fromTime,toTime=toTime)        # If fromDate and toDate doesn't exist, then the page is being loaded for the first time                          
			#return "Hello"
		else:
			print "------------>4: " + 'results= ' + str(len(results.items))
			return render_template('Home.html',results=results,fromDate=fromDate,toDate=toDate,fromTime=fromTime,toTime=toTime)  # To make sure the date and time data doesn't vanish when clicking accept
			#return render_template('Home.html',results=results)
			#return "Hello World"
		
	fromTime=request.args.get('fromTime','')
	toTime=request.args.get('toTime','')
	#2
	print '-----------------------------------------------------------'
	
	if fromTime and toTime:
		results = dieselLevel.query.filter(dieselLevel.mTime <= toTime).filter(dieselLevel.mTime >= fromTime).order_by(dieselLevel.mTime.desc()).paginate(page, POSTS_PER_PAGE, True)
	else:
		results=None
		
	"""print "------------>5: " + 'page= '+str(page)+'results= ' ,
				if results:
					str(len(results.items))
				else:
					print 'None'"""

	print 'fromTime='+str(fromTime)
	print 'toTime='+str(toTime)
	print 'results='+str(results)
	print 'request.method='+str(request.method)
	print '-----------------------------------------------------------'
	return render_template('Home.html',results=results,fromTime=fromTime,toTime=toTime)

"""
@app.route('/logout')
def logout():
	logInStatus['logged_in']=False
	#flash('You were just logged out')
	return redirect(url_for('login'))
"""



"""

@app.route('/filter', methods=['GET', 'POST'])
@nocache
@login_required
def filterData():
	results=None
	dbObj=database()
	if request.method == 'POST':
		
		fromDate=request.form['fromDate']
		fromHours=request.form['fromHours']
		fromMinutes=request.form['fromMinutes']

		toDate=request.form['toDate']
		toHours=request.form['toHours']
		toMinutes=request.form['toMinutes']

		
		fromTime= fromDate+' '+fromHours+':'+fromMinutes+':00'
		toTime= toDate+' '+toHours+':'+toMinutes+':00'
		
		try:
			fromTime = datetime.strptime(fromTime, "%Y-%m-%d %H:%M:%S")
			#fromTime = fromTime.strftime("%Y-%m-%d %H:%M:%S")
		except ValueError as e:
			if 'format' in str(e):
				flash('(From, '+str(fromDate)+'), '+"Use format: yyyy-mm-dd hh:mm:ss")
			else:
				flash('(From, '+str(fromDate)+'): '+str(e))
			return render_template('filter.html',results=None,fromDate=fromDate,toDate=toDate)

		try:
			toTime = datetime.strptime(toTime, "%Y-%m-%d %H:%M:%S")
			#toTime = toTime.strftime("%Y-%m-%d %H:%M:%S")
		except ValueError as e:
			if 'format' in str(e):
				flash('(To, '+str(toDate)+'), '+"Use format: yyyy-mm-dd hh:mm:ss")
			else:
				flash('(To, '+str(toDate)+'): '+str(e))

			return render_template('filter.html',results=None,fromDate=fromDate,toDate=toDate)

		#print 'from:'+str(type(fromTime))+': '+str(fromTime)
		#print 'to:'+str(type(toTime))+': '+str(toTime)

		results=dbObj.filterRange(fromTime,toTime)
		
	
	
	if not results:
		results=None



	try:
		fromDate
		toDate
	except NameError:
		return render_template('filter.html',results=results)                                  # To make sure the date and time data doesn't vanish when clicking accept
	else:
		return render_template('filter.html',results=results,fromDate=fromDate,toDate=toDate)

"""

	

	
"""
@app.route('/logs', methods=['GET', 'POST'])
@login_required
def logs():
	if request.method == 'POST':
		result = []
		if (validate(request.form['param1'])):
			if (validate(request.form['param2'])):
		#print '1'
				results = dieselLevel.query.filter(conTime(request.form['param1']) < dieselLevel.mTime).filter(dieselLevel.mTime < conTime(request.form['param2'])).order_by(dieselLevel.mTime.desc()).all()
			else:
		#print '2'
				results = dieselLevel.query.filter(conTime(request.form['param1']) < dieselLevel.mTime).order_by(dieselLevel.mTime.desc()).all()
		else:
			if (validate(request.form['param2'])):
				#print '3'                
				results = dieselLevel.query.filter(dieselLevel.mTime < conTime(request.form['param2'])).order_by(dieselLevel.mTime.desc()).all()
			else:
				return render_template('log.html')
		json_results = []
		for result in results:
			d = { 'device' : result.device,
			'level': result.level,
			'datetime' : result.mTime, 
			'ip' : result.ip}
			json_results.append(d)
			return jsonify(items=json_results)    
	return render_template('log.html')"""





if __name__ == "__main__":
	#dbObj=database()
	#dbObj.db_init()
	#dbObj.randomPacket("2015-04-01 00:00:00", "2015-04-30 00:00:00",'192.168.1.1')				
	#db.create_all()
	app.run(host='0.0.0.0',debug=True)

