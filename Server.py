from flask import Flask, request, jsonify, abort
import uuid

# Initialisiert die Flask-App
app = Flask(__name__)

# Speichert die Listen und Einträge
todo_lists = []
todo_entries = []

# Middleware, um CORS-Header hinzuzufügen
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Endpunkt zum Abrufen aller To-Do-Listen
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200

# Endpunkt zum Hinzufügen einer neuen Liste
@app.route('/todo-list', methods=['POST'])
def add_list():
    data = request.get_json()
    new_list = {'id': str(uuid.uuid4()), 'name': data['name']}
    todo_lists.append(new_list)
    return jsonify(new_list), 200

# Endpunkt zum Abrufen oder Löschen einer bestimmten Liste
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    todo_list = next((l for l in todo_lists if l['id'] == list_id), None)
    if not todo_list:
        abort(404)
    if request.method == 'GET':
        return jsonify(todo_list), 200
    elif request.method == 'DELETE':
        todo_lists.remove(todo_list)
        return jsonify({'msg': 'success'}), 200

# Endpunkt zum Abrufen aller Einträge einer bestimmten Liste
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_list_entries(list_id):
    entries = [e for e in todo_entries if e['list_id'] == list_id]
    return jsonify(entries), 200

# Endpunkt zum Hinzufügen eines neuen Eintrags zu einer Liste
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    data = request.get_json()
    new_entry = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'description': data.get('description', ''),
        'user_id': data.get('user_id', ''),
        'list_id': list_id
    }
    todo_entries.append(new_entry)
    return jsonify(new_entry), 200

# Endpunkt zum Aktualisieren oder Löschen eines bestimmten Eintrags
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def handle_entry(list_id, entry_id):
    entry = next((e for e in todo_entries if e['id'] == entry_id and e['list_id'] == list_id), None)
    if not entry:
        abort(404)
    if request.method == 'PUT':
        data = request.get_json()
        entry.update({
            'name': data.get('name', entry['name']),
            'description': data.get('description', entry['description'])
        })
        return jsonify(entry), 200
    elif request.method == 'DELETE':
        todo_entries.remove(entry)
        return jsonify({'msg': 'success'}), 200

# Startet den Flask-Server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)