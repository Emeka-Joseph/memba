from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CSRFProtect

#we want to make the object-based config available
from membapp import config 

app = Flask(__name__,instance_relative_config=True)
csrf = CSRFProtect(app) #initialise extension, this will protect all your post rpoutes against csrf and you must pass it 
#load the config
app.config.from_pyfile('config.py', silent=False)

#how to load config from object-based config that is within your package 
app.config.from_object(config.LiveConfig)

db = SQLAlchemy(app)
#load the routes

from membapp import adminroutes,userroutes,forms