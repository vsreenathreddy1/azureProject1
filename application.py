from flask import Flask,render_template,request
app = Flask(__name__)

con = sql.connect("database.db")
rd = redis.StrictRedis(host='Saii.redis.cache.windows.net', port=6380, db=0,password='7Z6Az0CdHRKCxGb3+a+XLxU52cc9xMIZPkXjJAfAn5U=',ssl=True)

@app.route("/")
def hello():
    return render_template('home.html')

if __name__ == '__main__':
   app.run()
