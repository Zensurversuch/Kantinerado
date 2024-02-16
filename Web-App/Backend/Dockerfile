FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000", "--debugger", "--reload" ]