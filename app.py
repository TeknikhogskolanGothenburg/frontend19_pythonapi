import uuid
from passlib.hash import sha256_crypt
from flask import Flask, render_template, jsonify, request, redirect, url_for
from dataaccess.da import get_all_movies, get_movie_by_id, get_movies_partial, does_user_exist, create_user, \
    get_user_password, get_api_key, check_api_key

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html", error=False)

@app.route('/login', methods=["POST"])
def login_done():
    if not does_user_exist(request.form['email']):
        return render_template("login.html", error=True)
    stored_password = get_user_password(request.form['email'])
    if sha256_crypt.verify(request.form["password"], stored_password):
        return redirect(url_for('.profile', email=request.form['email']))
    return render_template("login.html", error=True)

@app.route("/profile", methods=["GET"])
def profile():
    if len(request.args) == 0:
        return render_template('profile.html')
    email = request.args["email"]
    key = get_api_key(email)
    return render_template('profile.html', key=key)

@app.route('/signup', methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route('/signup', methods=["POST"])
def signup_done():
    result = does_user_exist(request.form["email"])
    if result:
        return render_template("api_info.html", uuid='', found=True)
    api_key = uuid.uuid1()
    pwd = sha256_crypt.encrypt(request.form["psw1"])
    create_user(request.form["name"], request.form["email"], api_key, pwd)
    return render_template("api_info.html", uuid=api_key, found=False)


@app.route('/api/v.1.0/movies', methods=["GET"])
def get_movies():
    if not check_api_key(request.headers.get("api_key")):
        return "Wrong or missing api key", 401

    result = get_all_movies()
    return jsonify(result)

@app.route('/api/v.1.0/movies/<int:movie_id>', methods=["GET"])
def get_movie(movie_id):
    if not check_api_key(request.headers.get("api_key")):
        return "Wrong or missing api key", 401
    result = get_movie_by_id(movie_id)
    return jsonify(result)

@app.route('/api/v.1.0/movies/partial', methods=["GET"])
def get_partial():
    if not check_api_key(request.headers.get("api_key")):
        return "Wrong or missing api key", 401
    partial = request.args.get('partial_title', default ='', type=str)
    result = get_movies_partial(partial)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
