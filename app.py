# ------------ Owen Lib ------------- #
from TODOApp.config import Development, Production
from TODOApp import create_app


if __name__ == '__main__':
    app = create_app(Development)
    app.run()
