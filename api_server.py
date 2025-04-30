from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, Float, String, Text, Boolean, Date, DateTime, Time, LargeBinary, Numeric
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
metadata = MetaData(bind=db.engine)

SQL_TYPE_MAP = {
    'INTEGER': Integer,
    'TEXT': Text,
    'STRING': String,
    'FLOAT': Float,
    'REAL': Float,
    'BOOLEAN': Boolean,
    'DATE': Date,
    'DATETIME': DateTime,
    'TIME': Time,
    'BLOB': LargeBinary,
    'NUMERIC': Numeric
}

def is_valid_identifier(name):
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name)

@app.route('/api/create-table', methods=['POST'])
def create_table():
    data = request.get_json()
    table_name = data.get('table_name')
    columns = data.get('columns')

    if not table_name or not isinstance(columns, list) or len(columns) == 0:
        return jsonify({'error': 'Invalid table definition'}), 400

    if not is_valid_identifier(table_name):
        return jsonify({'error': 'Invalid table name'}), 400

    try:
        if table_name in inspect(db.engine).get_table_names():
            return jsonify({'error': f"Table '{table_name}' already exists"}), 400

        table_columns = [Column('id', Integer, primary_key=True)]
        for col in columns:
            name = col.get('name')
            col_type = col.get('type', '').upper()

            if not name or not col_type:
                return jsonify({'error': 'Each column must have a name and type'}), 400
            if not is_valid_identifier(name):
                return jsonify({'error': f"Invalid column name '{name}'"}), 400
            if col_type not in SQL_TYPE_MAP:
                return jsonify({'error': f"Unsupported column type '{col_type}'"}), 400

            table_columns.append(Column(name, SQL_TYPE_MAP[col_type]))

        table = Table(table_name, metadata, *table_columns)
        table.create()
        return jsonify({'message': f"Table '{table_name}' created successfully"}), 201

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<table_name>', methods=['POST'])
def insert_data(table_name):
    data = request.get_json()
    try:
        table = Table(table_name, metadata, autoload_with=db.engine)
        db.session.execute(table.insert(), [data])
        db.session.commit()
        return jsonify({'message': 'Data inserted successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/<table_name>', methods=['GET'])
def get_data(table_name):
    try:
        table = Table(table_name, metadata, autoload_with=db.engine)
        result = db.session.execute(table.select()).fetchall()
        return jsonify([dict(row) for row in result])
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<table_name>/<int:record_id>', methods=['DELETE'])
def delete_record(table_name, record_id):
    try:
        table = Table(table_name, metadata, autoload_with=db.engine)
        db.session.execute(table.delete().where(table.c.id == record_id))
        db.session.commit()
        return jsonify({'message': f"Record {record_id} deleted"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/<table_name>/<int:record_id>', methods=['PUT'])
def update_record(table_name, record_id):
    data = request.get_json()
    try:
        table = Table(table_name, metadata, autoload_with=db.engine)
        db.session.execute(table.update().where(table.c.id == record_id).values(**data))
        db.session.commit()
        return jsonify({'message': f"Record {record_id} updated"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
