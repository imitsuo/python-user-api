FROM python:3.6
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir app

# Install dependencies:
COPY src/api/requirements.txt ./app
RUN pip install -r /app/requirements.txt

WORKDIR /app

# Run the application:
COPY src ./src
EXPOSE 8000
CMD ["python", "./src/api/main.py"]