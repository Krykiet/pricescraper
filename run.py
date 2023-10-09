import uvicorn

from app.config import get_config

if __name__ == "__main__":
    config = get_config()
    if config.local:
        print('@@Config local@@')
        uvicorn.run("app.main:app", reload=config.local)
    else:
        print('@@Config prod@@')
        uvicorn.run("app.main:app", port=10000, host='0.0.0.0', reload=config.prod)

