from flask import Flask, render_template, request, jsonify
import json
import requests
from pprint import pprint
import requests_cache
from cassandra.cluster import Cluster
#
cluster = Cluster(['cassandra'])
session = cluster.connect()

requests_cache.install_cache( 'weather_api_cache' , backend= 'sqlite' , expire_after=36000)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
weather_url_template= 'https://api.breezometer.com/weather/v1/current-conditions?lat={latitude}&lon={longitude}&key={Your_API_Key}&metadata=True'





@app.route('/currentweather', methods=['GET'])
def weather():
    MY_Lat= request.args.get ('latitude', '52.379189')
    MY_LON= request.args.get('longitude', '4.899431')
    weather_url = weather_url_template.format(latitude=MY_Lat, longitude= MY_LON,Your_API_Key= app.config['MY_API_KEY'] )
    data={}
    error=[]
    resp=requests.get(weather_url)
    if resp.ok:
        weather = resp.json()
        data['Country'] = weather['metadata']['location']['country']
        data['Temperature'] = weather ['data']['temperature']
        data['Humidity'] = weather ['data']['relative_humidity']
        #pprint(weather)
        #pprint(weather['metadata']['location']['country'])
        #pprint(weather['data']['temperature'])

    else:
        error = (resp.reason)
        print (jsonify(error))
    if len(data)==0:
        return jsonify("There is no City with these coordinates!")
    return (jsonify(data))

@app.route('/city/<city>')
def getcity (city):        
        information = session.execute("""select * From city.stats where city = '{}' ALLOW FILTERING""".format(city))
        #data=[]
        for info in information :
            return('<h1> The {} belongs to {} with the population of {}, latitude {} and longitude {}</h1>'.format(info.city, info.country , info.population,info.lat, info.lng))
        return('<h1> NO CITY FOUND!</h1>')    
                #if info['city'].lower() == city.lower() :
                 #   data.append(info)
       # if len(data)==0:
        #    return jsonify("NO INFORMATION!"), 404
        #return (jsonify(data))

    #for i in weather:
    #    print(weather["metadata"])

if __name__== "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

