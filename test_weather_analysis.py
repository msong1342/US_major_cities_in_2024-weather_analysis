import unittest
import os
from unittest.mock import patch
import module as mod
from weather_analysis import WeatherAnalysis

class TestWeatherAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_csv = "temp_weather_data.csv"
        with open(cls.temp_csv, 'w') as f:
            f.write("Temperature_C\n23.5\n22.1\n25.6\n24.2\n23.0\n22.9\n26.1\n")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.temp_csv)

    def test_open_file(self):
        fetcher = mod.DataFetcher(self.temp_csv)
        csv_data = fetcher.open_file()
        self.assertEqual(len(csv_data), 8)

    def test_csv_pandas(self):
        fetcher = mod.DataFetcher(self.temp_csv)
        df = fetcher.csv_pandas()
        self.assertEqual(len(df), 7)
        self.assertEqual(df.iloc[0]["Temperature_C"], 23.5)

    def test_fetch_data(self):
        analysis = WeatherAnalysis(self.temp_csv)
        analysis.fetch_data()
        self.assertIsNotNone(analysis.data)
        self.assertEqual(len(analysis.data), 7)

    def test_temperature_iterator(self):
        analysis = WeatherAnalysis(self.temp_csv)
        analysis.fetch_data()
        temps = list(analysis.temperature_iterator())
        self.assertEqual(temps[0], 23.5)

    def test_print_temperatures(self):
        analysis = WeatherAnalysis(self.temp_csv)
        analysis.fetch_data()
        with patch('builtins.print') as mocked_print:
            analysis.print_temperatures(limit=3)
            mocked_print.assert_any_call("Temperature 1: 23.50°C")
            mocked_print.assert_any_call("Temperature 2: 22.10°C")
            mocked_print.assert_any_call("Temperature 3: 25.60°C")

    def test_calculate_statistics(self):
        analysis = WeatherAnalysis(self.temp_csv)
        analysis.fetch_data()
        with self.assertLogs(level='INFO') as log:
            analysis.calculate_statistics()
            self.assertIn("The mean temperature is", log.output[0])
            self.assertIn("The median temperature is", log.output[0])
            self.assertIn("The mode of the temperature is", log.output[0])
            self.assertIn("The range of the temperature is", log.output[0])

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            analysis = WeatherAnalysis("non_existing_file.csv")
            analysis.fetch_data()

if __name__ == '__main__':
    unittest.main()
