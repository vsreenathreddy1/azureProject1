from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
import time
import redis as redis
import csv
import pickle
import random
import os
from sklearn.cluster import KMeans
from sklearn import preprocessing
import matplotlib.pyplot as plt
import re
app = Flask(__name__)

con = sql.connect("database.db")
#rd = redis.StrictRedis(host='Saii.redis.cache.windows.net', port=6380, db=0,password='7Z6Az0CdHRKCxGb3+a+XLxU52cc9xMIZPkXjJAfAn5U=',ssl=True)

#port = int(os.getenv('PORT', 8000))

myHostname = "saiii.redis.cache.windows.net"
myPassword = "DlAGHScUdv36nwvZL2jpP4KPVo6fuuc0v0u1v4oPOMk="

#r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl_cert_reqs=None)

pool = redis.ConnectionPool(host='Saiii.redis.cache.windows.net', port=6380, password='DlAGHScUdv36nwvZL2jpP4KPVo6fuuc0v0u1v4oPOMk=', db=0, connection_class=redis.SSLConnection, ssl_cert_reqs='none')
r = redis.Redis(connection_pool=pool)

print(r)




'''
    file = pd.read_csv("./static/all_month.csv")
    r.set(1,file)
    
    #print(r.get(1))
    user = {"Name":"Pradeep", "Company":"SCTL", "Address":"Mumbai", "Location":"RCP"}
    
    
    hi=pd.read_csv("./static/all_month.csv")
    print(hi.head())
    cols=[]
    for col in hi.columns:
    #print(col)
    cols.append(col)
    r.set(col,hi[col])
    r.hmset('bye',cols,hi[col])
    #print(r.get(col))
    print(r.get("time"))
    
    print(r.get('bye'))
    r.hmset("pythonDict", user)
    print(type(r.hgetall("pythonDict")))
    #print(r.hgetall("pythonDict"))
    r.set('name',r.hmget("pythonDict","Name"))
    #print(r.get('name'))
    #print(r.hmget("pythonDict","Name"))
    '''
'''
    for i in range(len(all)):
    r.set(i, all[i])
    
    value = r.get(2)
    print(value)
    '''
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload')
def upload_csv():
    return render_template('upload.html')


@app.route('/adddata',methods = ['POST', 'GET'])
def adddata():
    if request.method == 'POST':
        con = sql.connect("database.db")
        csv = request.files['myfile']
        file = pd.read_csv(csv)
        start_time=time.time()
        file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
        con.close()
        end_time=time.time()-start_time
        return render_template("adddata.html", msg = "Record inserted successfully", time=end_time)


@app.route('/display')
def display():
    keyname = 'hi'
    start_time = time.time()
    if(r.exists(keyname)):
        isCache = 'with Cache'
        rows = pickle.loads(r.get(keyname))
        print(time.time() - start_time,isCache)
        r.delete(keyname)
    else:
        isCache = 'without Cache'
        con = sql.connect("database.db")
        
        cur = con.cursor()
        cur.execute("select * from Earthquake")
        
        rows = cur.fetchall();
        print(time.time()-start_time,isCache)
        print(len(rows))
        con.close()
        print(time.time() - start_time,isCache)
        r.set(keyname, pickle.dumps(rows))
    taken_time=time.time()-start_time
    return render_template("display.html", data=rows, data1=taken_time, isCache=isCache)

@app.route('/multiple')
def multiple():
    start_time = time.time()
    #keyname = 'bye'
    count=0
    count1=0
    for i in range(100):
        #mag = "{:.1f}".format(random.uniform(1, 8))
        mag = round(random.uniform(1, 8),2)
        if (r.exists(mag)):
            rlist = []
            isCache = 'with Cache'
            print(isCache,mag)
            
            rows = pickle.loads(r.get(mag))
            #rlist.append(rows)
            #print(rows)
            #taken_time = time.time() - start_time
            print(time.time() - start_time, isCache)
            #r.delete(str(i))
            count+=1
        else:
            rlist = []
            isCache = 'without Cache'
            #start_time = time.time()
            con = sql.connect("database.db")
            cur = con.cursor()
            
            #print(isCache,mag)
            mag1 = random.uniform(1, 8)
            cur.execute("select * from Earthquake where mag > "+ str(mag))
            rows = cur.fetchall();
            r.set(mag, pickle.dumps(rows))
            count1+=1
            
            con.close()
    taken_time = time.time() - start_time
    print(count,count1)
    return render_template("display.html", data=rows, data1=taken_time, count=count,count1=count1, isCache=isCache)

@app.route('/net', methods = ['POST', 'GET'])
def net():
    
    if(request.method=='POST'):
        keyname = 'shevi'
        loop = request.form['loop']
        #print(int(loop))
        net = request.form['net']
        count = 0
        count1 = 0
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("select distinct net from Earthquake where net like ?", (net+'%',))
        rows1 = cur.fetchall()
        con.close()
        
        start_time = time.time()
        for i in range(int(loop)):
            
            ran_num = random.randint(0, len(rows1) - 1)
            if r.exists(keyname + str(rows1[ran_num])):
                isCache = "with Cache"
                
                res = pickle.loads(r.get(keyname + str(rows1[ran_num])))
                count+=1
            
            else:
                net1 = str(rows1[ran_num])
                isCache = "without Cache"
                #sh.append(isCache)
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute("select * from Earthquake where net = ?", (net1[2:4], ))
                temp_res = cur.fetchall()
                r.set(keyname + str(rows1[ran_num]), pickle.dumps(temp_res))
                count1+=1
                con.close()
        # r.set(cache,pickle.dumps(rows))
        taken_time = time.time() - start_time
        print(count,count1)
        
        return render_template("net.html", data1=taken_time,count=count,count1=count1)
    return render_template("net.html")

'''
    loop = request.form['loop']
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("select * from Earthquake where net like ?", (net+'%',))
    rows = cur.fetchall()
    for r1 in rows:
    res.add(r1[11])
    res=list(res)
    for j in res:
    j=j[1:]
    print(j)
    print(res,res[0])
    
    
    
    file = pd.read_csv("./static/all_month.csv")
    net_values = file['net']
    nn = set()
    for i in list(net_values):
    nn.add(i)
    nn = list(nn)
    check = {}
    for i in range(len(nn)):
    h = re.search(r'^a+', nn[i])
    if h:
    print(nn[i])
    check[i] = nn[i]
    print(check)
    #print(random.choice(list(check.keys())), check[random.choice(list(check.keys()))])
    
    start_time = time.time()
    #keyname = 'bye'
    count=0
    count1=0
    
    for i in range(int(loop)):
    net1=random.randint(0,len(res)-1)
    print(net1)
    if (r.exists(keyname+str(net1))):
    rlist = []
    isCache = 'with Cache'
    #print(isCache,mag)
    
    rows = pickle.loads(r.get(keyname+str(net1)))
    count+=1
    else:
    rlist = []
    isCache = 'without Cache'
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("select * from Earthquake where net = ? ", res[net1],)
    rows = cur.fetchall()
    r.set(keyname+str(net1), pickle.dumps(rows))
    count1+=1
    
    con.close()
    taken_time = time.time() - start_time
    print(count,count1)
    '''


def convert_fig_to_html(fig):
    from io import BytesIO
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    import base64
    # figdata_png = base64.b64encode(figfile.read())
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png


@app.route('/cluster', methods=['GET', 'POST'])
def clusters():
    rows = []
    rows1 = []
    if(request.method=="POST"):
        cl=request.form['no_of_clusters']
        
        query = 'SELECT latitude,longitude FROM Earthquake'
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        rows = pd.DataFrame(rows)
        hi = pd.read_csv("./static/all_month.csv")
        #le = preprocessing.LabelEncoder()
        #le.fit(rows.iloc[:,1])
        #rows.iloc[:,1]=le.transform(rows.iloc[:, 1])
        
        #reading = pd.DataFrame(rows)
        rows = rows.dropna()
        k = KMeans(n_clusters=int(cl)).fit(rows)
        centers=k.cluster_centers_
        labels = k.predict(rows)
        #print(labels)
        #fig,ax=plt.subplots()
        plt.xlim([min(rows.iloc[:,0])-10,max(rows.iloc[:,0])])
        plt.ylim([min(rows.iloc[:,1])-10,max(rows.iloc[:,1])])
        
        fig = plt.figure()
        plt.scatter(rows.iloc[:,0],rows.iloc[:,1],c=labels)
        
        plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, marker='+')
        plot = convert_fig_to_html(fig)
        #plt.scatter(hi['mag'], hi['place'],c=5,cmap=plt.cm.Paired)
        #fig.savefig('static/img.png')
        
        #plt.show()
        
        return render_template('cluster1.html', data=centers, data1=plot.decode('utf8'))
    return render_template('cluster1.html')


if __name__ == '__main__':
    app.run()
