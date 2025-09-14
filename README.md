# Установка проекта

## Клонирование репозитория

`git clone https://github.com/Solar-Spark/BCC-OCR-Case.git`

## Создание и активация виртуального окружения
`
python -m venv .venv
.\.venv\Scripts\activate
`

## Установка зависимостей

`pip install -r requirements.txt`

### Для запуска на CPU

`python -m pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/`

### Для запуска на GPU (CUDA)

`python -m pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/`

## Установка зависимостей Frontend

`
cd ocr-frontend
npm install
`

# Запуск проекта

## Backend

`
cd ocr-backend
uvicorn main:app --reload
`

## Frontend

`
cd ocr-frontend
npm run dev
`

### Адрес Frontend
`localhost:5173`