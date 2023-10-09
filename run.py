import uvicorn

from config import get_config

if __name__ == "__main__":
    config = get_config()
    uvicorn.run("main:app", reload=config.local)
