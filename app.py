from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from create_app import create_app

app = create_app()



if __name__ == '__main__':
    app.run(debug=True)
