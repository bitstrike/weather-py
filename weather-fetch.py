#!/usr/bin/env python3

import argparse
import requests
import os
from xml.etree import ElementTree as ET
import math

class CurrentCond:
    
    def __init__(self, xml_data):
        """
        Initializes a new instance of the CurrentCond class.

        Args:
            xml_data (Element): The XML data containing the current conditions.

        Attributes:
            location              (str): The specific location where the current conditions are observed.
            station_id            (str): The unique identifier for the weather station providing the data.
            latitude              (str): The geographic coordinate representing the north-south position.
            longitude             (str): The geographic coordinate representing the east-west position.
            observation_time      (str): The time when the current weather conditions were observed.
            weather               (str): The current weather conditions (e.g., sunny, rainy, cloudy).
            temperature_string    (str): The temperature represented as a string.
            temp_f                (str): The temperature in Fahrenheit.
            temp_c                (str): The temperature in Celsius.
            relative_humidity     (str): The amount of moisture in the air relative to the maximum amount the air can hold.
            wind_string           (str): Description of the wind speed and direction.
            wind_dir              (str): The compass direction from which the wind is blowing.
            wind_degrees          (str): The direction the wind is coming from in degrees.
            wind_mph              (str): The wind speed in miles per hour.
            wind_kt               (str): The wind speed in knots.
            pressure_string       (str): The atmospheric pressure represented as a string.
            pressure_mb           (str): The atmospheric pressure in millibars.
            pressure_in           (str): The atmospheric pressure in inches of mercury.
            dewpoint_string       (str): The temperature at which air becomes saturated with moisture.
            dewpoint_f            (str): The dewpoint temperature in Fahrenheit.
            dewpoint_c            (str): The dewpoint temperature in Celsius.
            visibility_mi         (str): The visibility in miles.
            icon_url_base         (str): The base URL for weather icon representations.
            icon_url_name         (str): The name of the weather icon.
            ob_url                (str): The URL for the full observation report.
        """
        self.location = xml_data.findtext('location')
        self.station_id = xml_data.findtext('station_id')
        self.latitude = xml_data.findtext('latitude')
        self.longitude = xml_data.findtext('longitude')
        self.observation_time = xml_data.findtext('observation_time')
        self.weather = xml_data.findtext('weather')
        self.temperature_string = xml_data.findtext('temperature_string')
        self.temp_f = xml_data.findtext('temp_f')
        self.temp_c = xml_data.findtext('temp_c')
        self.relative_humidity = xml_data.findtext('relative_humidity')
        self.wind_string = xml_data.findtext('wind_string')
        self.wind_dir = xml_data.findtext('wind_dir')
        self.wind_degrees = xml_data.findtext('wind_degrees')
        self.wind_mph = xml_data.findtext('wind_mph')
        self.wind_kt = xml_data.findtext('wind_kt')
        self.pressure_string = xml_data.findtext('pressure_string')
        self.pressure_mb = xml_data.findtext('pressure_mb')
        self.pressure_in = xml_data.findtext('pressure_in')
        self.dewpoint_string = xml_data.findtext('dewpoint_string')
        self.dewpoint_f = xml_data.findtext('dewpoint_f')
        self.dewpoint_c = xml_data.findtext('dewpoint_c')
        self.visibility_mi = xml_data.findtext('visibility_mi')
        self.icon_url_base = xml_data.findtext('icon_url_base')
        self.icon_url_name = xml_data.findtext('icon_url_name')
        self.ob_url = xml_data.findtext('ob_url')

    def get_temp_as_int(self):
        """
        Returns the temperature as an integer.
        """
        return int(float(self.temp_f))
    
    def get_dew_point_as_int(self):
        """
        Returns the dew point as an integer.
        """
        return int(float(self.dewpoint_f))
    
    def get_humidity_as_int(self):
        """
        Returns the humidity as an integer.
        """
        return int(float(self.relative_humidity))
    
    def get_wind_speed_as_int(self):
        """
        Returns the wind speed as an integer.
        """
        return int(float(self.wind_mph))
    

class WeatherPeriod:
    city = None
    state = None
    forecastZoneURL = None
    forecastZone = None

    def __init__(self, period_data):
        """
        Initializes a new instance of the WeatherPeriod class with the given period data.

        Args:
            period_data (dict): A dictionary containing the data for a weather period.

        Attributes:
            number               (str): The number of the weather period.
            name                 (str): The name of the weather period.
            start_time           (str): The start time of the weather period.
            end_time             (str): The end time of the weather period.
            is_daytime          (bool): Whether the weather period is during the daytime.
            temperature        (float): The temperature of the weather period.
            temperature_unit     (str): The unit of the temperature.
            temperature_trend    (str): The trend of the temperature.
            percip_percent     (float): The probability of precipitation in the weather period.
            wind_speed         (float): The wind speed in the weather period.
            wind_direction       (str): The wind direction in the weather period.
            icon                 (str): The icon representing the weather condition.
            short_forecast       (str): A short forecast for the weather period.
            detailed_forecast    (str): A detailed forecast for the weather period.
        """ 
        self.number = period_data.get('number')
        self.name = period_data.get('name')
        self.start_time = period_data.get('startTime')
        self.end_time = period_data.get('endTime')
        self.is_daytime = period_data.get('isDaytime')
        self.temperature = period_data.get('temperature')
        self.temperature_unit = period_data.get('temperatureUnit')
        self.temperature_trend = period_data.get('temperatureTrend')
        self.percip_percent = period_data.get('probabilityOfPrecipitation', {}).get('value')
        self.wind_speed = period_data.get('windSpeed')
        self.wind_direction = period_data.get('windDirection')
        self.icon = period_data.get('icon')
        self.short_forecast = period_data.get('shortForecast')
        self.detailed_forecast = period_data.get('detailedForecast')

    def get_temp_as_int(self):
        """
        Returns the temperature as an integer.
        """
        return int(self.temperature)
    
    def get_dew_point_as_int(self):
        """
        Returns the dew point as an integer.
        """
        return int(self.dew_point)
   
    def __str__(self):
        """
        Returns a formatted string representation of the object with name, short forecast, temperature, and temperature unit.
        """
        return f"{self.name}: {self.short_forecast}, {self.temperature} {self.temperature_unit}"

def compute_windchill(temp_f, wind_mph):
    """
    Compute wind chill using temperature in Fahrenheit and wind speed in mph.
    Returns 'NA' if conditions don't meet wind chill calculation criteria.
    """
    if temp_f > 50 or wind_mph <= 3:
        return 'NA'
    
    wind_chill = 35.74 + (0.6215 * temp_f) - (35.75 * (wind_mph ** 0.16)) + (0.4275 * temp_f * (wind_mph ** 0.16))
    return round(wind_chill, 1)


def compute_humidex(temp_c, rel_humidity):
    """
    Compute humidex using temperature in Celsius and relative humidity.
    Returns 'NA' if conditions don't meet humidex calculation criteria.
    
    verified here: http://www.csgnetwork.com/canhumidexcalc.html
    temp 39C RH: 87 = 39C
    
    """

    # little risk of heat stress when under 20C or 40% RH, but compute anyway
    # https://www.ohcow.on.ca/resources/apps-tools-calculators/humidex-based-heat-stress-calculator-plan/
    #if temp_c <= 20 or rel_humidity <= 40:
    #    return 'NA'
    
    # Calculate dewpoint
    # https://en.wikipedia.org/wiki/Dew_point#Definition
    a = 17.27 
    b = 237.7 
    alpha = ((a * temp_c) / (b + temp_c)) + math.log(rel_humidity / 100.0)
    dewpoint = (b * alpha) / (a - alpha)
    
    # Calculate humidex
    # https://en.wikipedia.org/wiki/Humidex
    e = 6.11 * math.exp(5417.7530 * ((1 / 273.16) - (1 / (dewpoint + 273.15))))
    humidex = temp_c + 0.5555 * (e - 10.0)
    
    return round(int(humidex), 1)


def geocode_zip(zip_code, api_key):
    """
    Geocodes a ZIP code using the provided API key.

    Parameters:
    - zip_code: The ZIP code to geocode.
    - api_key: The API key for geocoding.

    Returns:
    - Tuple of latitude and longitude if found, otherwise (None, None).
    """
    base_url = f"https://geocode.maps.co/search"
    params = {
        'q': zip_code,
        'api_key': api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Check if data is a list and contains results
        if isinstance(data, list) and len(data) > 0:
            # Assume we take the first result (data[0])
            result = data[0]
            lat = result.get('lat')
            lng = result.get('lon')
            if lat and lng:
                return lat, lng
            else:
                print("Latitude or longitude not found in geocoding response.")
                return None, None
        else:
            print("No results found for the ZIP code.")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geolocation data: {e}")
        return None, None



def fetch_weather_forecast(zip_code, api_key):
    """
    Fetches the weather forecast for a given zip code using the provided API key.

    Args:
        zip_code (str): The zip code for which to fetch the weather forecast.
        api_key (str): The API key for accessing the weather API.

    Returns:
        Tuple[str, List[WeatherPeriod]]: A tuple containing the update time of the forecast and a list of
        WeatherPeriod objects representing the forecast periods. Returns (None, None) if unable to retrieve
        latitude and longitude or if the API response is invalid.

    Raises:
        requests.exceptions.RequestException: If an error occurs while fetching the weather data.
    """
    lat, lng = geocode_zip(zip_code, api_key)
    
    if lat is not None and lng is not None:
        base_url = f"https://api.weather.gov/points/{lat},{lng}"
        try:
            response = requests.get(base_url)
            if response.status_code != 200:
                print (f"Error fetching weather data. site returned: {response.status_code}")
                exit(1)

            response.raise_for_status()
            data = response.json()

            if 'properties' in data:
                forecast_url = data['properties'].get('forecast') 
                WeatherPeriod.forecastZoneURL = data['properties'].get('forecastZone')

                if WeatherPeriod.forecastZoneURL:
                    # get the last portion of the forecastZoneURL which is like this: https://api.weather.gov/zones/forecast/ZYZ063
                    WeatherPeriod.forecastZone = WeatherPeriod.forecastZoneURL.split('/')[-1]
        
                WeatherPeriod.city = data['properties'].get('relativeLocation', {}).get('properties', {}).get('city')
                WeatherPeriod.state = data['properties'].get('relativeLocation', {}).get('properties', {}).get('state')
                

                if forecast_url:
                    forecast_response = requests.get(forecast_url)
                    forecast_response.raise_for_status()
                    forecast_data = forecast_response.json()

                    update_time = forecast_data['properties']['updateTime']
                    periods_data = forecast_data['properties']['periods']

                    periods = [WeatherPeriod(period) for period in periods_data]

                    return update_time, periods
                else:
                    print("No forecast URL found in the API response.")
            else:
                print("Invalid data structure returned from the API.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")

    else:
        print("Unable to retrieve latitude and longitude.")

    return None, None

def get_current_conditions(airport):
    """
    Fetches the current weather conditions for a specific airport.

    Parameters:
        airport (str): The airport code for which to fetch the current conditions.

    Returns:
        CurrentCond: An object representing the current weather conditions for the specified airport.
    """
    base_url = f"https://forecast.weather.gov/xml/current_obs/display.php?stid={airport}"

    try:
        response = requests.get(base_url)
        
        if response.status_code != 200:
            print (f"Error fetching current conditions data. site returned: {response.status_code}")
            exit(1) 

        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        # Create CurrentCond object
        current_cond = CurrentCond(root)

        return current_cond
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current conditions data: {e}")
        return None


def build_forecast_string(periods):
    """
    Builds a forecast string from a list of WeatherPeriod objects which is used .

    Args:
        periods (List[WeatherPeriod]): A list of WeatherPeriod objects representing the forecast periods.

    Returns:
        str: A string representing the forecast in the format "loc:name::short_forecast__,.,___temperature::detailed_forecast;name::short_forecast__,.,___temperature::detailed_forecast;...". If the periods list is empty, an empty string is returned.

    """
    if not periods:
        return ""

    forecast_string = ""
    forecast_details = []
    high_or_low = "High"

    for period in periods:
        # if detailed forecast contains wording "with a low" then high_or_low = "low"
        if "with a low" in period.detailed_forecast:
            high_or_low = "Low"

        # if detailed forecast contains wording "with a high" then high_or_low = "high"            
        elif "with a high" in period.detailed_forecast:
            high_or_low = "High"

           
        details = f"{period.name}:{period.short_forecast}__,.,__{high_or_low}:{period.get_temp_as_int()}__,.,__{period.detailed_forecast}"
        forecast_details.append(details)

    forecast_string += ";".join(forecast_details)

    return forecast_string


def build_condition_string(current_cond):    
    """
    Builds a delimited string based on the current conditions. The janky delimiters are used by an android app which is ancient and I don't want to update it.

    Args:
        current_cond (CurrentCond): The current weather conditions.

    Returns:
        str: The condition string containing the city, state, temperature, dew point, weather conditions, wind direction, wind speed, relative humidity, wind chill, humidex, and forecast.

    """

    # Define a mapping of full attribute names to shortened keys
    key_mapping = {
        'weather': 'cond',
        'wind_dir': 'wdir',
        'wind_mph': 'speed',
        'relative_humidity': 'humid',
        'observation_time': 'obstime'
    }

    # Initialize an empty list to store key-value pairs
    pairs = []

    # Get city and state from WeatherPeriod
    city = WeatherPeriod.city
    state = WeatherPeriod.state

    # Add loc: data for city and state
    pairs.append(f"loc:{city},{state}")

    # add current temp as integer
    pairs.append(f"temp:{current_cond.get_temp_as_int()}")

    # add current dew point as integer
    pairs.append(f"dew:{current_cond.get_dew_point_as_int()}")

    # Iterate through the mapping and add key-value pairs to the list
    for attr, short_key in key_mapping.items():
        value = getattr(current_cond, attr, 'NA')
        if value is not None:
            pairs.append(f"{short_key}:{value}")

    
    # Compute wind chill
    temp_f = float(current_cond.temp_f) if current_cond.temp_f else 0
    wind_mph = float(current_cond.wind_mph) if current_cond.wind_mph else 0
    wind_chill = compute_windchill(temp_f, wind_mph)
    pairs.append(f"chill:{wind_chill}")
  
    # Compute humidex
    temp_c = float(current_cond.temp_c) if current_cond.temp_c else 0
    rel_humidity = float(current_cond.relative_humidity) if current_cond.relative_humidity else 0
    humidex = compute_humidex(temp_c, rel_humidity)
    pairs.append(f"humidx:{humidex}")

    # Add some static values (you may want to replace these with actual data if available)
    static_pairs = [
        'gust:NA',
        'srise:na',
        'sset:na',
        'mrise:na',
        'mset:na',
        'hazard:NA',
        'hazardurl:NA',
        ':FCAST:'
    ]

    # Add the static pairs to the list
    pairs.extend(static_pairs)

    # Concatenate the forecast data
    forecast_string = build_forecast_string(periods)
    pairs.append(forecast_string)

    # Join all pairs with semicolons
    return ';'.join(pairs)


def get_hazards (zone, urgency, severity, certainty):
    """
    see: https://www.weather.gov/documentation/services-web-api

    Fetches the latest hazards for a specified zone.
    
    Args:
        zone (str): The zone code for which to fetch the hazards.
        # curl -X GET "https://api.weather.gov/alerts/active?zone=XYZ001&urgency=Immediate,Expected,Future&severity=Extreme,Severe,Moderate&certainty=Observed,Likely&limit=500
    """

    base_url = f"https://api.weather.gov/alerts/active?zone={zone}&urgency={urgency}&severity={severity}&certainty={certainty}&limit=500"
    try:
        response = requests.get(base_url)
        
        if response.status_code != 200:
            print (f"Error fetching weather data. site returned: {response.status_code}")
            exit(1)

        response.raise_for_status()
        data = response.json()
        
        # hazards are in the 'features' property. return it if it exists
        if 'features' in data:
            return data['features']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch 7-day weather forecast from National Weather Service.")
    parser.add_argument("--zip", required=False, help="ZIP code of the location")
    parser.add_argument("--gc_api_key", required=False, help="API key for Maps.co Geocoding API")
    parser.add_argument("--airport", required=False, help="Airport identifier for current conditions")
    parser.add_argument("--forecast_only", action="store_true", help="If set, only the forecast data will be printed.")
    
    args = parser.parse_args()

    # geocoding requires an API key. If none is provided, try to get it from the environment variables. You should really really use then environment variable.
    if args.gc_api_key is None:
        args.gc_api_key = os.environ.get('GC_API_KEY')
        if args.gc_api_key is None:
            print("GC_API_KEY not found in command line or environment variables.")
            exit(1)

    # If ZIP is not provided, try to get it from the environment variable ZIP
    if args.zip is None:
        args.zip = os.environ.get('ZIP')
        if args.zip is None:
            print("ZIP not found in command line or environment variables.")
            exit(1)

    # If airport is not provided, try to get it from the environment variable AIRPORT
    if args.airport is None:
        args.airport = os.environ.get('AIRPORT')
        if args.airport is None:
            print("AIRPORT not found in command line or environment variables.")
            exit(1)

    # Fetch weather forecast using the provided ZIP code and API key
    update_time, periods = fetch_weather_forecast(args.zip, args.gc_api_key)
     
    # Fetch current conditions using the provided airport and API key
    current_cond = get_current_conditions(args.airport)

    # check if any current weather hazards
    # see: https://www.weather.gov/documentation/services-web-api
    hazards = get_hazards (WeatherPeriod.forecastZone, "Immediate,Expected,Future", "Extreme,Severe,Moderate", "Observed,Likely")
    print(f"Current Hazards: {hazards}")

    # Print weather forecast for debugging or whatever.. if you want only the forecast, use --forecast_only
    if periods:
        if not args.forecast_only:
            print(f"Update Time: {update_time}")
            print(f"Forecast ZoneUrl: {WeatherPeriod.forecastZoneURL}")
            print(f"Forecast Zone: {WeatherPeriod.forecastZone}")
            
            print("Weather Forecast:")
            for period in periods:
                print(f"Number: {period.number}")
                print(f"Name: {period.name}")
                print(f"Start Time: {period.start_time}")
                print(f"End Time: {period.end_time}")
                print(f"Is Daytime: {period.is_daytime}")
                print(f"Temperature: {period.temperature} {period.temperature_unit}")
                print(f"Temperature Trend: {period.temperature_trend}")
                print(f"Probability of Precipitation: {period.percip_percent}")
                print(f"Wind Speed: {period.wind_speed}")
                print(f"Wind Direction: {period.wind_direction}")
                print(f"Icon: {period.icon}")
                print(f"Detailed Forecast: {period.detailed_forecast}")
                print()  # Blank line for separation between periods
    else:
        print("No weather data found.")

    # same here.. use --forecast_only if you want only the forecast
    if current_cond:
        condition_string = build_condition_string(current_cond)
        if not args.forecast_only:
            print (f"current_conditions:")
            print(f"Location: {current_cond.location}")
            print(f"Weather: {current_cond.weather}")
            print(f"Temperature: {current_cond.temperature_string}")
            print(f"Wind: {current_cond.wind_string}")
            print(f"Pressure: {current_cond.pressure_string}")

            attributes = vars(current_cond)
            for attr, value in attributes.items():
                print(f"{attr.replace('_', ' ').title()}: {value}")

        print (condition_string)
    else:
        print("No current conditions data found for the specified airport.")
            
    # finally, spit out the formatted delimited string of weather forecast info so the various scripts querying the web endpoint can use it
    forecast_string = build_forecast_string(periods)
    print(forecast_string)            
    
