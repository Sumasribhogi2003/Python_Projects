from fastapi import FastAPI
from api.query import router as query_router

app = FastAPI()

# Include the routes from query.py
app.include_router(query_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
