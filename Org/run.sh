docker-compose up -d
export DbURL="mongodb://localhost:27017"
uvicorn app.main:app --reload --port 3000