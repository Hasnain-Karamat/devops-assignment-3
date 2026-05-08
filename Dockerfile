FROM python:3.11

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    chromium \
    chromium-driver

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["pytest", "-v"] 
