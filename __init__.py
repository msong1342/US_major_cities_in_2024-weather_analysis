"""
Module1 - Weather Data Analysis
"""
import csv
import pandas as pd

def open_file(file_name):
    """
    Reads a CSV file into a DataFrame.

    Parameters:
    file_name (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The data from the CSV file.
    """
    try:
        data = pd.read_csv(file_name)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_name}' is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file '{file_name}' could not be parsed.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    file_name = "archive (1)\weather_data.csv"
    weather_data = open_file(file_name)

    if weather_data is not None:
        print(f"Number of rows in the dataset: {len(weather_data)}")
