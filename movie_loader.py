import sqlite3
import requests
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)

apiV3 = '5b8d80b80e618bfd8c5231c61e467b5b'

url = 'https://api.themoviedb.org/3'

type = '/movie/popular'

total_movie_list = []
final_list = []

for page_number in range(1,101):

    params = {'api_key': apiV3, 'language':"ko-KR", 'page':page_number}
    URL = url + type
    res = requests.get(URL, params=params)
    movie_list = res.json()['results']
    total_movie_list += movie_list


print(len(total_movie_list))


for movie in total_movie_list:
      single_movie_data = {"model":"movies.movie"}
      single_movie_data["fields"] = movie
      final_list.append(single_movie_data)


with open('movie_data.json', 'w', encoding='UTF-8') as f:
  json.dump(final_list, f,ensure_ascii=False, indent=2)


      



# con = sqlite3.connect('db.sqlite3')
# cur = con.cursor()


# for movie in total_movie_list:
#   cur.execute('''INSERT INTO movies_movie (adult, id, original_language, original_title, overview, popularity, poster_path, release_date, title, video, vote_average, vote_count) VALUES (?, ?, ?, ? , ?, ? ,? , ? , ?, ? , ? , ?)''', (movie["adult"], movie["id"], movie["original_language"], movie["original_title"], movie["overview"], movie["popularity"], movie["poster_path"], movie["release_date"], movie["title"], movie["video"], movie["vote_average"], movie["vote_count"]))
#   for genre in movie['genre_ids']:
#         cur.execute('''INSERT INTO movies_movie_genre_ids (movie_id, genre_id) VALUES(?, ?)''',(movie['id'], genre))

# con.commit()
# con.close()

