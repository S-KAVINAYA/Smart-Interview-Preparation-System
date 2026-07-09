from fastapi import FastAPI

app = FastAPI(
    title="Smart Interview Preparation System"
)


@app.get("/")
def home():
    return {
        "message": "AI Interview Preparation Backend Running"
    }