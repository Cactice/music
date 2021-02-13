FROM python:3.8-slim as builder
WORKDIR /usr/src/app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt > requirements.txt

FROM 2.91-cpu-ubuntu18.04
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
