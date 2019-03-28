#!C:\Users\Administrator\AppData\Local\Programs\Python\Python37\python.exe
import sys


from wsgiref.handlers import CGIHandler
from run import app

CGIHandler().run(app)