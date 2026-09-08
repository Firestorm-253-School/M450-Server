from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Snake Game API"}

@app.get("/health")
def health():
    return {"message": "Service is running"}
