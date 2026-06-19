FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY login_flow.py .

# O script ja roda em modo headless.
CMD ["python", "login_flow.py"]
