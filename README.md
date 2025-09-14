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

## Установка зависимостей

```bash
pip install -r requirements.txt
```

Для запуска на CPU

```bash
python -m pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/`
```

Для запуска на GPU (CUDA)

```bash
python -m pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
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