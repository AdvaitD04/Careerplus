from flask import Flask,render_template,request,redirect, url_for, session, flash, abort,jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId,json_util
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
def index():
    # if 'user' in session:
        
    #     return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def loginuser():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        radio = request.form['radiobtn']

        user = mongo.db.register.find_one({'email': email, 'type': radio})

        if user:
            test = f.decrypt(user['password']).decode()
            if test == password:
                session['loginuser'] = True
                session['user'] = str(user['_id'])
                session['userid'] = user['userid']
                use = session['userid']
                type = user['type']
                if type == "Employee":
                    return redirect(url_for('dashboardemp'))
                elif type == "Employer":
                    return redirect(url_for('dashboardemployer'))
            else:
                flash('Invalid username or password', 'error')  # Flash an error message
                return redirect(url_for('loginuser'))
        else:
            flash('Invalid username or password', 'error')  # Flash an error message
            return redirect(url_for('loginuser'))

    elif 'user' in session:
        user = mongo.db.register.find_one({'userid': session['userid']})
        if user:
            type = user['type']
            if type == "Employee":
                return redirect(url_for('dashboardemp'))
            elif type == "Employer":
                return redirect(url_for('dashboardemployer'))

    return render_template('login.html')

  
@app.route('/logout',methods=['GET','POST'])
def logout():
    if 'user' in session:
        session.pop("user",None)
        return redirect(url_for('index'))

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
                user = mongo.db.register.find_one({'userid': userid,'email': email })
                if user:
                    flash('username already exists', 'error')  # Flash an error message
                    return redirect(url_for('signup'))
                
                else:
                    password = f.encrypt(password.encode()).decode()
                    users = {'userid': userid, 'email': email, 'password': password,'type': radio ,'date_created': datetime.utcnow()}
                    mongo.db.register.insert_one(users)
            else:
                flash('Confirm password and Password dont match', 'error')
                return redirect(url_for('signup'))

            return redirect(url_for('jobemployer', us = userid))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "An error occurred while registering. Please try again."

  return render_template('signup.html')



@app.route('/profile', methods=['GET', 'POST'])
def profile():
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
        return redirect(url_for('loginuser'))
    
    # Query MongoDB for job data (e.g., retrieve 10 job entries)
    job_entries = mongo.db.jobentries.find().limit(10)

    # Convert MongoDB cursor to a list of dictionaries
    job_data = [entry for entry in job_entries]

    # Remove _id field from each document
    for job in job_data:
        job.pop('_id', None)

    # Render the template with job data
    us = session['userid']
    return render_template('jobemployer.html', job_data=job_data, us=us)

#  for dashboard by user
@app.route('/Dashboardemp', methods=['GET', 'POST'])
def dashboardemp():
    if 'user' not in session:
        return redirect(url_for('loginuser'))
    
    if request.method == 'POST':
        # Retrieve the JSON data from the request
        data = request.json
        user_id = session.get('userid')
        # Update the data for the user ID if it already exists, otherwise insert new data
        existing_data = mongo.db.profileemp.find_one({"user_id": user_id})
        if existing_data:
              mongo.db.profileemp.update_one({"user_id": user_id}, {"$set": {"personal_info": data['personal_info']}}, upsert=True)
        
        
        else:
            data['user_id'] = user_id
            mongo.db.profileemp.insert_one(data)
        
        print("Received data:", data)
        return jsonify({"message": "Data received successfully"}), 200

    # If it's a GET request or if the POST request doesn't have JSON data
    # Retrieve the existing data for the user ID
    user_id = session.get('userid')
    data = mongo.db.profileemp.find_one({"user_id": user_id})
    
    if data is None:
        data = {'personal_info': {'name': '', 'dob': '', 'gender': '', 'age': '', 'phone': '', 'country': '', 'qualification': '', 'experience': '', 'languages': '', 'salary_type': '', 'expected_salary': '', 'job_category': ''}}
    
    return render_template('Dashboardemp.html', data=data,uid=user_id)

# for employer dashboard---------------------------------------

@app.route('/Dashboardemployer', methods=['GET', 'POST'])
def dashboardemployer():
    if 'user' not in session:
        return redirect(url_for('loginuser'))
    
    if request.method == 'POST':
        # Retrieve the JSON data from the request
        data = request.json
        user_id = session.get('userid')
        if 'personal_info' in data: 
        # Update the data for the user ID if it already exists, otherwise insert new data
         existing_data = mongo.db.profileemployer.find_one({"user_id": user_id})
         if existing_data:
               mongo.db.profileemployer.update_one({"user_id": user_id}, {"$set": {"personal_info": data['personal_info']}}, upsert=True)
        
        
         else:
             data['user_id'] = user_id
             mongo.db.profileemployer.insert_one(data)
        
         print("Received data:", data)
         return jsonify({"message": "Data received successfully"}), 200
        
        if 'General_info' in data:
            data['user_id'] = user_id
            mongo.db.jobentries.insert_one(data)


    
    user_id = session.get('userid')
    data = mongo.db.profileemployer.find_one({"user_id": user_id})
    
    if data is None:
        data = {'personal_info': {'name': '', 'dob': '', 'gender': '', 'age': '', 'phone': '', 'country': '', 'qualification': '', 'experience': '', 'languages': '', 'salary_type': '', 'expected_salary': '', 'job_category': ''}}
    
    return render_template('Dashboardemployer.html', data=data,uid=user_id)
  


if __name__ == "__main__":
    app.run(debug=True ,port = 8080)