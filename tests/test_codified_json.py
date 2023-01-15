import codified_json as cjson
import json

# Copy/pasted from the "forecast example" at the bottom of this "weatherapi" website:
# - https://www.weatherapi.com/
json_file = 'tests/weather_forecast.json'
with open(json_file, 'r') as f:
    weather_data = json.load(f)

filename = 'tests/weather_forecast.codf.json'
with open(filename, 'r') as f:
    cjson_str = f.read()


def test_as_str():
    assert cjson.as_str(weather_data) == cjson_str


def test_parse_str():
    assert cjson.parse_str(cjson_str) == weather_data


def test_read_from_file():
    cjson.write_to_file(weather_data, filename)
    assert cjson.read_from_file(filename) == weather_data


def test_read_from_compressed_bytes_file():
    filename_zip = filename + '.gz'
    cjson.write_to_compressed_bytes_file(weather_data, filename_zip)
    assert cjson.read_from_compressed_bytes_file(filename_zip) == weather_data
