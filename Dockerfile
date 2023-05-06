FROM python:3.10.10-alpine as build

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY . .

RUN pip install build
RUN python -m build --wheel

RUN mv config config.py

FROM openstax/selenium-chrome

WORKDIR /app

ENV PATH "$PATH:/home/seluser/.local/bin"

COPY --from=build /app/ .

RUN python -m pip install --upgrade pip

RUN pip install dist/*.whl

RUN pip install waitress

EXPOSE 9888

CMD [ "waitress-serve", "--listen=*:9888", "--call", "main:create_app"] 