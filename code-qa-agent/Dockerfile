FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV PORT 8080
CMD ["python", "code-qa-agent/demo/app.py"]
