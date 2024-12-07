import pandas as pd
import csv
import logging
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

logging.basicConfig(filename="weather_analysis.log", 
                    level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_app.db'
db = SQLAlchemy(app)

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)

class DataFetcher:
    def __init__(self, file_name):
        self.file_name = file_name

    def csv_pandas(self):
        """Reads a CSV file into a pandas DataFrame."""
        try:
            data_frame = pd.read_csv(self.file_name)
            data_frame.columns = data_frame.columns.str.strip()
            return data_frame
        except Exception as e:
            logging.error(f"Error reading CSV: {e}")
            return None

def populate_database(file_name):
    fetcher = DataFetcher(file_name)
    data_frame = fetcher.csv_pandas()
    if data_frame is not None:
        for _, row in data_frame.iterrows():
            weather_entry = WeatherData(
                location=row['Location'],
                date_time=row['Date_Time'],
                temperature=row['Temperature_C'],
                humidity=row['Humidity_pct'],
                precipitation=row['Precipitation_mm'],
                wind_speed=row['Wind_Speed_kmh']
            )
            db.session.add(weather_entry)
        db.session.commit()
