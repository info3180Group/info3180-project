"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file,url_for, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from app.auth_guard import encode_auth_token
from app.forms import *
from app.models import *

from sqlalchemy import func

import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        photo_filename = None
        if form.photo.data:
            photo = form.photo.data
            photo_filename = secure_filename(photo.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True) 
            photo.save(os.path.join(upload_folder, photo_filename))
        new_user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            name=form.name.data,
            email=form.email.data,
            photo=photo_filename
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify(form.errors), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
           
            payload = {
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'photo': user.photo,
                    'date_joined': user.date_joined.isoformat()  
                }
            
            token = encode_auth_token(payload)
            return jsonify({
            'message': 'Login successful',
            'user': payload,
            'token': token
        })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify(form.errors), 400


@app.route('/api/auth/logout', methods=['POST'])
def logout():
   
    return jsonify({'message': 'Logout successful'})
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    profiles = Profile.query.all()
    result = [{
        "id": p.id,
        "user_id_fk": p.user_id_fk,
        "description": p.description,
        "parish": p.parish,
        'biography': p.biography,
        'sex': p.sex,
        'race': p.race,
        'birth_year': p.birth_year,
        'height': p.height,
        'fav_cuisine': p.fav_cuisine,
        'fav_colour': p.fav_colour,
        'fav_school_subject': p.fav_school_subject,
        'political': p.political,
        'religious': p.religious,
        'family_oriented': p.family_oriented

    } for p in profiles]
    return jsonify(result)

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        profile = Profile(
            user_id_fk=form.user_id_fk.data,
            description=form.description.data,
            parish=form.parish.data,
            biography=form.biography.data,
            sex=form.sex.data,
            race=form.race.data,
            birth_year=form.birth_year.data,
            height=form.height.data,
            fav_cuisine=form.fav_cuisine.data,
            fav_colour=form.fav_colour.data,
            fav_school_subject=form.fav_school_subject.data,
            political=form.political.data,
            religious=form.religious.data,
            family_oriented=form.family_oriented.data
        )
        db.session.add(profile)
        db.session.commit()
        return jsonify({'message': 'Profile created successfully'}), 201
    return jsonify(form.errors), 400

@app.route('/api/profiles/<int:user_id>', methods=['DELETE'])
def delete_profile(user_id):
    profiles = Profile.query.filter_by(user_id_fk=user_id).all()
    if not profiles:
        return jsonify({'message': 'Profile not found'}), 404
    for profile in profiles:
        db.session.delete(profile)
    db.session.commit()
    return jsonify({'message': 'Profile(s) deleted successfully'}), 200

@app.route('/api/profile/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = Profile.query.filter_by(id=profile_id).first()
    if not profile:
        return jsonify({'message': 'Profile not found'}), 404
    result = {
        "id": profile.id,
        "user_id_fk":  profile.user_id_fk,
        "description":  profile.description,
        "parish":  profile.parish,
        'biography': profile.biography,
        'sex': profile.sex,
        'race': profile.race,
        'birth_year': profile.birth_year,
        'height': profile.height,
        'fav_cuisine': profile.fav_cuisine,
        'fav_colour': profile.fav_colour,
        'fav_school_subject': profile.fav_school_subject,
        'political': profile.political,
        'religious': profile.religious,
        'family_oriented': profile.family_oriented
      
    } 
    return jsonify(result)

@app.route('/api/profiles/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
  
    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404

   
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    
    profile.description = data.get('description', profile.description)
    profile.parish = data.get('parish', profile.parish)
    profile.biography = data.get('biography', profile.biography)
    profile.sex = data.get('sex', profile.sex)
    profile.race = data.get('race', profile.race)
    profile.birth_year = data.get('birth_year', profile.birth_year)
    profile.height = data.get('height', profile.height)
    profile.fav_cuisine = data.get('fav_cuisine', profile.fav_cuisine)
    profile.fav_colour = data.get('fav_colour', profile.fav_colour)
    profile.fav_school_subject = data.get('fav_school_subject', profile.fav_school_subject)
    profile.political = data.get('political', profile.political)
    profile.religious = data.get('religious', profile.religious)
    profile.family_oriented = data.get('family_oriented', profile.family_oriented)

    
    db.session.commit()

    
    return jsonify({
        'message': 'Profile updated successfully',
        'profile': {
            'id': profile.id,
            'user_id_fk': profile.user_id_fk,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented
        }
    })



@app.route('/api/profiles/<int:fav_user_id>/favourite', methods=['POST'])
def favourite_profile(fav_user_id):
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    if user_id == fav_user_id:
        return jsonify({'error': 'Cannot favourite your own profile'}), 400

   
    profile = User.query.get(fav_user_id)
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404


    existing_favourite = Favourite.query.filter_by(user_id_fk=user_id, fav_user_id_fk=fav_user_id).first()
    if existing_favourite:
        return jsonify({'message': 'Already favourited'}), 200

  
    new_favourite = Favourite(user_id_fk=user_id, fav_user_id_fk=fav_user_id)
    db.session.add(new_favourite)
    db.session.commit()

    return jsonify({'message': 'Profile favourited successfully'}), 201


@app.route('/api/search', methods=['GET'])
def search_profiles():
    name = request.args.get('name')
    birth_year = request.args.get('birth_year')
    sex = request.args.get('sex')
    race = request.args.get('race')

   
    query = db.session.query(Profile, User).join(User, Profile.user_id_fk == User.id)

  
    if name:
        query = query.filter(User.name.ilike(f'%{name}%'))  
    if birth_year:
        query = query.filter(Profile.birth_year == int(birth_year))
    if sex:
        query = query.filter(Profile.sex == sex)
    if race:
        query = query.filter(Profile.race.ilike(f'%{race}%'))

    results = query.all()

    profiles_list = []
    for profile, user in results:
        profiles_list.append({
            'profile_id': profile.id,
            'user_id': user.id,
            'name': user.name,
            'email': user.email,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented
        })

    return jsonify({'results': profiles_list})

@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
def get_matches(profile_id):

    base_profile = Profile.query.get(profile_id)
    if not base_profile:
        return jsonify({'error': 'Profile not found'}), 404

   
    matches = Profile.query.filter(
        Profile.id != base_profile.id,  
        Profile.parish == base_profile.parish,
        Profile.fav_cuisine == base_profile.fav_cuisine,
        Profile.birth_year.between(base_profile.birth_year - 5, base_profile.birth_year + 5)
    ).all()
    matches_data = []
    for match in matches:
        matches_data.append({
            'id': match.id,
            'user_id_fk': match.user_id_fk,
            'description': match.description,
            'parish': match.parish,
            'biography': match.biography,
            'sex': match.sex,
            'race': match.race,
            'birth_year': match.birth_year,
            'height': match.height,
            'fav_cuisine': match.fav_cuisine,
            'fav_colour': match.fav_colour,
            'fav_school_subject': match.fav_school_subject,
            'political': match.political,
            'religious': match.religious,
            'family_oriented': match.family_oriented
        })

    return jsonify({'matches': matches_data})


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_data = {
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'photo': user.photo,
        'date_joined': user.date_joined.isoformat()  
    }

    return jsonify({'user': user_data})


@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):

    favourites = Favourite.query.filter_by(user_id_fk=user_id).all()

    if not favourites:
        return jsonify({'message': 'No favourites found'}), 404

    fav_users_list = []
    for fav in favourites:
        fav_user = User.query.get(fav.fav_user_id_fk)
        if fav_user:
            fav_users_list.append({
                'id': fav_user.id,
                'username': fav_user.username,
                'name': fav_user.name,
                'email': fav_user.email,
                'photo': fav_user.photo
            })

    return jsonify({'favourites': fav_users_list})




@app.route('/api/users/favourites/<int:n>', methods=['GET'])
def get_top_favoured_users(n):
  
    fav_counts = db.session.query(
        Favourite.fav_user_id_fk,
        func.count(Favourite.id).label('fav_count')
    ).group_by(Favourite.fav_user_id_fk).order_by(func.count(Favourite.id).desc()).limit(n).all()

    top_users = []
    for fav_user_id, fav_count in fav_counts:
        user = User.query.get(fav_user_id)
        if user:
            top_users.append({
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'photo': user.photo,
                'favoured_count': fav_count
            })

    return jsonify({'top_favoured_users': top_users})


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404