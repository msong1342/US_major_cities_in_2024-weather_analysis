import pandas as pd
import module as mod
import logging
import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for plots
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import RFE

# Set up logging
logging.basicConfig(
    filename='weather_analysis.log', 
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s'
)

class WeatherAnalysis:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def fetch_data(self):
        """Fetches and cleans the data from the CSV file."""
        try:
            if os.path.exists(self.file_path):
                fetcher = mod.DataFetcher(self.file_path)
                self.data = fetcher.csv_pandas()

                # Ensure datetime parsing
                self.data['Date_Time'] = pd.to_datetime(self.data['Date_Time'], errors='coerce')

                # Drop rows with missing essential data
                self.data = self.data.dropna(subset=['Temperature_C', 'Date_Time'])

                # Encode categorical 'Location' column as numeric values
                label_encoder = LabelEncoder()
                self.data['Location_Encoded'] = label_encoder.fit_transform(self.data['Location'])

                # Add time-based features
                self.data['month'] = self.data['Date_Time'].dt.month
                self.data['season'] = self.data['month'].apply(lambda x: (x % 12 + 3) // 3)  # 1=Winter, 2=Spring, etc.

                logging.info(f"Data fetched and cleaned successfully from {self.file_path}")
            else:
                raise FileNotFoundError(f"File {self.file_path} does not exist.")
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def print_temperatures(self, limit=10):
        """Print a limited number of temperature records."""
        try:
            for i, temp in enumerate(self.data['Temperature_C'][:limit]):
                print(f"Temperature {i + 1}: {temp:.2f}°C")
            logging.info("Printed temperature records successfully.")
        except Exception as e:
            logging.error(f"Error printing temperatures: {e}")
            raise

    def calculate_statistics(self):
        """Calculate and return statistics for the temperature data."""
        try:
            temp_data = self.data['Temperature_C']
            stats = {
                'mean_temp': round(temp_data.mean(), 2),
                'median_temp': round(temp_data.median(), 2),
                'mode_temp': round(temp_data.mode()[0], 2),
                'range_temp': round(temp_data.max() - temp_data.min(), 2),
            }
            logging.info("Statistics calculated successfully.")
            return stats
        except Exception as e:
            logging.error(f"Error calculating statistics: {e}")
            return {}

    def find_extreme_weather(self):
        """Identify the hottest and coldest days in the dataset."""
        try:
            hottest_day = self.data.loc[self.data['Temperature_C'].idxmax()]
            coldest_day = self.data.loc[self.data['Temperature_C'].idxmin()]
            print(f"Hottest Day: {hottest_day['Date_Time']} with {hottest_day['Temperature_C']:.2f}°C")
            print(f"Coldest Day: {coldest_day['Date_Time']} with {coldest_day['Temperature_C']:.2f}°C")
            logging.info(f"Hottest Day: {hottest_day['Date_Time']} with {hottest_day['Temperature_C']:.2f}°C")
            logging.info(f"Coldest Day: {coldest_day['Date_Time']} with {coldest_day['Temperature_C']:.2f}°C")
        except Exception as e:
            logging.error(f"Error finding extreme weather: {e}")
            raise

    def plot_daily_avg_temp_and_precip(self, save_path="static/daily_avg_temp_precip.png"):
        """Plot daily average temperature and precipitation."""
        try:
            self.data['Date'] = self.data['Date_Time'].dt.date
            daily_data = self.data.groupby('Date').agg(
                avg_temp=('Temperature_C', 'mean'),
                avg_precip=('Precipitation_mm', 'mean')
            )

            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax2 = ax1.twinx()
            ax1.plot(daily_data.index, daily_data['avg_temp'], 'g-', label="Avg Temp (°C)")
            ax2.bar(daily_data.index, daily_data['avg_precip'], color='blue', alpha=0.5, label="Avg Precip (mm)")

            ax1.set_xlabel('Date')
            ax1.set_ylabel('Temperature (°C)', color='green')
            ax2.set_ylabel('Precipitation (mm)', color='blue')
            plt.xticks(rotation=45)

            plt.savefig(save_path, bbox_inches='tight')
            logging.info(f"Saved daily average temperature and precipitation plot to {save_path}")
        except Exception as e:
            logging.error(f"Error plotting daily avg temp and precip: {e}")
            raise

    def plot_temperature_distribution(self, save_path="static/temperature_distribution.png"):
        """Plot temperature distribution as a histogram."""
        try:
            plt.hist(self.data['Temperature_C'], bins=20, color='skyblue', edgecolor='black')
            plt.xlabel('Temperature (°C)')
            plt.ylabel('Frequency')
            plt.title('Temperature Distribution')
            plt.savefig(save_path, bbox_inches='tight')
            logging.info(f"Saved temperature distribution plot to {save_path}")
        except Exception as e:
            logging.error(f"Error plotting temperature distribution: {e}")

    def summarize_by_location(self):
        """Print a summary of average temperature and precipitation for each location."""
        try:
            summary = self.data.groupby('Location').agg(
                avg_temp=('Temperature_C', 'mean'),
                avg_precip=('Precipitation_mm', 'mean')
            ).reset_index()
            print("Location-wise Weather Summary:")
            print(summary)
            logging.info("Location-based summary generated successfully.")
        except Exception as e:
            logging.error(f"Error summarizing by location: {e}")
            raise

    def save_summary(self, output_path="weather_summary.txt"):
        """Save summary statistics to a text file."""
        try:
            with open(output_path, 'w') as f:
                hottest_day = self.data.loc[self.data['Temperature_C'].idxmax()]
                coldest_day = self.data.loc[self.data['Temperature_C'].idxmin()]
                f.write(f"Hottest Day: {hottest_day['Date_Time']} with {hottest_day['Temperature_C']}°C\n")
                f.write(f"Coldest Day: {coldest_day['Date_Time']} with {coldest_day['Temperature_C']}°C\n")
                f.write("\nSummary by Location:\n")
                summary = self.data.groupby('Location').agg(
                    avg_temp=('Temperature_C', 'mean'),
                    avg_precip=('Precipitation_mm', 'mean')
                )
                f.write(summary.to_string())
                print(f"Summary saved to {output_path}")
                logging.info("Summary saved successfully.")
        except Exception as e:
            logging.error(f"Error saving summary: {e}")
            raise

from sklearn.ensemble import RandomForestRegressor
import numpy as np

class WeatherAnalysisImproved(WeatherAnalysis):
    def remove_outliers(self):
        """Remove outliers using the IQR method."""
        try:
            q1 = self.data['Temperature_C'].quantile(0.25)
            q3 = self.data['Temperature_C'].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            self.data = self.data[(self.data['Temperature_C'] >= lower_bound) & 
                                  (self.data['Temperature_C'] <= upper_bound)]
            logging.info("Outliers removed successfully.")
        except Exception as e:
            logging.error(f"Error removing outliers: {e}")
            raise

    def add_features(self):
        """Add lagged and interaction features."""
        try:
            # Lagged features
            self.data['temp_lag_1'] = self.data['Temperature_C'].shift(1)
            self.data['temp_lag_7'] = self.data['Temperature_C'].shift(7)
            
            # Interaction terms
            self.data['humidity_precip_interaction'] = self.data['Humidity_pct'] * self.data['Precipitation_mm']
            
            # Drop rows with NaN due to lagged features
            self.data.dropna(inplace=True)
            logging.info("Lagged and interaction features added successfully.")
        except Exception as e:
            logging.error(f"Error adding features: {e}")
            raise

    def train_predictive_model(self, target_column, feature_columns, city=None, graph_path="static/actual_vs_predicted_rf.png"):
        """Train a Random Forest model and plot Actual vs Predicted values."""
        try:
            if city:
                city_data = self.data[self.data['Location'] == city]
                if city_data.empty:
                    raise ValueError(f"No data available for the city: {city}")
            else:
                city_data = self.data

            # Ensure required columns exist
            if target_column not in city_data.columns or not all(col in city_data.columns for col in feature_columns):
                raise ValueError("Missing required columns in the dataset.")

            # Prepare data
            X = city_data[feature_columns]
            y = city_data[target_column]

            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train the model (Random Forest)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            # Make predictions
            predictions = model.predict(X_test)

            # Evaluate the model
            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            # Align dates with test data
            test_indices = X_test.index
            test_dates = city_data.loc[test_indices, 'Date_Time']

            # Create a results DataFrame for daily averages
            results_df = pd.DataFrame({
                'Date': test_dates.dt.date,
                'Actual': y_test.values,
                'Predicted': predictions
            })
            daily_results = results_df.groupby('Date').mean().reset_index()

            # Plot daily averages
            plt.figure(figsize=(12, 6))
            plt.plot(daily_results['Date'], daily_results['Actual'], label="Actual", color="blue", linestyle='-', marker='o', alpha=0.7)
            plt.plot(daily_results['Date'], daily_results['Predicted'], label="Predicted", color="red", linestyle='--', marker='x', alpha=0.7)
            plt.title(f"Daily Average Actual vs Predicted Temperatures ({city if city else 'All Cities'})")
            plt.xlabel("Date")
            plt.ylabel("Temperature (°C)")
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid(True)
            plt.savefig(graph_path, bbox_inches="tight")
            plt.close()

            logging.info(f"Graph saved at {graph_path}")
            return {
                "model": model,
                "predictions": predictions,
                "mse": mse,
                "r2": r2,
                "actual_vs_predicted": list(zip(y_test, predictions)),
                "graph_path": graph_path
            }
        except Exception as e:
            logging.error(f"Error training predictive model: {e}")
            raise

if __name__ == "__main__":
    file_name = r"C:\Users\msong\OneDrive\Documents\cs3270\weather_analysis_project\weather_data.csv"
    analysis = WeatherAnalysisImproved(file_name)

    try:
        # Fetch data
        analysis.fetch_data()

        # Preprocessing steps
        analysis.remove_outliers()
        analysis.add_features()

        # Analyze the data
        analysis.find_extreme_weather()
        analysis.summarize_by_location()
        stats = analysis.calculate_statistics()
        print("Temperature Statistics:", stats)

        # Train a predictive model
        city = "Chicago"
        results = analysis.train_predictive_model(
            target_column="Temperature_C",
            feature_columns=["Humidity_pct", "Precipitation_mm", "Wind_Speed_kmh", 
                             "Location_Encoded", "month", "season", 
                             "temp_lag_1", "temp_lag_7", "humidity_precip_interaction"],
            city=city
        )

        # Print results
        print(f"Model Evaluation for {city}:")
        print(f"Mean Squared Error (MSE): {results['mse']}")
        print(f"R-squared (R²): {results['r2']}")
        print("Actual vs Predicted:")
        for actual, predicted in results["actual_vs_predicted"][:10]:
            print(f"Actual: {actual:.2f}, Predicted: {predicted:.2f}")

        print(f"Graph saved at: {results['graph_path']}")

    except Exception as e:
        print(f"An error occurred: {e}")
