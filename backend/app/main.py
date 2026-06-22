from fastapi import FastAPI

app = FastAPI( title="Enterprise Analytics Agent")  

@app.get('/')
def read_root():
    return {"message": "Welcome to the Enterprise Analytics Agent API!"}