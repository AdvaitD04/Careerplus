from flask import Flask,render_template,request,redirect, url_for, session, flash, abort,jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId
from cryptography.fernet import Fernet
app = Flask(__name__)

# mongodb connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Carrierplus'
app.config['SECRET_KEY'] = 'afdglnalnheognohe'
mongo = PyMongo(app)


#cryptography fernet
# Fernet key setup for encryption/decryption
file = open('key.key', 'rb')
key = file.read()
file.close()
f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def loginuser():
  if 'user' in session:
        
        return redirect(url_for('dashboard'))
   
  if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        radio = request.form['radiobtn']

        user = mongo.db.register.find_one({'email': email,'type': radio})

    
        if user:
            test = f.decrypt(user['password']).decode()
            if test == password:
              session['loginuser'] = True
              session['user'] = str(user['_id'])
              session['userid'] = user['userid']
              use = session['userid']
              return redirect(url_for('dashboard', us=use))
            else:
              flash('Invalid username or password', 'error')  # Flash an error message
              return redirect(url_for('loginuser'))
        else:
              flash('Invalid username or password', 'error')  # Flash an error message
              return redirect(url_for('loginuser'))    

  return render_template('login.html')
  


@app.route('/signup',methods=['GET','POST'])
def signup():
  if 'user' in session:
        
        return redirect(url_for('dashboard'))
  
  if request.method == 'POST':
        try:
            userid = request.form['username']
            email = request.form['email']
            password = request.form['password']
            repass = request.form['confirm_password']
            radio = request.form['radiobtn']
           

            if password == repass:
                user = mongo.db.register.find_one({'userid': userid})
                if user:
                    flash('Email or username already exists', 'error')  # Flash an error message
                    return redirect(url_for('signup'))
                
                else:
                    password = f.encrypt(password.encode()).decode()
                    users = {'userid': userid, 'email': email, 'password': password,'type': radio ,'date_created': datetime.utcnow()}
                    mongo.db.register.insert_one(users)
            else:
                return redirect(url_for('register'))

            return redirect(url_for('jobemployer', us = userid))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "An error occurred while registering. Please try again."

  return render_template('signup.html')



@app.route('/profile', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        # Handle image upload
        if 'image' in data:
            image_filename = data['image']
            # You can save the image file to a specific directory or process it as needed
            # For now, let's just print the image filename
            print("Uploaded image:", image_filename)
        # Insert the profile data into the MongoDB collection
        mongo.db.profile.insert_one(data)
        return jsonify(success=True)
    return render_template('profile.html')

@app.route('/dataall')
def data_all():
    profiles = list(mongo.db.profile.find({}))  # Exclude _id field from response
    return render_template('dataall.html', profiles=profiles)

@app.route('/jobemployer')
def jobemployer():

    if 'user' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('loginuser'))
    
    us = session['userid']
    return render_template('jobemployer.html',us=us)    



@app.route('/Dashboard')
def dashboard():

    if 'user' not in session:
        
        return redirect(url_for('loginuser'))
    
    us = session['userid']
    return render_template('Dashboardemp.html',us=us)


  


if __name__ == "__main__":
    app.run(debug=True ,port = 8080)