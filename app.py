from flask import Flask
# הגבלת גישה לפי כמות בקשות
from flask_limiter import Limiter
# מחלק גישה לכל לקוח ולא כללי
from flask_limiter.util import get_remote_address

app = Flask(__name__)



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
