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
 && pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip install gunicorn \
 && rm requirements.txt

# copy the sources as the last step
# and expose the server port
#  to make it accessible from the outside
COPY ./ /app/
EXPOSE 5000
