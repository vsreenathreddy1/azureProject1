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


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/new', methods=['POST', 'GET'])
def new():
    row = []
    if request.method == 'POST':
        mag = int(request.form['number'])
        r1= str(mag+86)
        r2= str(mag)
        rows = r2+' + 86='+r1
        if rows != False:
            row.append(rows)
        print(rows)
        return render_template("new.html", data=rows)
    return render_template("new.html")

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
        file.to_sql('qm', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
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

@app.route('/q2search')
def q2search():
    return render_template('q2search.html')

@app.route('/clustering_scatter',methods = ['POST', 'GET'])
def clustering_scatter():
    rows = []
    mainres = []
    n1  = int(request.form["n1"])
    n2  = int(request.form["n2"])
    keyname = 'hii'
    start_time = time.time()
    #mag = "{:.1f}".format(random.uniform(1, 8))
    #mag = round(random.uniform(1, 8),2)
    if (r.exists(keyname)):
        rlist = []
        isCache = 'with Cache'
        print(isCache,keyname)
        
        rows = pickle.loads(r.get(keyname))
        #rlist.append(rows)
        #print(rows)
        #taken_time = time.time() - start_time
        print(time.time() - start_time, isCache)
        #r.delete(str(i))
        
    else:
        rlist = []
        isCache = 'without Cache'
        #start_time = time.time()
        con = sql.connect("database.db")
        cur = con.cursor()
        
        #print(isCache,mag)
        #mag1 = random.uniform(1, 8)
        print("select * from qi where mag between "+ str(n1)+" and "+str(n2))
        cur.execute("select * from qi where mag between "+ str(n1)+" and "+str(n2))
        rows = cur.fetchall();
        r.set(keyname, pickle.dumps(rows))
        con.close()
    taken_time = time.time() - start_time
    return render_template("display.html", data=rows, data1=taken_time, isCache=isCache)

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
        taken_time = time.time() - start_time
        print(count,count1)
        
        return render_template("net.html", data1=taken_time,count=count,count1=count1)
    return render_template("net.html")


@app.route('/q1search')
def q1search():
    return render_template('q1search.html')

@app.route('/q1',methods = ['POST', 'GET'])
def q1():
    lat1 = float(request.form['lat1'])
    lat2 = float(request.form['lat2'])
    net = str(request.form['num'])
    result = []
    lat1_random = lat1
    lat2_random = lat1+1
    
    for i in range(round(lat2)):
        #lat1_random = round(random.uniform(lat1,lat2),2)
        #lat2_random = round(random.uniform(lat1,lat2),2)
        if lat1_random <= lat2:
            query = "select count(*) from Earthquake where net like '"+str(net)+"' and mag between '"+str(lat1_random)+"' and '"+str(lat2_random)+"'"
            con = sql.connect("database.db")
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchone()
            result.append(net)
            result.append(lat1_random)
            result.append(rows)
            lat1_random = lat1_random+1
            lat2_random = lat1_random+1

    
    return render_template("q1result.html",row = result)




@app.route('/rangecsv1', methods=['GET', 'POST'])
def rangecsv1():
    # connect to DB2
    #cur = db2conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name1']
        mag1 = int(request.form['mag1'])
        mag2 = int(request.form['mag2'])
        
        df1 =pd.read_csv('quakes.csv', encoding='latin-1')
        ranges = []
        dfq = df1[df1.net == name]
        dfq = dfq[(dfq.mag > mag1) & (dfq.mag < mag2)]
        for x in range(mag1,mag2):
            ranges.append(x)
    
        dfq = dfq.groupby(pd.cut(dfq.mag, ranges)).count()
        dfq = dfq[['time']]
        rows=[]
        return render_template('rangecsv1.html', ci=[dfq.to_html(classes='data', header="true")])
    return render_template('rangecsv1.html')

@app.route('/pie', methods=['GET', 'POST'])
def rangecsv2():
    
    if request.method == 'POST':
        name = request.form['name1']
        mag1 = int(request.form['mag1'])
        mag2 = int(request.form['mag2'])
        
        df1 =pd.read_csv('quakes.csv', encoding='latin-1')
        
        ranges = []
        dfq = df1[df1.net == name]
        dfq = dfq[(dfq.mag > mag1) & (dfq.mag < mag2)]
        for x in range(mag1,mag2):
            ranges.append(x)
    
        dfm = dfq.groupby(pd.cut(dfq.mag, ranges)).count()
        dfq = dfm[['time']]
        ax = dfm.plot.pie(y='time', figsize=(10, 5))
        ax.get_legend().remove()
        
        plot = convert_fig_to_html(ax)
        rows=[]
        return render_template('rangecsv2.html',data1=plot.decode('utf8'))
    return render_template('rangecsv2.html')


@app.route('/bar', methods=['GET', 'POST'])
def rangecsv3():
    # connect to DB2
    #cur = db2conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name1']
        mag1 = int(request.form['mag1'])
        mag2 = int(request.form['mag2'])
        
        df1 =pd.read_csv('quakes.csv', encoding='latin-1')
        
        ranges = []
        dfq = df1[df1.net == name]
        dfq = dfq[(dfq.mag > mag1) & (dfq.mag < mag2)]
        for x in range(mag1,mag2):
            ranges.append(x)
    
        dfm = dfq.groupby(pd.cut(dfq.mag, ranges)).count()
        dfq = dfm[['time']]
        my_colors = 'rgbkymc'  #red, green, blue, black, etc.
        
        ax = dfq.plot(kind='barh', title ="bar plot", figsize=(15, 10), legend=True, fontsize=12,    color=my_colors)
        plot = convert_fig_to_html(ax)
        rows=[]
        return render_template('rangecsv2.html',data1=plot.decode('utf8'))
    return render_template('rangecsv2.html')




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
        type = str(cl)
        query = 'SELECT latitude,longitude FROM Earthquake'
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        rows = pd.DataFrame(rows)
        #hi = pd.read_csv("./static/all_month.csv")
        #le = preprocessing.LabelEncoder()
        #le.fit(rows.iloc[:,1])
        #rows.iloc[:,1]=le.transform(rows.iloc[:, 1])
        
        #reading = pd.DataFrame(rows)
        rows = rows.dropna()
        #k = KMeans(n_clusters=int(cl)).fit(rows)
        #centers=k.cluster_centers_
        #labels = k.predict(rows)
        #print(labels)
        #fig,ax=plt.subplots()
        #plt.xlim([float(min(rows.iloc[:,0]))-10,float(max(rows.iloc[:,0]))])
        #plt.ylim([float(min(rows.iloc[:,1]))-10,float(max(rows.iloc[:,1]))])
        
        fig = plt.figure()
        #plt.bar(rows.iloc[:,0],rows.iloc[:,1],c=labels)
        #plt.bar(centers[:, 0], centers[:, 1], c='red', s=200, marker='+')
        #plt.bar(rows.iloc[:,0],rows.iloc[:,1])
        #plt.bar(centers[:, 0], centers[:, 1], c='red', s=200, marker='+')
        #plot = convert_fig_to_html(fig)
        #plt.scatter(hi['mag'], hi['place'],c=5,cmap=plt.cm.Paired)
        
        #Cheese, notveg, 6
        #Bread, notveg, 8
        
        #fig.savefig('static/img.png')
        
        
        print (type)
        if type == 'veg':
            print (type)
            labels = 'brocoli', 'Cabbage', 'Coke'
            sizes = [5, 2, 10]
            colors = ['gold', 'yellowgreen', 'lightcoral']
            explode = (0.1, 0, 0)  # explode 1st slice
            plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
            plt.axis('equal')
            plot = convert_fig_to_html(fig)
            return render_template('cluster1.html', data1=plot.decode('utf8'))
        if type == 'notveg':
            labels = 'Cheese', 'Bread'
            sizes = [6, 8]
            colors = ['gold', 'yellowgreen']
            explode = (0, 0)  # explode 1st slice
            plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
            plt.axis('equal')
            plot = convert_fig_to_html(fig)
            return render_template('cluster1.html', data1=plot.decode('utf8'))
                
        # Plot
        #plt.show()
        #plt.show()
        
        
    return render_template('cluster1.html')


if __name__ == '__main__':
    app.run(debug = True)
