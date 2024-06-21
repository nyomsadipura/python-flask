from flask import Flask, request, jsonify,Response
from model import User
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    db = SQLAlchemy(app)

    # Check if email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email address already exists!'}), 400

    new_user = User(email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    avatar=data['avatar'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.__dict__), 201

@app.route('/users/fetch', methods=['GET'])
def fetch_users():
    page = request.args.get('page', default=1)
    data = request.get_json()
    if data is None :
        return
    id = data['id']
    source_url = 'https://reqres.in/api/users?page='+str(page)
    
    response = requests.get(source_url)
    for u in response['data']:
        if u['id'] == id:
            user = u
            existing_user = User.query.filter_by(integration_id=data['id']).first()
            if existing_user :
                return jsonify({"Messages":"User already exists!","Status":"201"})
            else :
                new_user = User(email=user['email'],
                        first_name=user['first_name'],
                        last_name=user['last_name'],
                        avatar=user['avatar'],
                        integration_id=user['id'])
        else :
            return jsonify({"Messages":"User Not Found","Status":"400"})

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)