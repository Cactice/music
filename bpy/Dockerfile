# python 3.7
FROM nytimes/blender:2.91-cpu-ubuntu18.04 as dev
RUN apt-get update && apt-get install -y git
RUN pip install poetry
ENV PATH="/bin/2.91/python/bin:${PATH}"
ENV PATH="/usr/src/app/.venv/bin:${PATH}"

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./
RUN \
  poetry config virtualenvs.in-project true && \
  poetry install --no-dev
RUN cp -rf /usr/src/app/.venv/lib/* /bin/2.91/python/lib

COPY install_sverchok.py ./
RUN blender -P install_sverchok.py -b
