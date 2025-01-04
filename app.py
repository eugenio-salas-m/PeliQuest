from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message

load_dotenv()

client = OpenAI()
app = Flask(__name__)
bootstrap = Bootstrap5(app)
db_config(app)


@app.route('/')
def index():
    return render_template('landing.html')



@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user = db.session.query(User).first()
    nombre = user.nombre or ""
    user_id  = user.id or 1
    generos_preferidos = user.generos_preferidos or ""
    peliculas_favoritas = user.peliculas_favoritas or ""
    directores_favoritos = user.directores_favoritos or ""


    if request.method == 'GET':
        return render_template('chat.html', messages=user.messages, nombre=nombre, generos_preferidos=generos_preferidos, peliculas_favoritas=peliculas_favoritas, directores_favoritos=directores_favoritos, user_id=user_id)

    intent = request.form.get('intent')
    user_message = request.form.get('message');
    if user_message == "":
        user_message = intent

    # Guardar nuevo mensaje en la BD
    db.session.add(Message(content=user_message, author="user", user=user))
    db.session.commit()

    messages_for_llm = [{
        "role": "system",
        "content": f"Eres PeliQuest, un chatbot experto en cine, creado para recomendar películas a cinéfilos y profesionales del cine. Debes proporcionar recomendaciones de manera breve, concisa y especializada, sin repetir nunca las sugerencias. Debes recordar el nombre del usuario ({user.nombre}), sus géneros preferidos ({generos_preferidos}), sus peliculas favoritas ({peliculas_favoritas}) y sus directores favoritos ({directores_favoritos}) todo el tiempo.",
    }]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
        temperature=1
    )

    model_recommendation = chat_completion.choices[0].message.content
    db.session.add(Message(content=model_recommendation, author="assistant", user=user))
    db.session.commit()

    return render_template('chat.html', messages=user.messages, nombre=nombre, generos_preferidos=generos_preferidos, peliculas_favoritas=peliculas_favoritas, directores_favoritos=directores_favoritos, user_id=user_id)


@app.route('/user/<username>')
def user(username):
    user = db.session.query(User).first()
    nombre = user.nombre or ""
    generos_preferidos = user.generos_preferidos or ""
    peliculas_favoritas = user.peliculas_favoritas or ""
    directores_favoritos = user.directores_favoritos or ""

    favorite_movies = peliculas_favoritas.split(",")
    return render_template('user.html', username=username, favorite_movies=favorite_movies)


@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = db.session.query(User).get(id)
    
    if request.method == 'POST':
        if user:
            # Se actualizan los campos con los datos enviados desde el formulario
            user.nombre = request.form['nombre']
            user.email = request.form['email']
            user.generos_preferidos = request.form['generos_preferidos'].lower()
            user.peliculas_favoritas = request.form['peliculas_favoritas'].lower()
            user.directores_favoritos = request.form['directores_favoritos'].lower()
            
            # Guardan los cambios en la base de datos
            db.session.commit()
            
            # Se redirige de nuevo a la misma página con un mensaje de éxito como parámetro en la URL
            return redirect(url_for('update_user', id=id, success='Información del usuario fue actualizada'))
        
        else:
            return redirect(url_for('update_user', id=id, error='Usuario no encontrado'))

    # Si es GET, mostramos el formulario con los datos del usuario
    return render_template('update_user.html', user=user)
