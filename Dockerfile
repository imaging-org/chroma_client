FROM python:3.11.5-slim-bullseye as compiler
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y

WORKDIR /app/

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install Flask Flask-Cors gunicorn
RUN pip install chromadb

FROM python:3.11.5-alpine3.18 as runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/
EXPOSE 5646
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]