FROM python:3.6.8
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN update-ca-certificates
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE  80
CMD ["python", "server.py"]