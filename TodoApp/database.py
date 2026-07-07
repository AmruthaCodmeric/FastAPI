#database.py file is going to be used for us to be able to create our URL string which will connect our API application to our database
#SQLALCHEMY is an orm,which is what our API application is going to use to be able to create a database and be able to create a connection
# to a database and being able to use all  the database records within our application
#first install sqlalchemy in to fast API environment -on terminal type..pip install sqlalchemy
#create an engine for our application, now database engine is something that we can use to be able to open up a connection and be able to use our database
#connect_argument are argument that we can pass into our create engine, which will allow us to be able to define some kind of connection to a database
#we want to say check same thread of type false and now by default , sqlite will allow one thread to communicate with it
#assume that each thread will handle an independent request , this is to prevent any kind of accident sharing of the same connection of different kind of requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'"""
SQLALCHEMY_DATABASE_URL = (
"postgresql://neondb_owner:npg_qXJDtf07GVSc@ep-solitary-bar-aos6xhkl-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
)

""" SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1357900@localhost/TodoApplicationDatabase' """

# pip install pymysql (library)
"""SQLALCHEMY_DATABASE_URL ='mysql+pymysql://root:1357900@127.0.0.1:3306/TodoApplicationDatabase'"""
# This url is going to be used to be able to create a location of this database on our fast api application

#below code was only used for sqlite
""" engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})"""

"""engine = create_engine(SQLALCHEMY_DATABASE_URL)"""
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)
#SessionLocal-> perform database operations.(db.add(todo))
#sessionmaker is a factory that creates sessions.Instead of manually creating sessions every time, you define a template:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
#declarative_base() creates a base class that your database models.py will inherit from