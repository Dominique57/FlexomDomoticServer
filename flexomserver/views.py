from . import app


@app.get("/")
def root():
    return "Hello World !"
