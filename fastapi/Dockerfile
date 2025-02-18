FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

CMD ["fastapi", "run", "fastapi_image_server.py"]
