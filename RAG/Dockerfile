FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copie le reste du code (après l'installation)
COPY . .

CMD ["python", "RAGMultimodal.py"]