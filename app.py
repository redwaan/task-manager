from flask import Flask, request, jsonify
from db import get_db_connection

app = Flask(__name__)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE completed = 0")
    tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

@app.route('/task', methods=['POST'])
def add_task():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, completed) VALUES (%s, %s)", (data['task'], 0))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task added"}), 201

@app.route('/task/<int:id>/complete', methods=['PUT'])
def complete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task completed"})

@app.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

