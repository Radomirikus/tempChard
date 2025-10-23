import pandas as pd
import requests
from matplotlib import pyplot as plt

def get_coordinates(city_name, country_code):
    url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-postal-code@public/records"
    payload = {
        "limit": 20,
        "where": f"place_name='{city_name}' AND country_code='{country_code}'"
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    if response.json()['total_count'] == 0:
        print("Город не найден")
        exit()
    return response.json()['results'][0]['latitude'], response.json()['results'][0]['longitude']

def get_weather_data(latitude, longitude, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    hourly_data =  response.json()['hourly']
    df = pd.DataFrame({
        'date': hourly_data['time'],
        'temp': hourly_data['temperature_2m']
    })
    df['date'] = pd.to_datetime(df['date'])
  
    return df


def main():
    country_code = "BY"
    city_name = "Minsk"
    start_date = "2024-12-01"
    end_date = "2025-01-10"

    latitude, longitude = get_coordinates(city_name, country_code)
    df = get_weather_data(latitude, longitude, start_date, end_date)
    plt.plot(df['date'], df['temp'])
    plt.xlabel('Даты')
    plt.ylabel('Температуры (°C)')
    plt.title(f'График температуры в {city_name}')
    plt.show()
    
    print(df)

if __name__ == "__main__":
    main()