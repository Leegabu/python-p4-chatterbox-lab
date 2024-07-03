from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        return jsonify([{"id": message.id, "body": message.body, "username": message.username} for message in messages])
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(body=data["body"], username=data["username"])
        db.session.add(message)
        db.session.commit()
        return jsonify({"id": message.id, "body": message.body, "username": message.username})

@app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if message is None:
        return jsonify({"error": " Messages is not found"}), 404

    if request.method == 'PATCH':
        data = request.get_json()
        for attr in request.form:
            setattr(message, attr, request.form.get(attr))    
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 200
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

    return jsonify({'deleted': True}), 200

if __name__ == '__main__':
    app.run(port=5555)
