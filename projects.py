import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://admin:admin@cluster0.24xbm.mongodb.net/sravyaProjects?retryWrites=true&w=majority',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class Project(db.Document):
    name = db.StringField()
    duration = db.StringField()
    technology_stack = db.StringField()
    description = db.StringField()
    def to_json(self):
        return {"name": self.name,
                "duration": self.duration,
                "technology_stack": self.technology_stack,
                "description":self.description}

@app.route('/get-all-projects', methods=['GET'])
def get_all_projects():
    project = Project.objects()
    if not project:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(project)

@app.route('/', methods=['GET'])
def get_project():
    name = request.args.get('name')
    project = Project.objects(name=name).first()
    if not project:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(project.to_json())

@app.route('/add-project', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    project = Project(name=record['name'],
                duration=record['duration'],
                technology_stack = record['technology_stack'],
                description = record['description'])
    project.save()
    return jsonify(project.to_json())

@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    project = Project.objects(name=record['name']).first()
    if not project:
        return jsonify({'error': 'data not found'})
    else:
        project.delete()
    return jsonify(project.to_json())

if __name__ == "__main__":
    app.run(debug=True)