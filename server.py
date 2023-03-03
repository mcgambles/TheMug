from flask_app import app
from flask_app.controllers import users, games, signups

if __name__=="__main__":
    app.run(host='localhost', port=5000, debug=True)