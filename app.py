from src.app import app as dash_app
import src.callbacks  # noqa: F401
from src.layouts import body

dash_app.layout = body

server = dash_app.server

if __name__ == '__main__':
    dash_app.run_server(debug=True)