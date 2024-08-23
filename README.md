## Запуск проекта

- docker compose up



#### API для тестирования
baseUrl = http://localhost:8000/api/v1

1. Создание груза
- Method: POST
- Endpoint: {{baseUrl}}/cargo
- Body:
- pick_up_zip_code: 410000
- delivery_zip_code: 630000
- weight: 149
- description: Морковь
2. Получение списка грузов
- Method: GET
- Endpoint: {{baseUrl}}/cargo
- No body required
3. Получение информации о конкретном грузе по ID 

- Method: GET
- Endpoint: {{baseUrl}}/cargo/1


4. Удаление груза по ID
- Method: DELETE
- Endpoint: {{baseUrl}}/cargo
- Body:
- items: 1,2,3

5. Редактирование груза по ID
- Method: PATCH
- Endpoint: {{baseUrl}}/cargo
- Body:
- id: 1
- weight: 57
- description: Свекла
- 
6. Редактирование машины по ID
- Method: PATCH
- Endpoint: {{baseUrl}}/car
- Body:
- id: 1
- location_zip_code: 625000
- load_capacity :450
7. Фильтр списка грузов
- Method: GET
- Endpoint: {{baseUrl}}/cargo/filter/
- Query Params:
- weight_min: 45
- weight_max: 1000
- distance_max: 700








