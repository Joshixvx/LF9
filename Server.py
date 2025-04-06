from flask import Flask, request, jsonify, abort
import uuid

# Initialisiert die Flask-App
app = Flask(__name__)

# Beispiel-IDs für Listen
todo_list_1_id = str(uuid.uuid4())
todo_list_2_id = str(uuid.uuid4())
todo_list_3_id = str(uuid.uuid4())

# Beispiel-Einträge
todo_entry_1 = {'id': str(uuid.uuid4()), 'name': 'Milch', 'description': '', 'list_id': todo_list_1_id}
todo_entry_2 = {'id': str(uuid.uuid4()), 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list_id': todo_list_2_id}
todo_entry_3 = {'id': str(uuid.uuid4()), 'name': 'Kinokarten kaufen', 'description': '', 'list_id': todo_list_3_id}
todo_entry_4 = {'id': str(uuid.uuid4()), 'name': 'Eier', 'description': '', 'list_id': todo_list_1_id}

# Beispiel-Listen & Einträge
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todo_entries = [todo_entry_1, todo_entry_2, todo_entry_3, todo_entry_4]

# Middleware für CORS
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Alle Listen abrufen
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200

# Neue Liste hinzufügen
@app.route('/todo-list', methods=['POST'])
def add_list():
    data = request.get_json(force=True)
    if 'name' not in data:
        return jsonify({'error': 'Missing list name'}), 400
    new_list = {'id': str(uuid.uuid4()), 'name': data['name']}
    todo_lists.append(new_list)
    return jsonify(new_list), 201

# Einzelne Liste abrufen oder löschen
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    todo_list = next((l for l in todo_lists if l['id'] == list_id), None)
    if not todo_list:
        abort(404)
    if request.method == 'GET':
        # Alle Einträge dieser Liste
        entries = [e for e in todo_entries if e['list_id'] == list_id]
        return jsonify(entries), 200
    elif request.method == 'DELETE':
        todo_lists.remove(todo_list)
        # Auch zugehörige Einträge löschen
        global todo_entries
        todo_entries = [e for e in todo_entries if e['list_id'] != list_id]
        return jsonify({'msg': 'List and related entries deleted'}), 200

# Einträge einer Liste abrufen
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_list_entries(list_id):
    entries = [e for e in todo_entries if e['list_id'] == list_id]
    return jsonify(entries), 200

# Eintrag zu einer Liste hinzufügen
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    data = request.get_json(force=True)
    if 'name' not in data:
        return jsonify({'error': 'Missing entry name'}), 400
    new_entry = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'description': data.get('description', ''),
        'user_id': data.get('user_id', ''),
        'list_id': list_id
    }
    todo_entries.append(new_entry)
    return jsonify(new_entry), 201

# Eintrag aktualisieren oder löschen
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def handle_entry(list_id, entry_id):
    entry = next((e for e in todo_entries if e['id'] == entry_id and e['list_id'] == list_id), None)
    if not entry:
        abort(404)
    if request.method == 'PUT':
        data = request.get_json(force=True)
        entry.update({
            'name': data.get('name', entry['name']),
            'description': data.get('description', entry['description'])
        })
        return jsonify(entry), 200
    elif request.method == 'DELETE':
        todo_entries.remove(entry)
        return jsonify({'msg': 'Entry deleted'}), 200

# Startet den Server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
