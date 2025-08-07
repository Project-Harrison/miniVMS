# miniVMS

A Flask web app that calculates and displays a sea route between two ports.

## Features

* Input two port locations (city + country)
* Matches ports using fuzzy logic
* Calculates sea route and distance using `searoute`
* Displays route on a Folium map
* Shows total nautical miles and estimated travel time at 12, 14, and 18 knots

## Requirements

* Python 3.8+
* `Flask`
* `folium`
* `searoute-py`

## Usage

```bash
pip install -r requirements.txt
python app.py
```

Then visit: `http://localhost:5000`

## Files

* `app.py`: Main Flask app
* `ports.json`: Port data (must include LATITUDE, LONGITUDE, CITY, COUNTRY)
* `templates/index.html`: Frontend template
* `static/`: Optional CSS/JS

## Example Inputs

* City 1: New York
* Country 1: USA
* City 2: Rotterdam
* Country 2: Netherlands


