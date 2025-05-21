from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import time 

app = Flask(__name__)
CORS(app)

def get_db_connection():

    retries = 10 
    delay = 5    
    for i in range(retries):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            print(f"Successfully connected to database on attempt {i+1}.")
            return conn
        except mysql.connector.Error as err:
            print(f"Attempt {i+1} to connect to DB failed: {err}")
            if i < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Could not connect to database.")
                raise
try:
    db_connection = get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT
        )
    """)
    db_connection.commit()
    cursor.close()
    db_connection.close() 
except Exception as e:
    print(f"Error during initial database connection or table creation: {e}")
  

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Python API!"})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    if not title:
        return jsonify({"error": "Title is required"}), 400
    conn = get_db_connection() 
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    conn.commit()
    task_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": task_id, "title": title, "description": description}), 201

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection() 
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection() 
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    if task:
        return jsonify(task), 200
    return jsonify({"message": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    if not title and not description:
        return jsonify({"error": "No data provided for update"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if title:
        updates.append("title = %s")
        params.append(title)
    if description:
        updates.append("description = %s")
        params.append(description)
    sql = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s"
    params.append(task_id)
    cursor.execute(sql, tuple(params))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({"message": "Task updated successfully"}), 200
    return jsonify({"message": "Task not found or no changes made"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection() 
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({"message": "Task deleted successfully"}), 200
    return jsonify({"message": "Task not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
