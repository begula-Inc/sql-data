import requests
import json


class APIClient:
    def __init__(self, base_url: str):
        """Инициализация клиента API с базовым URL."""
        self.base_url = base_url.rstrip("/")

    def _handle_response(self, response):
        try:
            data = response.json()
        except ValueError:
            data = response.text
        if response.ok:
            return data
        else:
            print(f"[{response.status_code}] {data}")
            return None

    def create_table(self, table_name: str, columns: list[dict]):
        """Создание таблицы в базе данных через API."""
        url = f"{self.base_url}/create-table"
        data = {
            "table_name": table_name,
            "columns": columns
        }
        try:
            response = requests.post(url, json=data)
            result = self._handle_response(response)
            if result:
                print(f"✅ Table '{table_name}' created.")
        except requests.RequestException as e:
            print(f"Request error: {e}")

    def get_data(self, table_name: str):
        """Получение всех данных из таблицы."""
        url = f"{self.base_url}/{table_name}"
        try:
            response = requests.get(url)
            return self._handle_response(response)
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

    def add_data(self, table_name: str, data: dict):
        """Добавление новой записи в таблицу."""
        url = f"{self.base_url}/{table_name}"
        try:
            response = requests.post(url, json=data)
            result = self._handle_response(response)
            if result:
                print(f"✅ Data added to '{table_name}'.")
        except requests.RequestException as e:
            print(f"Request error: {e}")

    def update_data(self, table_name: str, record_id: int, data: dict):
        """Обновление записи по ID."""
        url = f"{self.base_url}/{table_name}/{record_id}"
        try:
            response = requests.put(url, json=data)
            result = self._handle_response(response)
            if result:
                print(f"✅ Record {record_id} in '{table_name}' updated.")
        except requests.RequestException as e:
            print(f"Request error: {e}")

    def delete_data(self, table_name: str, record_id: int):
        """Удаление записи по ID."""
        url = f"{self.base_url}/{table_name}/{record_id}"
        try:
            response = requests.delete(url)
            result = self._handle_response(response)
            if result:
                print(f"✅ Record {record_id} deleted from '{table_name}'.")
        except requests.RequestException as e:
            print(f"Request error: {e}")
