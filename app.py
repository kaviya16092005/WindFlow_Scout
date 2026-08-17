from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import joblib
import os
import json
import urllib.request
import urllib.parse

app = Flask(__name__)

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "WindFlow_Global_Complete_2024.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "model",
    "windflow_global_random_forest.pkl"
)

# ==========================================================
# MODEL FEATURES
# ==========================================================

FEATURES = [
    "mean_wind_speed",
    "wind_variability",
    "elevation",
    "slope",
    "open_land"
]

# ==========================================================
# SUITABILITY INFORMATION
# ==========================================================

CLASS_NAMES = {
    0: "Low Suitability",
    1: "Medium Suitability",
    2: "High Suitability"
}

CLASS_COLORS = {
    0: "#ef4444",
    1: "#facc15",
    2: "#22c55e"
}


# ==========================================================
# LOAD DATASET
# ==========================================================

print("\n" + "=" * 60)
print("LOADING GLOBAL WINDFLOW DATASET")
print("=" * 60)

try:

    df = pd.read_csv(DATA_FILE)

    print("Dataset loaded successfully!")
    print("Rows:", len(df))

    print("Columns:")
    print(df.columns.tolist())

except Exception as e:

    print("ERROR loading dataset:")
    print(e)

    df = pd.DataFrame()


# ==========================================================
# CLEAN DATA
# ==========================================================

if not df.empty:

    missing = [
        column
        for column in FEATURES
        if column not in df.columns
    ]

    if missing:

        print("\nMissing model columns:")
        print(missing)

    else:

        for column in FEATURES:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        df["latitude"] = pd.to_numeric(
            df["latitude"],
            errors="coerce"
        )

        df["longitude"] = pd.to_numeric(
            df["longitude"],
            errors="coerce"
        )

        df = df.dropna(
            subset=[
                "latitude",
                "longitude"
            ] + FEATURES
        ).copy()

        print("\nData cleaned successfully!")
        print("Usable rows:", len(df))


# ==========================================================
# LOAD RANDOM FOREST
# ==========================================================

print("\n" + "=" * 60)
print("LOADING GLOBAL RANDOM FOREST MODEL")
print("=" * 60)

try:

    model = joblib.load(MODEL_FILE)

    print(
        "Random Forest model loaded successfully!"
    )

    print(
        "Model type:",
        type(model).__name__
    )

except Exception as e:

    print("ERROR loading model:")
    print(e)

    model = None


# ==========================================================
# PREPARE MAP DATA
# ==========================================================

MAP_POINTS = []

print("\n" + "=" * 60)
print("PREPARING GLOBAL MAP DATA")
print("=" * 60)

if not df.empty and model is not None:

    try:

        X = df[FEATURES].copy()

        print(
            "Running Random Forest prediction for",
            len(X),
            "locations..."
        )

        predictions = model.predict(X)

        probabilities = model.predict_proba(X)

        confidence = (
            np.max(
                probabilities,
                axis=1
            ) * 100
        )

        df["prediction"] = (
            predictions.astype(int)
        )

        df["confidence"] = confidence

        # ==================================================
        # CREATE MAP POINTS
        # ==================================================

        for row in df.itertuples(index=False):

            prediction = int(
                row.prediction
            )

            MAP_POINTS.append({

                "latitude":
                    float(row.latitude),

                "longitude":
                    float(row.longitude),

                "mean_wind_speed":
                    float(row.mean_wind_speed),

                "wind_variability":
                    float(row.wind_variability),

                "elevation":
                    float(row.elevation),

                "slope":
                    float(row.slope),

                "open_land":
                    float(row.open_land),

                "suitable":
                    prediction,

                "class_name":
                    CLASS_NAMES.get(
                        prediction,
                        "Unknown"
                    ),

                "color":
                    CLASS_COLORS.get(
                        prediction,
                        "#808080"
                    ),

                "confidence":
                    round(
                        float(row.confidence),
                        2
                    )
            })

        print(
            "Map points prepared:",
            len(MAP_POINTS)
        )

        print("\nPrediction distribution:")

        print(
            df["prediction"]
            .value_counts()
            .sort_index()
        )

    except Exception as e:

        print(
            "\nERROR preparing map data:"
        )

        print(e)

        MAP_POINTS = []


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================================
# MAP DATA API
# ==========================================================

@app.route("/api/map-data")
def map_data():

    print(
        "\nMap data requested..."
    )

    if not MAP_POINTS:

        return jsonify({

            "success": False,

            "message":
                "No map locations available."

        }), 500

    return jsonify({

        "success": True,

        "count":
            len(MAP_POINTS),

        "points":
            MAP_POINTS

    })


# ==========================================================
# AI PREDICTION API
# ==========================================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
def predict():

    if model is None:

        return jsonify({

            "success": False,

            "message":
                "AI model is not loaded."

        }), 500

    try:

        data = request.get_json()

        mean_wind_speed = float(
            data["mean_wind_speed"]
        )

        wind_variability = float(
            data["wind_variability"]
        )

        elevation = float(
            data["elevation"]
        )

        slope = float(
            data["slope"]
        )

        open_land = float(
            data["open_land"]
        )

        X = pd.DataFrame([{

            "mean_wind_speed":
                mean_wind_speed,

            "wind_variability":
                wind_variability,

            "elevation":
                elevation,

            "slope":
                slope,

            "open_land":
                open_land

        }])

        prediction = int(
            model.predict(X)[0]
        )

        probabilities = model.predict_proba(X)[0]

        confidence = (
            float(
                np.max(probabilities)
            ) * 100
        )

        # Make sure all 3 classes are available
        probability_values = {

            "low": 0,
            "medium": 0,
            "high": 0

        }

        classes = model.classes_

        for i, class_value in enumerate(classes):

            class_value = int(class_value)

            if class_value == 0:

                probability_values["low"] = round(
                    float(probabilities[i] * 100),
                    2
                )

            elif class_value == 1:

                probability_values["medium"] = round(
                    float(probabilities[i] * 100),
                    2
                )

            elif class_value == 2:

                probability_values["high"] = round(
                    float(probabilities[i] * 100),
                    2
                )

        return jsonify({

            "success": True,

            "prediction":
                prediction,

            "class_name":
                CLASS_NAMES.get(
                    prediction,
                    "Unknown"
                ),

            "color":
                CLASS_COLORS.get(
                    prediction,
                    "#808080"
                ),

            "confidence":
                round(
                    confidence,
                    2
                ),

            "probabilities":
                probability_values

        })

    except Exception as e:

        print(
            "Prediction error:",
            e
        )

        return jsonify({

            "success": False,

            "message":
                str(e)

        }), 400


# ==========================================================
# REVERSE GEOCODING
# ==========================================================
#
# This converts:
#
# Latitude + Longitude
#
# into:
#
# City / State / Country
#
# ==========================================================

@app.route(
    "/api/reverse-geocode"
)
def reverse_geocode():

    try:

        lat = request.args.get(
            "lat"
        )

        lon = request.args.get(
            "lon"
        )

        if lat is None or lon is None:

            return jsonify({

                "success": False,

                "message":
                    "Latitude and longitude are required."

            }), 400

        lat = float(lat)

        lon = float(lon)

        # Validate coordinates

        if (
            lat < -90
            or lat > 90
            or lon < -180
            or lon > 180
        ):

            return jsonify({

                "success": False,

                "message":
                    "Invalid coordinates."

            }), 400


        # ==================================================
        # NOMINATIM REQUEST
        # ==================================================

        params = urllib.parse.urlencode({

            "format": "jsonv2",

            "lat": lat,

            "lon": lon,

            "zoom": 10,

            "addressdetails": 1,

            # Ask Nominatim to return English place names.
            "accept-language": "en"

        })


        url = (
            "https://nominatim.openstreetmap.org/reverse?"
            + params
        )


        req = urllib.request.Request(

            url,

            headers={
                "User-Agent":
                    "WindFlowScout/1.0",
                # Prefer English names in the response.
                "Accept-Language": "en"
            }

        )


        with urllib.request.urlopen(
            req,
            timeout=10
        ) as response:

            result = json.loads(
                response.read().decode(
                    "utf-8"
                )
            )


        address = result.get(
            "address",
            {}
        )


        # ==================================================
        # GET PLACE INFORMATION
        # ==================================================

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or address.get("county")
            or "Unknown"
        )


        state = (
            address.get("state")
            or address.get("region")
            or ""
        )


        country = (
            address.get("country")
            or "Unknown"
        )


        country_code = (
            address.get(
                "country_code",
                ""
            ).upper()
        )


        # ==================================================
        # CREATE USER-FRIENDLY NAME
        # ==================================================

        location_parts = []

        if city:
            location_parts.append(
                city
            )

        if state and state != city:
            location_parts.append(
                state
            )

        if country and country != city:
            location_parts.append(
                country
            )


        location_name = ", ".join(
            location_parts
        )


        return jsonify({

            "success": True,

            "city":
                city,

            "state":
                state,

            "country":
                country,

            "country_code":
                country_code,

            "location_name":
                location_name,

            # Return the English city/state/country name.
            # The Nominatim request above explicitly asks for English.
            "display_name":
                location_name

        })


    except Exception as e:

        print(
            "Reverse geocoding error:",
            e
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to find place name."

        }), 500


# ==========================================================
# INFORMATION API
# ==========================================================

@app.route("/api/info")
def info():

    return jsonify({

        "success": True,

        "dataset_rows":
            len(df),

        "map_points":
            len(MAP_POINTS),

        "model_loaded":
            model is not None,

        "features":
            FEATURES

    })


# ==========================================================
# START FLASK
# ==========================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)

    print(
        "             WINDFLOW SCOUT"
    )

    print("=" * 60)

    print(
        "Website:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print("=" * 60)

    app.run(
        debug=True
    )