# base image
FROM python:3.12-slim

# setting a working directory
WORKDIR /app

#copying requirements and installing dependeces
COPY requirements.txt .
RUN pip install -r requirements.txt

#copying rest of the code
COPY . .

#exposing port
EXPOSE 8501 8000

#command to start fast api application
CMD ["bash", "-c", "uvicorn Movie_Recomm_System.Backend.main:app --host 0.0.0.0 --port 8000 & streamlit run Movie_Recomm_System/Frontend/app.py --server.port=8501 --server.address=0.0.0.0"]
