from api_client import APIClient

# Создаём экземпляр клиента для работы с API

client = APIClient(base_url="http://localhost:5000/api")

# 1. Создание таблицы

columns = [
    {"name": "id", "type": "INTEGER PRIMARY KEY AUTOINCREMENT"},
    {"name": "name", "type": "TEXT"},
    {"name": "age", "type": "INTEGER"},
    {"name": "salary", "type": "REAL"}
]
client.create_table("employees", columns)

# 2. Добавление данных

client.add_data("employees", {"name": "Alice", "age": 30, "salary": 50000.0})
client.add_data("employees", {"name": "Bob", "age": 25, "salary": 45000.0})

# 3. Получение данных

employees = client.get_data("employees")
print("Current employees:", employees)

# 4. Обновление данных

client.update_data("employees", 1, {"name": "Alice Updated", "age": 31, "salary": 55000.0})

# 5. Получение данных после обновления

employees = client.get_data("employees")
print("Updated employees:", employees)

# 6. Удаление данных

client.delete_data("employees", 1)

# 7. Получение данных после удаления

employees = client.get_data("employees")
print("Employees after deletion:", employees)
