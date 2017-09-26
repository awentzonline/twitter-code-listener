from python:2.7

RUN apt-get update && apt-get install -y libzbar-dev

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY code_listener.py ./

CMD ["python", "-u", "code_listener.py"]
