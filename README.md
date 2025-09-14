# Установка проекта

Клонирование репозитория

```bash
git clone https://github.com/Solar-Spark/BCC-OCR-Case.git
```

Создание и активация виртуального окружения

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Создание .env файла

Создайте файл .env в корне проекта с содержимым:

```
GITHUB_API_KEY=<Ваш ключ GitHub AI API>
ISGPU=False
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

Для запуска на CPU

```bash
python -m pip install paddlepaddle
```

Для запуска на GPU (CUDA)

```bash
python -m pip install paddlepaddle-gpu
```

## Установка зависимостей Frontend

```bash
cd ocr-frontend
npm install
```

# Запуск проекта

Backend

```bash
cd ocr-backend
uvicorn main:app --reload
```

Frontend

```bash
cd ocr-frontend
npm run dev
```

### Адрес Frontend
`localhost:5173`