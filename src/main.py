import uvicorn

from src.config.settings import Config

from src.infrastructure import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host=Config.HOST, port=int(Config.PORT))