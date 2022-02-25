# TestPoint: Appointment booking for covid test centres

TestPoint is an appointment booking flask application that allows users to make appointments for covid tests and check their test results.

# Usage

TestPoint is a flask application and should be used with a dedicated WSGI server like uWSGI to host it on a website.

You can run TestPoint locally on your machine like this:
```
python3 runner.py (on Linux/Mac)
python runner.py (on Windows)
```

# Pre-requisites

In order to run TestPoint, please make sure to install the dependencies from [requirements.txt](requirements.txt) in a virtual environment like so:

1. Navigate to the main "testpoint" folder.
2. Create a virtual environment with venv, activate it and install the required packages with pip:
- On Linux/Mac
```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
deactivate
```
- On Windows
```
python -m venv .
venv\bin\activate
pip install -r requirements.txt
deactivate
```

Next, you have to configure the [config.ini-template](config.ini-template) so that TestPoint can store the data entered in the form in the MySQL database and send the notification emails:

1. Rename "config.ini-template" to "config.ini".
2. Enter the necessary information. Below you see an example of how to set the configuration if you want to run TestPoint locally:
```
[DATABASE]                          
USER = dbuser                       username of the mysql user of your mysql server
PW = dbpassword                     password for the mysql user
NAME = testpoint                    name of the database
ADDRESS = 127.0.0.1                 ip address of your mysql server (assuming mysql server runs on local machine)
PORT = 3306                         default port of mysql server

[EMAIL]
USER = youremail@testdomain.com     email address to send notification emails from
PW = yourpassword                   password for the email account related to the email address
SERVER = smtp.yourdomain.com        smtp server to send emails from
PORT = 465                          smtp port of smtp server
```

For more information on how to set up a mysql server on Ubuntu see [this](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) tutorial.

