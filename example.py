from api_client import APIClient

# Создаём экземпляр клиента для работы с API
client = APIClient(base_url="http://localhost:5000/api")

# 1. Создание таблицы с несколькими типами данных и внешними ключами

columns = [
    {"name": "id", "type": "INTEGER PRIMARY KEY AUTOINCREMENT"},
    {"name": "name", "type": "TEXT"},
    {"name": "age", "type": "INTEGER"},
    {"name": "salary", "type": "REAL"},
    {"name": "department_id", "type": "INTEGER"},
    {"name": "created_at", "type": "DATETIME"}
]
client.create_table("employees", columns)

# Создадим таблицу для департаментов с внешним ключом
department_columns = [
    {"name": "id", "type": "INTEGER PRIMARY KEY AUTOINCREMENT"},
    {"name": "name", "type": "TEXT"}
]
client.create_table("departments", department_columns)

# 2. Добавление данных

# Добавляем департамент
client.add_data("departments", {"name": "HR"})
client.add_data("departments", {"name": "Engineering"})

# Добавляем сотрудников с ссылкой на департамент
client.add_data("employees", {"name": "Alice", "age": 30, "salary": 50000.0, "department_id": 1, "created_at": "2024-01-01 10:00:00"})
client.add_data("employees", {"name": "Bob", "age": 25, "salary": 45000.0, "department_id": 2, "created_at": "2024-02-01 10:00:00"})

# 3. Получение всех данных из таблицы с фильтрацией и сортировкой

# Получаем сотрудников старше 25 лет, отсортированных по зарплате
employees = client.get_data("employees", filters={"age": 25}, sort_by="salary")
print("Employees with age > 25 sorted by salary:", employees)

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

# 8. Пример использования сложной фильтрации (например, по диапазону зарплат)

filtered_employees = client.get_data("employees", filters={"salary_min": 45000, "salary_max": 55000})
print("Filtered employees with salary between 45k and 55k:", filtered_employees)

# 9. Пример использования пагинации (например, получения данных по страницам)
# Для простоты пагинация реализована через параметр limit и offset

paged_employees = client.get_data("employees", limit=2, offset=0)
print("Paged employees (first page):", paged_employees)
