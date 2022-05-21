FROM python:3.8-slim

# separate requirements fetching routines
# from the application layer
# this way, docker's caching will be
# used better (i.e., the layer won't be
# rebuilt each time something is changed 
# in the sources)
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

# chain the command to reduce number of layers
RUN mkdir logs \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir gunicorn \
 && rm requirements.txt

# copy the sources as the last step
# and expose the server port
#  to make it accessible from the outside
COPY ./app/ /app/app
COPY ./src/ /app/src
COPY wsgi.py /app/wsgi.py

EXPOSE 5000
