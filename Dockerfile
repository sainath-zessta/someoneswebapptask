# # For more information, please refer to https://aka.ms/vscode-docker-python
# FROM mongo:latest
# EXPOSE 27017

FROM python:3.8-slim

EXPOSE 7731

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
# RUN python -m pytest web-app/test_app.py
# RUN python -m pylint web-app/test_app.py
# RUN python -m pycodestyle web-app/test_app.py
# RUN python -m flake8 web-app/test_app.py



# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]