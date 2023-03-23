# Base layer
FROM python:3.8
WORKDIR /app

# Install linux packages
RUN apt update && apt install -y zip htop screen libgl1-mesa-glx && apt-get update

## Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY . /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]~
