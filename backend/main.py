from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/merge")
def test(files: UploadFile = File(...)):
    print(files)
    return "hello"
