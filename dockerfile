FROM python:latest

WORKDIR /File2Anki

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "File2Anki.py" ]