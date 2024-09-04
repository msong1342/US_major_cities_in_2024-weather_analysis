"""
Module - Weather Data Analysis
"""
import pandas as pd
import csv
import numpy as np

csv_data = []

def open_file(file_name):
    """
    Reads a CSV file into a list.

    Parameters:
    file_name (str): The path to the CSV file.

    Returns:
    list: Data read from the CSV file.
    """
    try:
        with open(file_name, mode="r") as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            add_to_weather_data(data)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def add_to_weather_data(reader):
    """
    Appends each row of CSV data to the csv_data list.

    Parameters:
    reader (csv.reader): CSV reader object.

    Returns: None
    """
    for lines in reader:
        csv_data.append(lines)

def csv_pandas(file_name):
    """
    Reads a CSV file into a DataFrame using pandas.

    Parameters:
    file_name (str): The path to the CSV file.

    Returns:
    pd.DataFrame: Data from the CSV file.
    """
    try:
        data_frame = pd.read_csv(file_name)
        return data_frame
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
    file_name = r"C:\Users\msong\OneDrive\Documents\cs3270\weather_analysis/weather_data.csv"  # Ensure the correct path to your file
    data_frame = csv_pandas(file_name)

