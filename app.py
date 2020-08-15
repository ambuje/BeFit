import requests
import json
from flask import Flask, render_template, request, redirect, url_for, flash
import engine
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as bsa
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = False

@app.route('/')
def index_get():
    return render_template('main.html')

@app.route('/pollution')
def index_pollution():
    return render_template('index.html')

@app.route('/exercise')
def index_exercise():
    return render_template('exercise.html')

@app.route('/exercise1')
def index_exercise1():
    return render_template('ex1.html')
@app.route('/exercise2')
def index_exercise2():
    return render_template('ex2.html')
@app.route('/exercise3')
def index_exercise3():
    return render_template('ex3.html')
@app.route('/meditate')
def index_meditate():
    return render_template('meditate.html')
@app.route('/mapper-template')
def index_mapper_template():
    return render_template('mapper.html')

@app.route('/location<string>',methods=['GET','POST'])
def index_location(string):
    lat,long=string.split(",$,")
    print(lat,long)
    geolocator = Nominatim(user_agent="appl")
    location = geolocator.reverse(lat+", "+ long)
    print(location)
    return "Your Location: "+str(location.address)


@app.route('/map<string>',methods=['GET','POST'])
def index_map(string):
    lat,long,km,mode=string.split(",$,")
    lat,long,km=[float(lat),float(long),int(km)]
    if mode=="walking":
        mode="foot"
    else:
        mode="bike" 
    print(lat,long,km,mode)
    url="https://raw.githubusercontent.com/ambuje/BeFit/master/rawgit"
    r = requests.get(url)
    if r.status_code == 200 :
        html = bsa(r.text,'html.parser');
        html=str(html).strip()
        html=html.split("\n")
        print(html)
    fin_list=html
    temp=fin_list[-1]
    output=['','']
    try:
      output=engine.route((lat,long),km,mode,temp)
    except Exception as e:
        print(e, "ERROR")
        if(len(fin_list)>0):
            fin_list.pop()
            temp=fin_list[-1]
            output=engine.route((lat,long),km,mode,temp)
        
    
    #output=backend.route((lat,long),km,mode,temp)
    out1="".join(str(output[0]).split('?api=1')[1])
    out2=out1.split("&travelmode")
    out2='https://www.google.com/maps/embed/v1/directions?key=AIzaSyAwrCjWGJkvadPAu_A6nP4vRhAqk0oxD8M'+out2[0]+"&mode"+out2[1]
    
    #https://www.google.com/maps/dir/?api=1&origin=29.86308966681687%2C+77.90072298947152&destination=29.86308966681687%2C+77.90072298947152&travelmode=walking&waypoints=29.863089641459847%2C+77.903310487057%7C29.86627908713111%2C+77.9043823800247%7C29.86905659691511%2C+77.9043824209547%7C29.86627908713111%2C+77.9043823800247%7C29.863089641459847%2C+77.903310487057
    return [out2,output[1]]
    #return ['https://www.google.com/maps/embed/v1/directions?key=AIzaSyAwrCjWGJkvadPAu_A6nP4vRhAqk0oxD8M&origin=28.507795599999998%2C+77.2544234&destination=28.507795599999998%2C+77.2544234&mode=walking&waypoints=28.503478888290246%2C+77.26621950592026%7C28.49348379981598%2C+77.27416115517933%7C28.503478888290246%2C+77.26621950592026',]


app.run(port=8000)


'''  
if(len(fin_list)>0):
fin_list.pop()
temp=fin_list[-1]
output=engine.route((lat,long),km,mode,temp)
''' 
