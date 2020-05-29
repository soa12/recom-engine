FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

LABEL Name=recom-engine Version=0.0.1

# Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends mc net-tools
# Clear cache
# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

# Set working directory
WORKDIR /var/www/

# copy requirements file
#COPY ./requirements.txt /var/www/app/requirements.txt

#ARG packeges_path
#ENV PYTHONUSERBASE="$packeges_path"
#ENV PATH="$packeges_path/bin:$PATH"
#RUN pip install -r /var/www/app/requirements.txt --user
ENV PATH=/var/www/bin:$PATH
