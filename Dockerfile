FROM python:3.11-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libffi-dev \
       ffmpeg \
       aria2 \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt
COPY . /app

# Run the bot (single foreground process)
CMD ["python3", "main.py"]
