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
                session['type'] = user['type']
                
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


@app.route('/aboutus')
def aboutus():
    # if 'user' in session:
        
    #     return redirect(url_for('dashboard'))
    return render_template('aboutus.html')


@app.route('/contactus')
def contactus():
    # if 'user' in session:
        
    #     return redirect(url_for('dashboard'))
    return render_template('contactus.html')



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

@app.route('/jobemployer', methods=['GET', 'POST'])
def jobemployer():
    
    type = session['type']

    if type == "Employer":
        return redirect(url_for('dashboardemployer')) 

    
    if request.method == 'POST':

       data = request.json 
       if 'locations' in data:
        # Retrieve filter parameters from the request
        locations = request.json.get('locations')
        min_salary = request.json.get('min_salary')
        max_salary = request.json.get('max_salary')
        
        # Add more filters as needed

        # Construct query based on filters
        query = {}
        
        if locations:
            query['location_more.city'] = {'$in': locations}
            
        if min_salary:
            query['salary'] = {'$gte': float(min_salary)}
        if max_salary:
            query['salary']['$lte'] = float(max_salary)
        
        
        # Query MongoDB for job data based on filters
        job_entries = mongo.db.jobentries.find(query).limit(10)

        # Convert MongoDB cursor to a list of dictionaries
        job_data = [entry for entry in job_entries]

        
        for job in job_data:
         job['_id'] = str(job['_id'])

       
        return jsonify(job_data)
       
       # for job bookmark using id of job

       if 'jobId' in data:
        print(data)

        if 'user' not in session:
         return redirect(url_for('loginuser'))
        
        
        user_id = session.get('userid')
        
        existing_data = mongo.db.profileemp.find_one({"user_id": user_id})
        if existing_data:
            # Check if 'jobApply' exists in existing_data
            if 'Bookmark' in existing_data:
                # Check if the jobId already exists in jobApply
                exists = mongo.db.profileemp.find_one({"user_id": user_id, "Bookmark": {"$elemMatch": {"jobId": data["jobId"]}}})
                if exists:
                    return jsonify({"message": "Data already exists"}), 200
                else:
                    # Append data to 'jobApply'
                    mongo.db.profileemp.update_one({"user_id": user_id}, {"$push": {"Bookmark": {"jobId":data["jobId"]}}})
            else:
                # Create 'jobApply' object if it doesn't exist
                mongo.db.profileemp.update_one({"user_id": user_id}, {"$set": {"Bookmark": {"jobId":[data["jobId"]]}}})
        else:
            # If user_id doesn't exist, create a new document
            mongo.db.profileemp.insert_one({"user_id": user_id, "Bookmark": {"jobId":[data["jobId"]]}})

        print("Received data:", data["jobId"])
        return jsonify({"message": "Data received successfully"}), 200

        

    # If it's a GET request, proceed with the existing logic to render the template with all job data
    job_entries = mongo.db.jobentries.find().limit(10)
    job_data = [entry for entry in job_entries]



    
    
    for job in job_data:
        job['_id'] = str(job['_id'])
    us = session['userid']
    return render_template('jobemployer.html', job_data=job_data, us=us)



@app.route('/jobdata', methods=['GET', 'POST'])
def fulljobs():
    if 'user' not in session:
        return redirect(url_for('loginuser'))
    type = session['type']

    if type == "Employer":
        return redirect(url_for('dashboardemployer'))    
    
    if request.method == 'POST':
        if type == "Employer":
         return redirect(url_for('dashboardemployer'))   
        # Retrieve the JSON data from the request
        data = request.json
        user_id = session.get('userid')
        # Update the data for the user ID if it already exists, otherwise insert new data
        existing_data = mongo.db.profileemp.find_one({"user_id": user_id})
        if existing_data:
            # Check if 'jobApply' exists in existing_data
            if 'jobApply' in existing_data:
                # Check if the jobId already exists in jobApply
                exists = mongo.db.profileemp.find_one({"user_id": user_id, "jobApply": {"$elemMatch": {"jobId": data["jobId"]}}})
                
                if exists:
                    return jsonify({"message": "Data already exists"}), 200
                else:
                    # Append data to 'jobApply'
                    mongo.db.profileemp.update_one({"user_id": user_id}, {"$push": {"jobApply": data}})
            else:
                # Create 'jobApply' object if it doesn't exist
                mongo.db.profileemp.update_one({"user_id": user_id}, {"$set": {"jobApply": [data]}})
        else:
            # If user_id doesn't exist, create a new document
            mongo.db.profileemp.insert_one({"user_id": user_id, "jobApply": [data]})
        #   for adding same in job entries
        
        job_id = ObjectId(data["jobId"])
        existing_data_jobentries = mongo.db.jobentries.find_one({"_id": job_id})
        print(existing_data_jobentries)
        if existing_data_jobentries:
            data["userid"] = user_id
            # Check if 'jobApply' exists in existing_data
            if 'jobApply' in existing_data_jobentries:
                # Check if the jobId already exists in jobApply
                exists = mongo.db.jobentries.find_one({"_id": job_id, "jobApply": {"$elemMatch": {"userid": user_id}}})

                
                if exists:
                    return jsonify({"message": "Data already exists"}), 200
                else:
                    # Append data to 'jobApply'
                    mongo.db.jobentries.update_one({"_id": job_id}, {"$push": {"jobApply": data}})
            else:
                # Create 'jobApply' object if it doesn't exist
                mongo.db.jobentries.update_one({"_id": job_id}, {"$set": {"jobApply": [data]}})
        else:
            # If user_id doesn't exist, create a new document
            mongo.db.jobentries.insert_one({"_id": job_id, "jobApply": [data]})    

        print("Received data:", data)
        return jsonify({"message": "Data received successfully"}), 200

    # If the request method is not POST, render a template (GET request)
    jobid = request.args.get('jobid')
    job_id = ObjectId(jobid)
    jobdata = mongo.db.jobentries.find_one({"_id": job_id})
    return render_template('fulljob.html', jobid=jobid,jobdata = jobdata)






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

        if 'sent_info' in data:
            existing_data = mongo.db.profileemployer.find({"user_id": user_id})
            print(existing_data)
                


    
    user_id = session.get('userid')
    data = mongo.db.profileemployer.find_one({"user_id": user_id})
    
    existing_data = mongo.db.jobentries.find({"user_id": user_id})

    print(user_id)
    
    entries = []
    jobentries = []
    i=1
    for document in existing_data:
     general_info = document.get("General_info", {})
     name = general_info.get("name", "N/A")
     company_name = general_info.get("companyname", "N/A")
     jobCat = general_info.get("Categ", "N/A")

     qualification_salary = document.get("qualification_salary", {})
     job_salary = qualification_salary.get("name", "N/A")

     job_location = document.get("location_more", {})
     job_city = job_location.get("city", {})
     job_deadline = job_location.get("job_deadline", {})

     
    
     job_apply = document.get("jobApply", [])
    
     for application in job_apply:
         userid = application.get("userid")
        
        # Query MongoDB for user data using the extracted user_id
         user_data = mongo.db.profileemp.find_one({"user_id": userid})
         i = i+1
         
        
        # Extract required fields from user data
         if user_data:
             user_personal_info = user_data.get("personal_info", {})
             user_name = user_personal_info.get("name", "N/A")
             user_country = user_personal_info.get("country", "N/A")
             user_languages = user_personal_info.get("languages", "N/A")
             user_languages = user_personal_info.get("languages", "N/A")
             
             
             
             
         else:
             user_name = "N/A"
             user_country = "N/A"
             user_languages = "N/A"
        
        # Append data to output_data list
         entry = {
            "name": name,
            "companyname": company_name,
            "userid": userid,
            "user_name": user_name,
            "user_country": user_country,
            "user_languages": user_languages,
            "jobApply": application  # Include the jobApply data
        }
         
         jobentry = {
            "name": name,
            "companyname": company_name,
            "Category":jobCat,
            "job_salary": job_salary,
            "job_city": job_city,
            "job_deadline":job_deadline,
            "count":i
        }
         
         entries.append(entry)
       
         jobentries.append(jobentry)
    
         
        
    
    if data is None:
        data = {'personal_info': {'name': '', 'dob': '', 'gender': '', 'age': '', 'phone': '', 'country': '', 'qualification': '', 'experience': '', 'languages': '', 'salary_type': '', 'expected_salary': '', 'job_category': ''}}
    
    return render_template('Dashboardemployer.html', data=data,uid=user_id,entries = entries,jobentries = jobentries)
  


if __name__ == "__main__":
    app.run(debug=True ,port = 8080)