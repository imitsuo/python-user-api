FROM python:3.6
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY api/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /api/

# Run the application:
COPY ./api /api
EXPOSE 8000
CMD ["python", "main.py"]