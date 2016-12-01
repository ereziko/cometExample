from gevent import monkey; monkey.patch_all()
from flask import Flask, request, render_template, url_for, redirect
from flaskext.mysql import MySQL
from models.gamemessaging import GameNamespace
from models.gameserver import GameServer
from socketio import socketio_manage
from models.registration import RegistrationForm
import ConfigParser, os

 
# Flask routes
app = Flask(__name__)
mysql = MySQL()

#Load configurations
settings = ConfigParser.ConfigParser()
path = os.path.join(os.getcwd(), 'config', 'config.ini') 
settings.read(path)
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = settings.get('Database', 'user')
app.config['MYSQL_DATABASE_PASSWORD'] = settings.get('Database', 'passwd')
app.config['MYSQL_DATABASE_DB'] =  settings.get('Database', 'db')
app.config['MYSQL_DATABASE_HOST'] = settings.get('Database', 'host')
mysql.init_app(app)



#class Tester(db.Model):
#	id = db.Column(db.Integer, primary_key=True)
#	username = db.Column(db.String(80), unique=True)
#	email = db.Column(db.String(120), unique=True)
#	age = db.Column(db.Integer)
#	gender = db.Column(db.Boolean)
#
#	def __init__(self, username, email, age, gender):
#		self.username = username
#		self.email = email
#		self.age = age
#		self.gender = True if gender == 'Male' else False
#
#	def __repr__(self):
#		return '<User %r>' % self.username
#		
#class Message(db.Model):
#	id = db.Column(db.Integer, primary_key=True)
#	message = db.Column(db.String(100))
#	from_tester_id = db.Column(db.Integer, db.ForeignKey('tester.id'))
#	from_tester = db.relationship('Tester', backref=db.backref('message', lazy='dynamic'))
#	to_tester_id = db.Column(db.Integer, db.ForeignKey('tester.id'))
#	to_tester = db.relationship('Tester', backref=db.backref('message', lazy='dynamic'))
#	
#	def __init__(self, from_tester, to_tester, message):
#		self.message = message
#		self.from_tester = from_tester
#		self.to_tester = to_tester
		
			

#when a socket connects it looks something like:
#/socket.io/1/websocket/<sess_id>
@app.route("/socket.io/<path:path>")
def run_socketio(path):
	socketio_manage(request.environ, {'': GameNamespace})
	return ''

@app.route('/')
def index():
    return render_template('chat.html')
	
@app.route('/configure/')
def configure():
	#form = RegistrationForm(request.form)
    #if request.method == 'POST' and form.validate():
    #    print (form.first_name.data, 
	#				form.last_name.data, form.email.data,
    #                form.id.data, form.age.data)
    #    #db_session.add(user)
    #    #flash('Thanks for registering')
	#	return redirect(url_for('initialize_game_session'))
	return render_template('configure.html')

@app.route('/initialize-game/',  methods=['GET', 'POST'])
def initialize_game_session():
	pass
	
	
@app.route('/register-tester/' , methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        print (form.first_name.data, 
					form.last_name.data, form.email.data,
                    form.id.data, form.age.data)
        #db_session.add(user)
        #flash('Thanks for registering')
        return redirect(url_for('tester_is_ready_to_begin'))
    return render_template('register.html', form=form)

@app.route('/tester-ready/')
def tester_is_ready_to_begin():
	return render_template('ready-player.html')	
				
		
if __name__ == '__main__':
    print 'Listening on http://localhost:8080'
	
    app.debug = True
    import os
    from werkzeug.wsgi import SharedDataMiddleware
    app = SharedDataMiddleware(app, {
        '/': os.path.join(os.path.dirname(__file__), 'static')
        })
    
    GameServer(mysql, ('0.0.0.0', 8080), app,
        resource="socket.io", policy_server=False).serve_forever()

