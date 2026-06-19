FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fill_form.py data.json sonnar.png .

# O confirmation.png fica em /app; monte um volume nesse diretorio para acessa-lo.
CMD ["python", "fill_form.py"]
