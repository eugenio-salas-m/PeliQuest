from movies import search, search_platforms, s_company
from openai import OpenAI
from models import User


def build_prompt(user: User, context: str):
    system_prompt = f'''
                    Eres PeliQuest, un chatbot experto en cine, creado para recomendar películas a cinéfilos y profesionales del cine. 
                    Debes proporcionar recomendaciones de manera breve, concisa y especializada, sin repetir nunca las sugerencias. 
                    Debes recordar el nombre del usuario ({user.nombre}), sus géneros preferidos ({user.generos_preferidos}), 
                    sus peliculas favoritas ({user.peliculas_favoritas}) y sus directores favoritos ({user.directores_favoritos}) todo el tiempo.
                    Si tienes links tienes que retornalos siempre.
                    Si tienes imagenes tienes que retornalas siempre.
                    Si encuentras información acerca de scores imdbRating o metascore, retornalos siempre.
                    Si te solicitan el trailer de una pelicula tienes que ir a buscar y usar la información a TMDB. 
                    Si te solicitan películas similares tienes que ir a buscar y usar la información a TMDB. 
                    Si te preguntan por la popularidad de una pelicula tienes que usar la información a TMDB.
                    Si te preguntan por los premios de una pelicula tienes que usar la información a TMDB.
                    Si te solicitan imagenes o posters de peliculas tienes que ir a TMDB a buscarlos y retornar siempre los links EXACTOS a los posters proporcionados por TMDB.
                    Si te solicitan imagenes de compañías productoras tienes que ir a TMDB a buscarlas y retornar siempre los links EXACTOS a las imagenes proporcionadas por TMDB.
                    No puedes inventar ni improvisar datos sobre películas. No puedes inventar imagenes ni links a imagenes. Si no tienes suficiente información, debes solicitar más datos directamente de TMDB.
                    '''

    # Incluir preferencias del usuario
    # if user.generos_preferidos:
    #     system_prompt += f'- El género favorito del usuario es: {user.generos_preferidos}.\n'
    # if user.peliculas_favoritas:
    #     system_prompt += f'- El género a evitar del usuario es: {user.peliculas_favoritas}.\n'
    # if user.directores_favoritos:
    #     system_prompt += f'- El género a evitar del usuario es: {user.directores_favoritos}.\n'

    if context:
        system_prompt += f'Además considera el siguiente contenido: {context}.  Si vienen links a imagenes, retornalos siempre.\n'

    return system_prompt


def where_to_watch(client: OpenAI, search_term: str, user: User):
    movie_or_tv_show = search_platforms(search_term)

    if not movie_or_tv_show:
        return f'No estoy seguro de dónde puedes ver esta película o serie :(, pero quizas puedes revisar en JustWatch: https://www.justwatch.com/cl/buscar?q={search_term}'

    system_prompt = build_prompt(user, str(movie_or_tv_show))

    messages_for_llm = [{"role": "system", "content": system_prompt}]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
        temperature=1,
    )

    return chat_completion.choices[0].message.content

def search_company(client: OpenAI, search_term: str, user: User):
    persona = s_company(search_term)

    system_prompt = build_prompt(user, str(persona))

    messages_for_llm = [{"role": "system", "content": system_prompt}]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
        temperature=1,
    )

    return chat_completion.choices[0].message.content

def search_movie_or_tv_show(client: OpenAI, search_term: str, user: User):
    movie_or_tv_show = search(search_term)

    if movie_or_tv_show:
        system_prompt = build_prompt(user, str(movie_or_tv_show))
    else:
        system_prompt = build_prompt(user, '')

    messages_for_llm = [{"role": "system", "content": system_prompt}]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
        temperature=1,
    )

    return chat_completion.choices[0].message.content