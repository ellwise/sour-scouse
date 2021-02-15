from app import app
from layouts import make_layout
import callbacks  # important to have this after layouts

app.title = "Sour Scouse"
app.layout = make_layout()

server = app.server  # zappa uses this variable for deployment

if __name__ == "__main__":
    app.run_server(debug=False)
