import  json

from flask import Flask, jsonify, render_template, request, jsonify, make_response, session
from flask_cors import CORS
from flaskwebgui import FlaskUI #get the FlaskUI class

import geopandas as gpd

from mapfile import WaspVectorMap

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = "secret_key"
ui = FlaskUI(app)
layers = {}

@app.route("/new_map")
def new_map():
    try:
        layers["rugo_map"]  = gpd.GeoDataFrame(
            columns=["id", "l_rough", "r_rough", "elevation", "geometry"], 
            geometry="geometry", 
            crs=4326)
        return jsonify({"succes": True}) 
    except:
        return jsonify({"succes": False})

# @app.route("/add_polygon")
# def add_polygon():


# @app.route("/update_polygon")
# def update_polygon():
#     return None
# @app.route("/delete_polygon")
# def delete_polygon():
#     return None

@app.route('/open_map')
def open_map(): 
    rugo_map = WaspVectorMap.from_file(
        request.args.get("path", None, type=str),
        map_type=1,
        reproj={"from_epsg": 2154}
    )
    rugo_map.reproj(overwrite=True) 
    # response = jsonify(rugo_map.to_geojson())
    # response.headers.add('Access-Control-Allow-Origin', '*')
    layers['rugo_map'] = rugo_map #.to_geodataframe()
    return jsonify(rugo_map.to_geojson())

@app.route('/export')
def export_map():
    dest_epsg = request.args.get("dest_epsg", None, type=int)
    if "rugo_map" in layers.keys() :
        layers['rugo_map'].reproj(to_epsg=dest_epsg, overwrite=True)
        layers['rugo_map'].to_mapfile("souvans_from_firefox.map")
        response =  jsonify({"result": True})
        response.headers.add('Access-Control-Allow-Origin', '*')
    else:
        response = jsonify({"result": False})
    return response

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    ui.run()
    #app.run(debug=True)