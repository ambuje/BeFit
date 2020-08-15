import requests
import sys
import traceback
import urllib
import gmplot
import json
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point
from haversine import haversine, Unit
import urllib.request,json
import os
from radar import RadarClient




#Tiny URl: To shorten the link
class UrlShortenTinyurl:
    URL = "http://tinyurl.com/api-create.php"

    def shorten(self, url_long):
        try:
            url = self.URL + "?" \
                + urllib.parse.urlencode({"url": url_long})
            res = requests.get(url)
            print("STATUS CODE:", res.status_code)
            print("   LONG URL:", url_long)
            return(res.text)
        except Exception as e:
            raise
#Engine
def route(coorigin,disto,modee,temp):
   #
  import gmplot
  import requests
  import json
  #
  from functools import partial
  import pyproj
  from shapely.ops import transform
  from shapely.geometry import Point
  from haversine import haversine, Unit
  import urllib.request,json
  print("Hello-1")
  try:
      proj_wgs84 = pyproj.Proj(init='epsg:4326')
  except Exception as e:
      print(e)
      
  def geodesic_point_buffer(lat, lon, km):
      # Azimuthal equidistant projection
      aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
      project = partial(
          pyproj.transform,
          pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
          proj_wgs84)
      buf = Point(0, 0).buffer(km * 1000)  # distance in metres
      return transform(project, buf).exterior.coords[:]
    
  def mapsUrlGenerator(origin_loc, waypoints):
      url_ext_origin_loc = origin_loc.replace(',','%2C').replace(' ','+')
      url_ext_waypoints = (("%7C".join(waypoints)).replace(',','%2C')).replace(' ','+')
      if(modee=='foot'):
        maps_url = 'https://www.google.com/maps/dir/?api=1&origin={}&destination={}&travelmode=walking&waypoints={}'.format(url_ext_origin_loc, url_ext_origin_loc, url_ext_waypoints)
      #maps_url = 'https://www.google.com/maps/dir/?api=1&amporigin={}&ampdestination={}&amptravelmode=walking&ampwaypoints={}'.format(url_ext_origin_loc, url_ext_origin_loc, url_ext_waypoints)
      elif(modee=='bike'):
        maps_url = 'https://www.google.com/maps/dir/?api=1&origin={}&destination={}&travelmode=bicycling&waypoints={}'.format(url_ext_origin_loc, url_ext_origin_loc, url_ext_waypoints)

      #print(maps_url)
      return(maps_url)      

      
  #temp='8c5f54ac39174a029f77cd81ae0d707d'
  def get_aqi(lat, lon,temp):
      # try:
      api_url = 'https://api.breezometer.com/air-quality/v2/current-conditions?lat=' +str(lat)+'&lon='+str(lon)+'&key='+temp
      call = requests.get(api_url)
      resp = json.loads(call.text)
      dct = {}
      tempp = resp['data']['indexes']['baqi']
      info = tempp['aqi']
      dct['category'] = tempp['category']
      dct['dom_p'] = tempp['dominant_pollutant']
      return [info]

  def radar_distance(lat1,lng1,lat2,lng2,mode=modee):
    from radar import RadarClient
  # initialize client
    radar = RadarClient('prj_test_pk_d1b12f986cd3ddab0fa4fd6c926742ce32061434')
  #routing
    r = radar.route.distance(origin=[lat1,lng1], destination=[lat2,lng2], modes=mode, units='metric')
    if(mode=='foot'):
      return r.foot.distance.value
    elif(mode=='bike'):
      return r.bike.distance.value

  def f_dist(xx,yy,f1,f2):
    p=float(radar_distance(xx,yy,f1,f2)/1000)
    #print(p)
    return (p)

  #coordinl = coordin.split()
  #print(coorigin)
  x = coorigin[0]
  y = coorigin[1]
  distance=disto/2

  coord = []
  for j in range(4):
      l = (geodesic_point_buffer(x,y,(distance/8)*(j+1)))
      #print((distance/8)*(j+1))
      for i in range(0,len(l)):
          #print(l[i])
          l[i]=l[i][::-1]
          dist=haversine((x,y), l[i])
          l[i]=l[i]+(dist,)
      coord.append(l)
  latitudes=[]
  longitudes=[]
  dist=[]
  for i in coord:
    for j in i:
      lat,log,dis=j
      latitudes.append(lat)
      longitudes.append(log)
      dist.append(dis)
  coord1_lat=[]
  coord2_lat=[]
  coord3_lat=[]
  coord4_lat=[]
  coord1_long=[]
  coord2_long=[]
  coord3_long=[]
  coord4_long=[]
  cnt=0
  for i in latitudes:
    if(cnt<66):
      coord1_lat.append(i)
    if(cnt>=66 and cnt<132):
      coord2_lat.append(i)
    if(cnt>=132 and cnt<198):
      coord3_lat.append(i)
    if(cnt>=198 and cnt<264):
      coord4_lat.append(i)
    cnt=cnt+1
  cnt=0
  for i in longitudes:
    if(cnt<66):
      coord1_long.append(i)
    if(cnt>=66 and cnt<132):
      coord2_long.append(i)
    if(cnt>=132 and cnt<198):
      coord3_long.append(i)
    if(cnt>=198 and cnt<264):
      coord4_long.append(i)
    cnt=cnt+1
  #print(len(coord4_lat))
  aqi_1=[]
  aqi_2=[]
  aqi_3=[]
  aqi_4=[]
  #print(x,y)
  for i in range (0,66):
    aqi_1.append(get_aqi(coord1_lat[i],coord1_long[i],temp))
    aqi_2.append(get_aqi(coord2_lat[i],coord2_long[i],temp))
    aqi_3.append(get_aqi(coord3_lat[i],coord3_long[i],temp))
    aqi_4.append(get_aqi(coord4_lat[i],coord4_long[i],temp))
  a1=(aqi_1.index(max(aqi_1)))
  a2=(aqi_2.index(max(aqi_2)))
  a3=(aqi_3.index(max(aqi_3)))
  a4=(aqi_4.index(max(aqi_4)))
  #print(coord1_lat[a1],coord1_long[a1])
  #print(coord2_lat[a2],coord2_long[a2])
  #print(coord3_lat[a3],coord3_long[a3])
  #print(coord4_lat[a4],coord4_long[a4])
  #print(dist[a1],dist[a2+66],dist[(a3+132)],dist[(a4+198)])
  la=[]
  lo=[]
  final_dis=0
  if(final_dis<distance):
    la.append(coord1_lat[a1])
    lo.append(coord1_long[a1])
    final_dis=final_dis+f_dist(x,y,coord1_lat[a1],coord1_long[a1])
  if(final_dis<distance):
    la.append(coord2_lat[a2])
    lo.append(coord2_long[a2])
    final_dis=final_dis+f_dist(coord1_lat[a1],coord1_long[a1],coord3_lat[a3],coord3_long[a3])
  if(final_dis<distance):
    la.append(coord3_lat[a3])
    lo.append(coord3_long[a3])
    final_dis=final_dis+f_dist(coord1_lat[a3],coord1_long[a3],coord3_lat[a4],coord3_long[a4])
  if(final_dis<distance):
    la.append(coord4_lat[a4])
    lo.append(coord4_long[a4])
    final_dis=final_dis+dist[a2+198]
  gmap = gmplot.GoogleMapPlotter(x,y,16)
  gmap.plot(la, lo, 'cornflowerblue', edge_width=10)
  gmap.scatter(latitudes, longitudes, '#3B0B39', size=40, marker=False)
  gmap.scatter(la, lo, '#3B0B39', size=40, marker=False)

  gmap.draw("templates/mapper.html")
  orig=''
  orig=str(x)+", "+str(y)
  origin_loc = orig
  destin_loc = origin_loc
  waypoints=[]
  a=''
  for i in range(0,len(la)):
    a=str(la[i])+', '+str(lo[i])
    waypoints.append(a)
   # waypoints.append(lo[i])
  cont=0
  for i in reversed(waypoints):
    if(cont==1):
      waypoints.append(i)
    cont=1
  z=mapsUrlGenerator(origin_loc, waypoints)
  
  url_long = z
  
  obj = UrlShortenTinyurl()
  b = obj.shorten(url_long)
        
  print(z,b)
  return [z,b]
