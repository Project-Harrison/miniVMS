from flask import Flask, request, render_template, jsonify
import json
import searoute as sr
from difflib import get_close_matches

app = Flask(__name__)

with open("ports.json") as f:
    ports = json.load(f)

def find_port(city, country=None, cutoff=0.8):
    city = city.lower().strip()
    country = country.lower().strip() if country else None

    for port in ports:
        port_city = port["CITY"].lower().strip()
        port_country = port["COUNTRY"].lower().strip()

        if city in port_city:
            if not country or country in port_country:
                return port
    return None



import folium
from folium.plugins import MarkerCluster

@app.route("/", methods=["GET", "POST"])
def index():
    result1 = result2 = distance = travel_times = None
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

    if request.method == "POST":
        city1 = request.form["city1"]
        country1 = request.form["country1"]
        city2 = request.form["city2"]
        country2 = request.form["country2"]

        match1 = find_port(city1, country1)
        match2 = find_port(city2, country2)

        result1 = json.dumps(match1, indent=2) if match1 else "No match found for Port 1."
        result2 = json.dumps(match2, indent=2) if match2 else "No match found for Port 2."

        if match1 and match2:
            origin = [match1["LONGITUDE"], match1["LATITUDE"]]
            dest = [match2["LONGITUDE"], match2["LATITUDE"]]
            route = sr.searoute(origin, dest, units="naut")

            if route and "geometry" in route:
                coords = [[lat, lon] for lon, lat in route["geometry"]["coordinates"]]
                folium.PolyLine(locations=coords, color="blue", weight=3).add_to(m)

                length_nm = route["properties"]["length"]
                distance = f"{length_nm:.1f} nautical miles"

                travel_times = {}
                for speed in [12, 14, 18]:
                    total_hours = length_nm / speed
                    days = int(total_hours // 24)
                    hours = int(total_hours % 24)
                    travel_times[speed] = f"{days}d {hours}h"

        if match2 and "LATITUDE" in match2 and "LONGITUDE" in match2:
            folium.Marker(
                location=[match2["LATITUDE"], match2["LONGITUDE"]],
                popup="End: " + match2["CITY"]
            ).add_to(m)

    map_html = m._repr_html_()
    return render_template("index.html",
                           result1=result1,
                           result2=result2,
                           map_html=map_html,
                           distance=distance,
                           travel_times=travel_times)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
