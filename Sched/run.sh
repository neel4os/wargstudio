# docker-compose up -d
export redisUrl="localhost:6379/0"
export storageUrl="localhost:9000"
export storageAccessKey="admin"
export storageSecretKey="admin123"
uvicorn app.main:app --reload --port 4000