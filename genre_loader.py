import sqlite3
import requests
import pprint
import json


apiV3 = '5b8d80b80e618bfd8c5231c61e467b5b'

url = 'https://api.themoviedb.org/3'

type = '/genre/movie/list'

URL = url + type
params = {'api_key': apiV3, 'language':"ko-KR"}
res = requests.get(URL, params=params)
print(res.json())
genre_list = res.json()['genres']
final_list = []

for genre in genre_list:
      single_genre = {"model":"movies.genre"}
      single_genre["fields"] = genre
      final_list.append(single_genre)

with open('genre_data.json', 'w', encoding='UTF-8') as f:
  json.dump(final_list, f,ensure_ascii=False, indent=2)
