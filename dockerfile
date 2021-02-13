FROM nytimes/blender:2.91-cpu-ubuntu18.04 as dev
RUN apt-get update && apt-get install -y git
RUN pip install poetry
ENV PATH="/bin/2.91/python/bi:${PATH}"
ENV PATH="/usr/src/app/.venv/bin:${PATH}"
WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true && \
  poetry install
RUN poetry export -f requirements.txt > requirements.txt

# FROM nytimes/blender:2.91-cpu-ubuntu18.04 as prod
# ENV PYTHONUNBUFFERED=1
# WORKDIR /usr/src/app
# COPY --from=builder /usr/src/app/requirements.txt .
# RUN pip install -r requirements.txt
