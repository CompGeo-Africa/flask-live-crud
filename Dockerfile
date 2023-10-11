FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4001

CMD [ "flask", "run", "--host=0.0.0.0", "--port=4001"]
