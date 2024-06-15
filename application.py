from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import InputRequired, Email
import boto3
import os

application = Flask(__name__)

#dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
region = os.environ['AWS_REGION']
dynamodb = boto3.resource('dynamodb',region_name=region)

def put_user(email):
    table = dynamodb.Table('users')
    response = table.put_item(
       Item={
            'email': email
        }
    )
    return response

# Index
@application.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user_resp = put_user(form.email.data)
        return render_template('obrigado.html')
    
    return render_template('index.html', form=form)

# Register Form Class
class RegisterForm(Form):
    email = StringField('Email', [InputRequired("Please enter your email.")])

if __name__ == '__main__':
    application.secret_key='secret123'
    application.run(debug=True)