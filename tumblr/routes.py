#aqui vão as rotas dos links
import flask

from tumblr import app
from flask import render_template, redirect, url_for
from tumblr import app
from flask import render_template, flash
from flask_login import login_required, login_user, current_user
from tumblr.models import load_user
from tumblr import bcrypt
from tumblr import database
from tumblr.models import User
from tumblr.forms import Register, Login
from tumblr.models import login_manager
from tumblr.forms import FormCreateNewPost
from werkzeug.utils import secure_filename
from tumblr.models import Posts
import os


@app.route('/')

@app.route('/index')
def homepage():
    return render_template('index.html', textinho='Top')


@app.route('/profile/<user_id>', methods=['POST', 'GET'])  # /<batata>')
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        _formCreateNewPost = FormCreateNewPost()

        if _formCreateNewPost.validate_on_submit():
            photo_file = _formCreateNewPost.photo.data
            photo_name = secure_filename(photo_file.filename)

            photo_path = f'{os.path.abspath(os.path.dirname(__file__))}/{app.config["UPLOAD_FOLDER"]}/{photo_name}'
            photo_file.save(photo_path)

            _postText = _formCreateNewPost.text.data

            newPost = Posts(post_Text=_postText, post_image=photo_name, user_id=int(current_user.id))
            database.session.add(newPost)
            database.session.commit()


        return render_template('profile.html', user=current_user, form=_formCreateNewPost)

    else:
        _user = User.query.get(int(user_id))
        return render_template('profile.html', user=user_id, form=None)




#feature 1: postagens
@app.route('/posts')
@login_required
def posts():
    posts = database.session.query(Posts, User).join(User, Posts.user_id == User.id).all()
    return(render_template('posts.html', posts=posts))

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Verifique se o usuário existe
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):  # Implemente a função check_password no modelo User
            login_user(user)
            print(f"Logado com sucesso, {username}!")
            return redirect(url_for('profile', user_id=user.id))  # Redireciona para a página inicial após o login

        else:
            print("Nome de usuário ou senha incorretos")

    return render_template('login.html', form=form)


#feature 2: excluir postagem
@app.route('/delete_post/<post_id>', methods=['POST'])
def delete_post(post_id):
    post = Posts.query.get(post_id)
    database.session.delete(post)
    database.session.commit()

    return redirect(url_for('profile', user_id=current_user.id))


@app.route('/register', methods=['POST', 'GET'])
def createAccount():
    _formCreateNewAccount = Register()


    if _formCreateNewAccount.validate_on_submit():
        password = _formCreateNewAccount.password.data
        password_cr = bcrypt.generate_password_hash(password)

        newUser = User(
            username= _formCreateNewAccount.username.data,
            email= _formCreateNewAccount.email.data,
            password=password_cr
        )

        database.session.add(newUser)
        database.session.commit()
    return render_template('register.html', form=_formCreateNewAccount)



@app.route('/perry')
def perry():
    return render_template('perry.html')

@app.route('/teste')
def teste():
    return render_template('teste.html')