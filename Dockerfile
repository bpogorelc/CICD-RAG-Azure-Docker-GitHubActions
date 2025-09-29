FROM python:3.10-slim

WORKDIR /code

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webapp/ ./webapp/

# Expose port
EXPOSE 80

# Run the application
CMD ["uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "80"]