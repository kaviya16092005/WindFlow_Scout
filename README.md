# 🌬️ WindFlow Scout

### AI-Powered Global Wind Energy Site Assessment

WindFlow Scout is a web-based application that uses **machine learning and global wind data** to identify and visualize potentially suitable locations for wind energy development.

The application combines **ERA5-based wind data**, a **Random Forest classification model**, and an **interactive geographical map** to help users explore wind conditions and assess the suitability of locations for wind energy projects.

---

## 📌 Project Overview

Selecting a suitable location for a wind energy project requires analyzing several geographical and environmental factors.

WindFlow Scout provides an interactive solution where users can:

* Explore wind conditions across the world
* Select locations directly on an interactive map
* View mean wind speed
* Get AI-based wind energy suitability predictions
* Identify low-suitability locations
* Identify medium-suitability locations
* Identify high-suitability locations
* View latitude and longitude
* Obtain readable geographical location information
* View prediction confidence
* Visually explore potential wind energy regions

---

## 🎯 Objectives

The main objectives of WindFlow Scout are:

1. To develop an AI-based wind energy site assessment system.
2. To use global wind data for geographical analysis.
3. To apply machine learning for wind-site suitability classification.
4. To visualize potential locations using an interactive map.
5. To provide user-friendly location information.
6. To reduce the complexity of interpreting geographical and wind datasets.
7. To provide a foundation for preliminary wind farm site assessment.

---

## ✨ Features

### 🌍 Global Interactive Map

WindFlow Scout provides a world map containing geographical data points.

Users can select a location on the map and view information associated with that location.

### 🌬️ Wind Speed Analysis

The application displays the mean wind speed available for a selected location.

Wind speed is one of the important factors considered during preliminary wind energy site assessment.

### 🤖 Machine Learning Prediction

A **Random Forest Classifier** is used to classify locations according to wind energy suitability.

The model provides:

* Suitability class
* Prediction confidence
* Location-specific information

### 🎨 Suitability Visualization

Locations are represented using different colors:

| Color     | Suitability        |
| --------- | ------------------ |
| 🔴 Red    | Low Suitability    |
| 🟡 Yellow | Medium Suitability |
| 🟢 Green  | High Suitability   |

This allows users to understand the map visually without having to interpret numerical classifications.

### 📍 Location Information

When a user selects a location, the application can display:

* Place name
* Country
* Latitude
* Longitude
* Mean wind speed
* Wind variability, when available
* Elevation, when available
* Slope, when available
* Open-land information, when available
* Suitability classification
* Prediction confidence

---

## 🧠 Machine Learning

WindFlow Scout uses a **Random Forest Classification** model.

Random Forest is an ensemble machine learning algorithm that combines multiple decision trees to produce a classification result.

The model is used to classify wind energy locations into three suitability categories:

```text
0 → Low Suitability
1 → Medium Suitability
2 → High Suitability
```

The trained model is stored as a Python pickle (`.pkl`) file and loaded by the Flask backend.

---

## 🌐 Dataset

The project uses global wind information derived from **ERA5 data**.

The current global ERA5 dataset contains approximately:

```text
114,903 locations
```

The current ERA5 CSV contains:

```text
latitude
longitude
mean_wind_speed
```

Example structure:

| latitude | longitude | mean_wind_speed |
| -------: | --------: | --------------: |
|     90.0 |    -180.0 |             ... |
|    89.75 |   -179.75 |             ... |
|      ... |       ... |             ... |

The dataset is used to provide global geographical coverage for the WindFlow Scout map.

> **Note:** The exact machine-learning features depend on the final trained model and dataset version used in the deployed application.

---

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │      ERA5 Dataset    │
                 │   Global Wind Data   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Data Preprocessing   │
                 │ Cleaning & Formatting│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Random Forest Model  │
                 │  Suitability Class.  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Flask Backend     │
                 │       app.py         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ HTML / CSS / JavaScript│
                 │    Web Interface     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Interactive Map    │
                 │ 🔴 🟡 🟢 Locations   │
                 └──────────────────────┘
```

---

## 🛠️ Technologies Used

### Programming Languages

* Python
* HTML
* CSS
* JavaScript

### Backend

* Flask

### Machine Learning

* Scikit-learn
* Random Forest Classifier
* Joblib / Pickle

### Data Processing

* Pandas
* NumPy

### Mapping

* Interactive web mapping
* Geographical coordinates
* OpenStreetMap-based location information

### Development Environment

* Visual Studio Code
* Python Virtual Environment
* Google Colab for model development

---

## 📂 Project Structure

```text
trustgridai/
│
├── app.py
│
├── requirements.txt
├── Procfile
├── .gitignore
│
├── data/
│   └── WindFlow_Global_ERA5_2024.csv
│
├── model/
│   └── windflow_era5_global_random_forest.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/kaviya16092005/WindFlow_Scout.git
```

Move into the project directory:

```bash
cd WindFlow_Scout
```

---

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

## 🔌 API Endpoints

### Test API

```text
GET /api/test
```

Checks whether the application and machine-learning model are loaded.

Example response:

```json
{
    "status": "WindFlow Scout is running",
    "dataset_rows": 114903,
    "model_loaded": true
}
```

---

### Locations API

```text
GET /api/locations
```

Returns the available geographical locations and their suitability information.

---

### Location Details

```text
GET /api/location/<id>
```

Returns detailed information for a selected dataset location.

Example:

```text
/api/location/100
```

---

### Reverse Geocoding

```text
GET /api/reverse-geocode
```

Converts latitude and longitude into readable geographical information.

Example:

```text
/api/reverse-geocode?lat=13.08&lon=80.27
```

---

### Health Check

```text
GET /health
```

Checks whether the backend and model are operational.

---

## 🖥️ User Workflow

The basic workflow of the application is:

```text
1. Open WindFlow Scout
          ↓
2. Explore the global map
          ↓
3. Select a geographical location
          ↓
4. Retrieve location information
          ↓
5. Analyze wind information
          ↓
6. Run Random Forest prediction
          ↓
7. Display suitability
          ↓
8. Show confidence and location details
```

---

## 📊 Suitability Classification

WindFlow Scout represents the model output using three categories.

### 🔴 Low Suitability

The location is classified as having relatively lower suitability according to the model.

### 🟡 Medium Suitability

The location has moderate suitability according to the model.

### 🟢 High Suitability

The location is classified as having relatively higher suitability according to the model.

These classifications are intended for **preliminary assessment** and should not be treated as a final engineering decision for constructing a wind farm.

---

## 🚀 Deployment

WindFlow Scout can be deployed as a Flask web application using a cloud hosting service.

A typical deployment process is:

```text
GitHub Repository
       ↓
Cloud Web Service
       ↓
Install Python Dependencies
       ↓
Run Gunicorn
       ↓
Flask Application
       ↓
Public Web URL
```

The project includes a `Procfile` for deployment using Gunicorn:

```text
web: gunicorn app:app
```

---

## 🔐 Important Deployment Considerations

Before deployment:

* Make sure the model file is included in the repository or otherwise available to the deployment environment.
* Make sure the dataset path is correct.
* Do not commit passwords, API keys, or other secrets.
* Test the application locally before deployment.
* Avoid sending an excessive number of map requests to external services.
* Reverse geocoding should preferably be performed only when a user selects a location.

---

## 📈 Future Enhancements

Possible future improvements include:

* Real-time weather information
* More detailed wind-resource analysis
* Wind direction visualization
* Wind power density calculation
* Terrain and elevation analysis
* Land-use and protected-area filtering
* Distance from roads and transmission infrastructure
* Advanced geospatial filtering
* Larger and higher-resolution datasets
* Better map clustering for large global datasets
* Mobile-friendly interface
* User-defined site comparison
* Downloadable site assessment reports
* Advanced machine-learning models
* Satellite imagery integration

---

## ⚠️ Limitations

WindFlow Scout is intended primarily as a **preliminary wind energy site assessment tool**.

The prediction should not be considered a substitute for:

* Detailed engineering studies
* On-site wind measurements
* Environmental impact assessments
* Land ownership verification
* Grid connection studies
* Infrastructure analysis
* Financial feasibility studies
* Regulatory approval

Actual wind farm development requires significantly more detailed analysis.

---

## 🎓 Project Applications

WindFlow Scout can be used for:

* Academic projects
* AI/ML demonstrations
* Renewable energy research
* Geospatial data visualization
* Preliminary wind site screening
* Environmental technology projects
* Machine-learning-based geographical analysis

---

## 👩‍💻 Author

**Kaviya Lakshmi**

WindFlow Scout
AI/ML + Geospatial Wind Energy Assessment Project

---

## 📜 License

This project is intended for educational and research purposes.

You may modify and extend the project according to your requirements.

---

## ⭐ Acknowledgements

This project makes use of:

* ERA5 climate/reanalysis data
* Python
* Flask
* Pandas
* NumPy
* Scikit-learn
* OpenStreetMap-based geographical services

---

## 🌬️ WindFlow Scout

**Using AI and global wind data to explore the future of wind energy.**
