FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt && \
    chmod +x run.sh

CMD ["sh", "run.sh"]

