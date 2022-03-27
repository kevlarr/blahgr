FROM python:3.10.4

ENV PYTHONUNBUFFERED 1

WORKDIR /blahgr

COPY poetry.lock pyproject.toml /blahgr/

RUN pip3 install poetry
RUN poetry install

CMD ["./entrypoint"]
