FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scrape_books.py .

# O books.xlsx fica em /app; monte um volume nesse diretorio para acessa-lo.
CMD ["python", "scrape_books.py"]
