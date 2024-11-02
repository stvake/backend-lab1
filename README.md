# Інструкція запуску застосунку.

## Варіант 1: Зайти на задеплоїний проект на Render.com
Відкрийте ваш веб-браузер і зайдіть за посиланням до мого проєкту на [Render.com](https://backend-lab1-ve3g.onrender.com/healthcheck).

## Варіант 2: Запустити локально через Flask
1. Спочатку потрібно скопіювати репозиторій на свій локальний комп'ютер:
   ```bash
   git clone https://github.com/stvake/backend-lab1.git
   ```
   ```bash
   cd backend-lab1
   ```
3. Переконайтеся, що Python встановлений на вашому комп'ютері.
4. Встановіть залежності, виконавши команду:
   ```bash
   pip install -r requirements.txt
   ```
5. Запустіть додаток командою:
   ```bash
   flask run --host 0.0.0.0 --port 8080
   ```
6. Відкрийте у браузері: `http://localhost:8080/healthcheck`.

## Варіант 3: Запуск через Docker
1. Спочатку потрібно скопіювати репозиторій на свій локальний комп'ютер:
   ```bash
   git clone https://github.com/stvake/backend-lab1.git
   ```
   ```bash
   cd backend-lab1
   ```
1. Переконайтеся, що Docker встановлений на вашому комп'ютері.
2. Створіть Docker-контейнери, виконавши команду:
   ```bash
   docker-compose build
   ```
3. Запустіть контейнер:
   ```bash
   docker-compose up
   ```
4. Відкрийте у браузері: `http://localhost:8080`.
