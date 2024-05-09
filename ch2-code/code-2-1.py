from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
'''
	For database storage and configuration, I use a separate folder called data
	app
	|----data
	|----|--<database_name>

	Creating the databse, you have to run the following command
	`flask -A app.py --debug run`
	Just change the `app.py` name what your file name
'''
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<mysql_username>:<mysql_password>@<mysql_host>:<mysql_port>/<mysql_db>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/my_db.db'

db = SQLAlchemy(app)
		
if __name__ == "__main__":
	app.run(debug=True)