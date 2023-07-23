FROM python:3.8-slim

RUN pip3 install poetry --user poetry
ENV PATH="${PATH}:/root/.local/bin"


WORKDIR /app
EXPOSE 5000
COPY ./ .

RUN poetry install

#ENTRYPOINT ["poetry", "run", "python", "main.py"]

#RUN python main.py
CMD ["poetry", "run", "python", "main.py"]
