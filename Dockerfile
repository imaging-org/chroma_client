FROM python:3.12.3-alpine3.19 as compiler
ENV PYTHONUNBUFFERED 1

RUN apk update

WORKDIR /app/

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt

FROM python:3.12.3-alpine3.19 as runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/
EXPOSE 5646
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
