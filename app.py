from flask import Flask,render_template,request,redirect, url_for, session, flash, abort,jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId
app = Flask(__name__)

# mongodb connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Carrierplus'
app.config['SECRET_KEY'] = 'afdglnalnheognohe'
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def loginuser():
  if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.register.find_one({'email': email, 'password': password})

        if user:
            session['loginuser'] = True
            session['user'] = str(user['_id'])
            session['userid'] = user['userid']
            use = session['userid']
            return redirect(url_for('dashboard', us=use))
        else:
            print("error")
            
            return redirect(url_for('login'))
  return render_template('login.html')
  


@app.route('/signup',methods=['GET','POST'])
def signup():
  if request.method == 'POST':
        try:
            userid = request.form['username']
            email = request.form['email']
            password = request.form['password']
            repass = request.form['confirm_password']
            if password == repass:
                users = {'userid': userid, 'email': email, 'password': password, 'date_created': datetime.utcnow()}
                mongo.db.register.insert_one(users)
            else:
                return redirect(url_for('register'))

            return redirect(url_for('dashboard', us = userid))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "An error occurred while registering. Please try again."

  return render_template('signup.html')
     

@app.route('/Dashboard/<us>')
def dashboard(us):
    return render_template('Dashboard.html',us=us)     
  


if __name__ == "__main__":
    app.run(debug=True ,port = 8080)