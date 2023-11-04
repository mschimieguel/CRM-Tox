import app
import os

if __name__ == '__main__':
    app.create_app().run(host='0.0.0.0', debug=True)