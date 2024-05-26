FROM python:3

WORKDIR /usr/src/app

COPY ./assets ./assets
COPY ./pages ./pages
COPY app.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/usr/src/app/app.py"]
