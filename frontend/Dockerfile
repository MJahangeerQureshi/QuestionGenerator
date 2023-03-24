FROM python:3.8
WORKDIR /app

# Install linux packages
RUN apt update && apt install -y zip htop screen libgl1-mesa-glx

# install poppler
RUN apt-get update && apt-get install poppler-utils -y

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

# Run
COPY . /app
CMD ["streamlit" ,"run", "app.py"]~