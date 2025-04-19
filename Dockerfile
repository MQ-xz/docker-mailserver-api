FROM mailserver/docker-mailserver:14.0.0

WORKDIR /app

# Install Python & dependencies
RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --break-system-packages -r requirements.txt

COPY . .

# Add your Flask app as a supervisor service
COPY api.conf /etc/supervisor/conf.d/api.conf

