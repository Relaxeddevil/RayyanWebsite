from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':

    from views import views

    app.register_blueprint(views, url_prefix='/')

    app.run(debug=True)