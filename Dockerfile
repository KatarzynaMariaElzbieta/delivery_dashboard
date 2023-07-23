FROM python:3.8-slim

RUN pip3 install poetry

WORKDIR /app
EXPOSE 5000
COPY ./ .

RUN poetry install

CMD ["poetry", "run", "python", "main.py"]
