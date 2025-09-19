import uvicorn

from app.config.settings import Config

from app.core.app_app import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host=Config.HOST, port=int(Config.PORT))