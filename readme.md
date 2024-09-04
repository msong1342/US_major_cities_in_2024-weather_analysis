## 10835225 Mingi Song

# Weather Data Analysis

This Python package provides basic functions to analyze weather data and calculate descriptive statistics, including mean, median, mode, and range.

# Dataset

The weather dataset used in this package should contain at least a column named Temperature_C, which stores temperature data in Celsius.

## Functions

- **`open_file(file_name)`**: Reads a CSV file and loads the data into a list.
- **`add_to_weather_data(reader)`**: Appends rows of data to a global list for further analysis.
- **`csv_pandas(file_name)`**: Reads a CSV file into a pandas DataFrame for easier manipulation.
- **`calculate_statistics(df)`**: Calculates the mean, median, mode, and range for temperature data in the provided DataFrame.

## Descriptive Statistics Functions

- **`calculate_mean(data)`**: Returns the mean of the data.
- **`calculate_median(data)`**: Returns the median of the data.
- **`calculate_mode(data)`**: Returns the mode of the data.
- **`calculate_range(data)`**: Returns the range of the data.

# Usage
1. Import the module in your Python code:
```
 import module as module
```
2. Load a CSV file containing weather data and calculate statistics:
```
file_name = 'path_to_your_weather_data.csv'
data_frame = module.csv_pandas(file_name)

if data_frame is not None:
    module.calculate_statistics(data_frame)
```

3. The package will output descriptive statistics for the temperature data, including mean, median, mode, and range.

## Installation

Ensure you have Python installed. You can use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary dependencies:

```bash
pip install pandas
pip install numpy
pip install setuptools

