from simplejustwatchapi.justwatch import search as justwatch_search
import tmdbsimple as tmdb
from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()
tmdb.API_KEY = getenv('TMDB_API_KEY')
tmdb.REQUESTS_TIMEOUT = 5 

#Función específica para obtener premios
def get_movie_awards_and_scores(movie_title):
    api_key=getenv('OMDB_API_KEY')
    print(f"Buscando awards y scores de: {movie_title}")
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    awards_and_scores={}
    try:
        response = requests.get(url)
        data = response.json()
        #print(f"data: {data}")
        if data.get('Response') == 'True':
            awards_and_scores= {
                'title': data.get('Title'),
                'year': data.get('Year'),
                'awards': data.get('Awards', 'No hay información de premios'),
                'ratings': data.get('Ratings', [])
            }
    except Exception as e:
        print(f"Error al buscar información de premios: {str(e)}")
    return awards_and_scores


def get_trailer_link(id_movie):
    print("Buscando info acerca del trailer")
    #print(f"id_movie (llamada): {id_movie}")
    
    api_key=getenv('TMDB_API_KEY')
    bearer = getenv('BEARER')

    # Define la URL y los encabezados
    url = f'https://api.themoviedb.org/3/movie/{id_movie}/videos?language=en-US'
    #print(f"URL: https://api.themoviedb.org/3/movie/{id_movie}/videos?language=en-US")
    headers = {
        'Authorization': f'Bearer {bearer}',
        'accept': 'application/json',
        'api_key': api_key
    }

    response = requests.get(url, headers=headers)
    link=''

    # Comprueba si la solicitud fue exitosa
    if response.status_code == 200:
        # Convierte la respuesta en formato JSON
        data = response.json()
        #print(f"data: {data}")
        #se obtiene el link al trailer
        for video in data['results']:
            if video['type'] == 'Trailer' and video['official'] == True and video['site'] == 'YouTube':
                link = f"https://www.youtube.com/watch?v={video['key']}"
                #print(link)
                break 
    return link
    #else:
    #    print(f'Error {response.status_code}: {response.text}')


def get_similar_movies(id_movie):
    print("Buscando info acerca de peliculas similares")
    #print(f"id_movie (llamada): {id_movie}")
    
    api_key=getenv('TMDB_API_KEY')

    # Define la URL y los encabezados
    url = f'https://api.themoviedb.org/3/movie/{id_movie}/similar?language=en-US&page=1&api_key={api_key}'
    #print(f"URL: https://api.themoviedb.org/3/movie/762509/similar?language=en-US&page=1&api_key={api_key}")
    headers = {
            'accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    similares=''
    # Comprueba si la solicitud fue exitosa
    if response.status_code == 200:
        data=response.json()
        #print(data)
        for movie in data['results'][:5]:  # Tomar solo los primeros 5 elementos
            title = movie['original_title']
            release_year = movie['release_date'].split('-')[0]  # Tomar solo el año
            print(f"Title: {title}, Year: {release_year}")
            similares += f"Title: {title}, Year: {release_year} ; "

    return similares

#Usa TMDB
def search(movie_name):
    search = tmdb.Search()
    print("antes de buscar en TMDB")
    response = search.multi(query=movie_name, language='es-CL')
    print("despues de buscar en TMDB")

    if not search.results:
        return None
    movie_info=search.results[0]
    print(f"resultados antes: {movie_info}")

    #Agregamos la info de awards y scores al diccionario, buscamos por nombre original
    if 'original_title' in movie_info and movie_info['original_title']:
        print(f"El titulo de la pelicula es: {movie_info['original_title']}")
        # Llamar a la función solo si 'original_title' tiene un valor
        new_info = get_movie_awards_and_scores(movie_info['original_title'])
    
        # Si la función devuelve un diccionario, actualizamos movie_info
        if isinstance(new_info, dict):
            movie_info.update(new_info)
    #movie_info.update(get_movie_awards_and_scores(movie_info['original_title']))

    print(f"El id de la pelicula es: {movie_info['id']}")
    trailer_link=get_trailer_link(movie_info['id'])
    #print(f"trailer_link: {trailer_link}")

    #Obtenemos el link del trailer y los agregamos al diccionario como "trailer_link"
    movie_info['trailer_link'] = trailer_link

    #Obtenemos las peliculas similares y las agregamos al diccionario como "similar_movies"
    similares=get_similar_movies(movie_info['id'])
    movie_info['similar_movies'] = similares

    print(f"resultados post: {movie_info}")
    
    return movie_info

#Usa TMDB
def s_company(company):
    search = tmdb.Search()
    print("antes de buscar en TMDB")
    response = search.company(query=company, language='es-CL')
    print("despues de buscar en TMDB")

    if not search.results:
        return None
    print(f"resultados: {search.results[0]}")
    return search.results[0]

#Usa JUSTWATCH
def search_platforms(movie_name):
    results = justwatch_search(movie_name, "CL", "es")
    platforms = []

    if not results:
        return platforms

    for offer in results[0].offers:
        platforms.append({
            'name': offer.package.name,
            'icon': offer.package.icon,
            'url': offer.url,
        })

    print(f"platforms: {platforms}")
    return platforms