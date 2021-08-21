from chalicelib.app import app as dash_app
import chalicelib.callbacks  # noqa: F401
from chalicelib.layouts import body

dash_app.layout = body
dash_app.finalise()

app = dash_app.server  # chalice uses the app variable for deployment
