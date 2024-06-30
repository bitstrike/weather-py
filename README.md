# Weather Forecast and Current Conditions Fetcher

This project is designed to retrieve comprehensive weather information using the National Weather Service API.  It was created with 95.42% AI-generated code. My old mess of a shell script was finally broken by whatever changes were made recently to the NWS API. It had been miraculously running for about a decade so it was time for an upgrade. This upgrade fetches real-time weather data such as temperature, wind speed, humidity, and more based on specific airport codes. Due to the unavailability of current weather conditions directly from the National Weather Service API, data from nearby airports is used for current weather updates. There is a TODO item to include current weather hazards, a feature present in the previous script but not yet implemented here.


1. **Current Weather Conditions and Forecast Retrieval**:
   - **Current Conditions**: "The script fetches real-time weather data such as temperature, wind speed, humidity, and more based on specific airport codes. Immediate weather conditions aren't available from the NWS API is not available, so nearby airport conditions are used instead.
   - **7-Day Weather Forecast**: It provides a detailed forecast spanning seven days for any given ZIP code. This includes hourly and daily weather predictions, covering aspects like temperature trends, precipitation chances, wind direction, and more.

2. **Geocoding ZIP Codes**:
   - The script integrates with the free geocoding API from Map Maker (My Maps Inc) to convert ZIP codes into geographic coordinates (latitude and longitude). This capability is essential for spatial data analysis, mapping, or any application requiring location-based information.

### Features

- **Current Conditions**: Retrieves up-to-date weather data for airports, including temperature, wind speed, humidity, and atmospheric pressure.
- **7-Day Forecast**: Provides detailed weather predictions for the next week, helping users plan activities or travel schedules.
- **Geocoding Support**: Converts ZIP codes into geographic coordinates, facilitating mapping or spatial analysis tasks.
- **Flexible Input Options**: Accepts input via command-line arguments or environment variables, ensuring ease of integration into various workflows.

## Requirements

- Python 3, of some flavor, probably
- `requests` library for making HTTP requests
- `xml.etree.ElementTree` for parsing XML responses

## Installation

Clone the repository and move the script to somewhere in the path

## Usage

Run the script with appropriate command-line arguments or set environment variables for API keys. Environment variables would be more secure as the command below would reveal your
API key to anyone looking over running processes:

```bash
python weather-fetch.py --zip <zip_code> --gc_api_key <maps_co_api_key> --airport <airport_code> [--forecast_only]
```
or, more betterer..
```bash
export GC_API_KEY="abc123xyz456"
export AIRPORT="KOZZ"
export ZIP="93142"

python weather-fetch.py [--forecast_only]
```


### Arguments

- `--zip`: ZIP code of the location for fetching weather forecast.
- `--gc_api_key`: API key for Maps.co Geocoding API (required for geocoding ZIP).
- `--airport`: Airport identifier for fetching current weather conditions.
- `--forecast_only`: Optional flag. If set, only the forecast data will be printed, excluding current conditions.

### Outputs

The script prints the following information:

- Weather Forecast:
  - Update Time
  - Forecast periods (up to 7 days) including start time, end time, temperature, wind speed, and detailed forecast.
  
- Current Conditions:
  - Location
  - Weather conditions (e.g., sunny, rainy)
  - Temperature
  - Wind information (speed, direction)
  - Pressure

### Weather Calculation

The script calculates additional weather metrics like wind chill and humidex based on temperature and wind conditions.

## Functionality

- **geocode_zip(zip_code, api_key)**: Geocodes a ZIP code to retrieve latitude and longitude using the Maps.co Geocoding API.
- **fetch_weather_forecast(zip_code, api_key)**: Fetches the 7-day weather forecast using latitude and longitude from the National Weather Service API.
- **get_current_conditions(airport)**: Fetches the current weather conditions using the airport identifier from the National Weather Service XML API.
- **build_forecast_string(periods)**: Constructs a formatted string representing the weather forecast periods.
- **build_condition_string(current_cond)**: Constructs a delimited string based on the current weather conditions.

## Notes

- Ensure environment variables (`GC_API_KEY`, `ZIP`, `AIRPORT`) are set or provide them via command-line arguments for successful execution.
- Required Python modules (`requests`, `xml.etree.ElementTree`) must be installed for the script to function correctly.
- The script uses janky delimiters for compatibility with an Android app.
- Error handling is implemented for API requests and responses.

- Obtainin the [geocode.maps.co API Key](https://geocode.maps.co/)
    To use the geocoding and reverse geocoding services provided by geocode.maps.co, you need an API key. There are other services you could use, this is just the one I stumbled on.
    Other services may return different formats for the data, but likely they all require signing up for a key
:::
## License

This script is licensed under the GNU General Public License v3.0 (GPL-3.0).