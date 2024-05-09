from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields, ValidationError

app = Flask(__name__)

'''
    For database storage and configuration, I use a separate folder called data
    app
    |----data
    |----|--<database_name>

    Creating the databse, you have to run the following command
    `flask -A app.py --debug run`
    Just change the `app.py` name what your file name
'''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/my_db.db'

db = SQLAlchemy(app)

class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20)) 
    specialisation = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation

    def __repr__(self):
        return '<Author %d>' % self.id

with app.app_context():
    db.create_all()

class AuthorsSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Authors
        load_instances = True
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)

@app.route('/authors', methods = ['GET'])
def index():
    get_authors = Authors.query.all()
    author_schema = AuthorsSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))

@app.route('/authors/<id>', methods = ['GET'])
def get_author_by_id(id):
    get_author = Authors.query.get(id)
    print(get_author)
    author_schema = AuthorsSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author": author}))

@app.route('/authors/<id>', methods = ['PUT'])
def update_author_by_id(id):
    data = request.get_json()
    get_author = Authors.query.get(id)
    if data.get('specialisation'):
        get_author.specialisation = data['specialisation']
    if data.get('name'):
        get_author.name = data['name']

    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorsSchema(only=['id', 'name', 'specialisation'])
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author": author}))

@app.route('/authors/<id>', methods = ['DELETE'])
def delete_author_by_id(id):
    get_author = Authors.query.get(id)
    db.session.delete(get_author)
    db.session.commit()
    return make_response("",204)

@app.route('/authors', methods = ['POST'])
def create_author():
    data = request.get_json()
    # print(data)
    author_schema = AuthorsSchema()
    try:
        # Load data into a dictionary
        author_data = author_schema.load(data)
        # Create an instance of Authors using the loaded data
        author = Authors(**author_data)
        # Add the author instance to the session and commit to the database
        author.create()
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        # Handle validation errors
        return make_response(jsonify({"error": err.messages}), 400)
    result = author_schema.dump(author)
    # print(result)
    return make_response(jsonify({"author": result}),200)

if __name__ == "__main__":
    app.run(debug=True)