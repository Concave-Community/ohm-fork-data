FROM python:3.8

RUN mkdir /app

COPY pyproject.toml /app
WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . /app

CMD python stable_farm_data/get_curve_official_pool_snapshot.py
CMD python stable_farm_data/get_curve_factory_snapshot.py
