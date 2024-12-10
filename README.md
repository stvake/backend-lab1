# Інструкція запуску застосунку.

Номер групи - 21, тому варіант `21 % 3 = 0` - Облік доходів.

## Варіант 1: Зайти на задеплоїний проект на Render.com
Відкрийте ваш веб-браузер і зайдіть за посиланням до мого проєкту на [Render.com](https://backend-lab1-ve3g.onrender.com). Далі можете надсилати запити.

## Варіант 2: Запустити локально через Flask
1. Спочатку потрібно скопіювати репозиторій на свій локальний комп'ютер:
   ```bash
   git clone https://github.com/stvake/backend-lab1.git
   cd backend-lab1
   ```
2. Переконайтеся, що Python встановлений на вашому комп'ютері.
3. Встановіть залежності, виконавши команду:
   ```bash
   pip install -r requirements.txt
   ```
4. Встановіть змінні середовища для підключення до бази даних:
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DB`
   - `DB_HOST`
5. Запустіть додаток командою:
   ```bash
   flask run --host 0.0.0.0 --port 8080
   ```
6. Надсилайте запити на `http://localhost:8080`.

## Варіант 3: Запуск через Docker
1. Спочатку потрібно скопіювати репозиторій на свій локальний комп'ютер:
   ```bash
   git clone https://github.com/stvake/backend-lab1.git
   cd backend-lab1
   ```
2. Переконайтеся, що Docker встановлений на вашому комп'ютері.
3. Встановіть змінні середовища для підключення до бази даних:
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DB`
4. Створіть та запустіть Docker-контейнери, виконавши команду:
   ```bash
   docker-compose up db
   docker-compose up app
   ```
5. Надсилайте запити на `http://localhost:8080`.
