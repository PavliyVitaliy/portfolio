FROM python:3.11

WORKDIR /backend

COPY /backend/requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r backend/requirements.txt

COPY /backend/app /backend/app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0"]
