FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

LABEL Name=recom-engine Version=0.0.1

# Set working directory
WORKDIR /var/www/

# Install dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends mc net-tools

# Clear cache
# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

# copy requirements file
COPY ./requirements.txt /var/www/app/requirements.txt

RUN pip install --upgrade pip && pip install -r /var/www/app/requirements.txt \
    && rm -rf /root/.cache/pip

