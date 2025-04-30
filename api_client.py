import requests
import json



class APIClient:
    def __init__(self, base_url):
        """Инициализация клиента API с базовым URL."""
        self.base_url = base_url

    # Функция для создания таблицы
    def create_table(self, table_name, columns):
        """Функция для создания таблицы в базе данных через API."""
        url = f"{self.base_url}/create-table"
        data = {
            "table_name": table_name,
            "columns": columns
        }

        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Table '{table_name}' created successfully.")
        else:
            print(f"Failed to create table: {response.json()}")

    # Функция для получения всех данных из таблицы
    def get_data(self, table_name):
        """Функция для получения всех данных из таблицы через API."""
        url = f"{self.base_url}/{table_name}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get data: {response.json()}")
            return None

    # Функция для добавления данных в таблицу
    def add_data(self, table_name, data):
        """Функция для добавления данных в таблицу через API."""
        url = f"{self.base_url}/{table_name}"
        response = requests.post(url, json=data)

        if response.status_code == 201:
            print(f"Data added to '{table_name}' successfully.")
        else:
            print(f"Failed to add data: {response.json()}")

    # Функция для обновления данных в таблице
    def update_data(self, table_name, record_id, data):
        """Функция для обновления данных в таблице через API."""
        url = f"{self.base_url}/{table_name}/{record_id}"
        response = requests.put(url, json=data)

        if response.status_code == 200:
            print(f"Data in record {record_id} updated successfully.")
        else:
            print(f"Failed to update data: {response.json()}")

    # Функция для удаления данных из таблицы
    def delete_data(self, table_name, record_id):
        """Функция для удаления данных из таблицы через API."""
        url = f"{self.base_url}/{table_name}/{record_id}"
        response = requests.delete(url)

        if response.status_code == 200:
            print(f"Record {record_id} deleted from '{table_name}' successfully.")
        else:
            print(f"Failed to delete data: {response.json()}")
