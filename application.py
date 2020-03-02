from flask import Flask,render_template,request
import sqlite3 as sql
import pandas as pd
import numpy as np
application = app = Flask(__name__)
import os
import time
import redis
import pickle as pickle
import random
from sklearn.cluster import KMeans
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import pyplot as mpld3
from sklearn.cluster import KMeans
from scipy.spatial import distance


app = Flask(__name__)

con = sql.connect("database.db")
rd = redis.StrictRedis(host='Saii.redis.cache.windows.net', port=6380, db=0,password='7Z6Az0CdHRKCxGb3+a+XLxU52cc9xMIZPkXjJAfAn5U=',ssl=True)

@app.route("/")
def hello():
    return render_template('home.html')

if __name__ == '__main__':
   app.run()
