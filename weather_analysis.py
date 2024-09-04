import module as module
import numpy as np

def calculate_statistics(df):
    """
    Calculate and print statistics for the temperature data in the DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing weather data.

    Returns:
    None
    """
    if 'Temperature_C' in df.columns:
        temp_data = df['Temperature_C']

        mean_temp = np.mean(temp_data)
        median_temp = np.median(temp_data)
        mode_temp = temp_data.mode().iloc[0]  # Mode might return multiple values, we take the first one
        range_temp = np.ptp(temp_data)

        print(f"The mean temperature is {mean_temp:.2f}°C")
        print(f"The median temperature is {median_temp:.2f}°C")
        print(f"The mode of the temperature is {mode_temp:.2f}°C")
        print(f"The range of the temperature is {range_temp:.2f}°C")
    else:
        print("The 'Temperature_C' column is not present in the data.")

if __name__ == "__main__":
    file_name = r"C:\Users\msong\OneDrive\Documents\cs3270\weather_analysis/weather_data.csv"  # Ensure correct path
    data_frame = module.csv_pandas(file_name)
    
    if data_frame is not None:
        calculate_statistics(data_frame)
    else:
        print("DataFrame is None.")