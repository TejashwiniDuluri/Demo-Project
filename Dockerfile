FROM python:3.6.7

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1

# Copy the rest of the applicaion's code
COPY . /usr/src/app

WORKDIR /usr/src/app

# Install dependencies
RUN pip install -r requirements.txt

# Run the app
CMD ["./run_app.sh"]

EXPOSE 8000
