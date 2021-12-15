docker-compose up -d
export DbURL="mongodb://localhost:27017"
export storageUrl="localhost:9000"
export storageAccessKey="admin"
export storageSecretKey="admin123"
uvicorn app.main:app --reload --port 3000