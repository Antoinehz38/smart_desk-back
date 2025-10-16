from backend import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8085, reload=False)



uvicorn.run("backend:app", host="127.0.0.1", port=8085, reload=True)