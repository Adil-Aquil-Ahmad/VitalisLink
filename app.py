from flask import Flask
from Routes import register_routes

app = Flask(__name__)
app.secret_key = 'adajsj435a$mKM%6mkls%mlamfo'

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
