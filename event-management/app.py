from flask import Flask, render_template, request
# from firebase_admin import credentials, firestore, initialize_app
import re
import os
import json
import boto3
import urllib3
#from passlib.hash import pbkdf2_sha256


app = Flask(__name__, template_folder='templates', static_folder='static')

post_url = urllib3.PoolManager()

state_machine_arn = 'arn:aws:states:us-east-1:096938558188:stateMachine:MyStateMachine'



@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('signup.html', message='Please Register')


@app.route("/", methods=['GET', 'POST'])
def login():
    return render_template('signin.html', message='Please login')


@app.route("/landing", methods=['GET', 'POST'])
def landing():
    return render_template('landing.html', message='landing')


@app.route("/weddingslot", methods=['GET', 'POST'])
def weddingSlot():
    firstname = request.form['firstname']
    email = request.form['email']
    phone = request.form['phone']
    city = request.form['city']
    guestcount = request.form['guestcount']
    date = request.form['date']
    budget = request.form['budget']
    event = request.form['event']
    print('evenet', request.form['event'])

   
    try:
        

        user_json = {
            "firstname": firstname,
                    "email": email,
                    "phone": phone,
                    "email": email,
                    "city":city,
                    "guestcount": guestcount,
                    "date": date,
                    "budget":budget,
                    "eventtype":event
        }
        json_dump = json.dumps(user_json)
        print(json_dump)
        # response = stepfunction_client.start_execution(stateMachineArn=state_machine_arn,
        #                                   input=json.dumps(user_json))

        # response = post_url.request(
        #     'POST', 'https://obxv6gfc82.execute-api.us-east-1.amazonaws.com/dev/bookingvalidation', body=json_dump)
        
        response = post_url.request(
            'POST', 'https://3id1a4uw09.execute-api.us-east-1.amazonaws.com/dev/verifyavailableslots', body=json_dump,headers={'Content-Type': 'application/json'})         

        print('response', response.data)
    except Exception as e:
        print('error', e)
        message = 'exception'
    return render_template('eventregister.html', message='We received your application. You will reveive an update shortly.')


@app.route("/eventregister", methods=['GET', 'POST'])
def eventRegister():
    print('request.form', request.form['event'])
    # event = request.form['wedding'] if request.form['wedding'] else request.form['birthday']
    return render_template('eventregister.html', message=request.form['event'])


@app.route('/signin-data', methods=['GET', 'POST'])
def signinData():
    message = ''
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:

        password = request.form['password']
        email = request.form['email']
        print(password, flush=True)
        print(email, flush=True)
        # all necessary validation are done here
        if not password or not email:
            message = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        
        else:
            message = 'You have successfully loggedin !'
            try:
                user_json = {
                    "password": password,
                    "email": email
                }
                json_dump = json.dumps(user_json)
                json_load = json.loads(json_dump)
            except Exception as e:
                print(e)
                message = 'exception'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
        return render_template('signup.html', message=message)

    return render_template('landing.html', message=message)


@app.route('/signup-data', methods=['GET', 'POST'])
def signupData():
    message = ''
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        email = request.form['email']
        print(password, flush=True)
        print(email, flush=True)
        # all necessary validation are done here
        if not password or not email:
            message = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     message = 'Username must contain only characters and numbers !'
        elif not re.match(password_pattern, password):
            message = 'Password should contain minimum 8 characters, at least one uppercase, at least one lowercase, at least one digit, at least one special character'
        else:
            message = 'Please confirm the subscription to our notification system to complete registration!'
            try:
                user_json = {
                    "firstname": firstname,
                    "lastname": lastname,
                    "password": password,
                    "email": email
                }
                json_dump = json.dumps(user_json)
                json_load = json.loads(json_dump)
                # response = post_url.request('POST', 'https://eqsnc5r3cbytxjmthschpoxyfm0tcrvi.lambda-url.us-east-1.on.aws/',
                #                             body=json_dump, headers={'Content-Type': 'application/json'})
                response = post_url.request('POST', 'https://3id1a4uw09.execute-api.us-east-1.amazonaws.com/dev/saveusertodbcf',
                                            body=json_dump, headers={'Content-Type': 'application/json'})
                
                 
                # response = post_url.request('POST', 'https://obxv6gfc82.execute-api.us-east-1.amazonaws.com/dev/saveusers',
                #                             body=json_dump, headers={'Content-Type': 'application/json'})
            except Exception as e:
                print(e)
                message = 'exception'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
        return render_template('signup.html', message=message)

    return render_template('signup.html', message=message)



if __name__=='__main__':
    app.run(host="0.0.0.0", port=80)