
import json
import requests

def get_weather():
    URL = "http://api.openweathermap.org/data/2.5/weather"
    API_KEY = 'b8bbebfbf8cf7c422f243592dd30be8a'
    CITY = 'seoul'
    UNITS = 'metric'
    LANGUAGE = 'kr'
    params = {'appid': API_KEY, 'q':CITY, 'units': UNITS, 'lang':LANGUAGE}
    res = requests.get(URL, params=params)
    weather_json = res.json()
    

    return weather_json

# print(weather_icon)



def get_genre(weather_id):
    #구름 - 모험
    if weather_id > 800:
        genre_id = 12   
        return genre_id
        
    #맑은날 - 가족
    elif weather_id == 800:
        genre_id = 10751
        return genre_id

    #흐릿 - 미스터리
    elif weather_id >= 700:
        genre_id = 9648
        return genre_id
    
    #눈 - 로맨스
    elif weather_id >= 600:
        genre_id = 10749
        return genre_id
        
    #비 - 스릴러
    elif weather_id >= 500:
        genre_id = 53
        return genre_id
        
    #가랑비 - 드라마
    elif weather_id >= 300:
        genre_id = 18
        return genre_id
        
    #천둥번개 - 공포
    else:
        genre_id = 27
        return genre_id
        