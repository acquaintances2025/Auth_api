FROM registry.flowai.ru/base/python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt --root-user-action=ignore

COPY src1 /app/

EXPOSE 8081
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8081"]