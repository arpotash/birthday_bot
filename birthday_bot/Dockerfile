FROM python:3.11.2-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ~/bd_bod
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD ["python", "-m", "main"]
