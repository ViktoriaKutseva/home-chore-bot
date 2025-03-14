FROM python:3.12-slim

WORKDIR /app

COPY /app/ .

ENV PYTHONPATH=/app:$PYTHONPATH
ENV PYTHONPATH=/:$PYTHONPATH

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]