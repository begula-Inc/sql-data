from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Функция для подключения к базе данных SQLite
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Чтобы работать с данными как с объектами
    return conn

# Функция для создания таблицы по данным, переданным в теле запроса
def create_table_from_data(table_name, columns):
    conn = get_db()
    cursor = conn.cursor()

    # Строим SQL запрос для создания таблицы
    columns_definition = ", ".join([f"{col['name']} {col['type']}" for col in columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})"
    
    cursor.execute(create_table_query)
    conn.commit()

# Эндпоинт для создания таблицы по данным, переданным в теле запроса
@app.route('/api/create-table', methods=['POST'])
def create_table_api():
    data = request.get_json()  # Получаем данные из тела запроса
    table_name = data.get('table_name')
    columns = data.get('columns')

    # Проверка наличия необходимых данных
    if not table_name or not columns:
        return jsonify({"error": "Table name and columns are required"}), 400

    # Проверка правильности структуры данных
    if not isinstance(columns, list) or len(columns) == 0:
        return jsonify({"error": "Columns should be a non-empty list"}), 400

    for col in columns:
        if 'name' not in col or 'type' not in col:
            return jsonify({"error": "Each column must have 'name' and 'type' fields"}), 400

    # Создаем таблицу на основе данных
    create_table_from_data(table_name, columns)
    return jsonify({"message": f"Table '{table_name}' created successfully."}), 200

# Эндпоинт для получения данных из таблицы (GET)
@app.route('/api/<table_name>', methods=['GET'])
def get_data(table_name):
    conn = get_db()
    cursor = conn.cursor()

    # Получаем все данные из указанной таблицы
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Возвращаем данные в виде JSON
    return jsonify([dict(row) for row in rows])

# Эндпоинт для создания записи в таблице (POST)
@app.route('/api/<table_name>', methods=['POST'])
def create_data(table_name):
    data = request.get_json()
    
    # Получаем ключи и значения для вставки
    columns = ', '.join(data.keys())
    values = ', '.join(['?' for _ in data.values()])
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Выполняем SQL-запрос на вставку данных в таблицу
    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})", tuple(data.values()))
    conn.commit()

    return jsonify({"message": "Data inserted successfully"}), 201

# Эндпоинт для удаления записи из таблицы (DELETE)
@app.route('/api/<table_name>/<int:record_id>', methods=['DELETE'])
def delete_data(table_name, record_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Выполняем SQL-запрос на удаление записи
    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
    conn.commit()
    
    return jsonify({"message": f"Record with ID {record_id} deleted successfully"}), 200

# Эндпоинт для обновления записи в таблице (PUT)
@app.route('/api/<table_name>/<int:record_id>', methods=['PUT'])
def update_data(table_name, record_id):
    data = request.get_json()
    
    # Строим запрос на обновление
    set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Выполняем SQL-запрос на обновление записи
    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = ?", (*data.values(), record_id))
    conn.commit()
    
    return jsonify({"message": f"Record with ID {record_id} updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
