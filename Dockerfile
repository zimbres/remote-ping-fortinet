FROM python:alpine

WORKDIR /code

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./modules ./modules
COPY ./main.py ./
COPY ./env.json.example ./env.json

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
