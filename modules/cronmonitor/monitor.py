#!/usr/bin/env python3.6
###################################################################################################
# Imports
# --=-- Standard library imports
import datetime
import os

# --=-- Third party imports
from flask import Flask, json, Blueprint, render_template, abort
from flask_bootstrap import Bootstrap
from jinja2 import TemplateNotFound
from flask_debug import Debug
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# --=-- Local application imports
from api.v1 import api as api_v1
#from api.v1_1 import api as api_v1_1
#from api.v2 import api as api_v2
###################################################################################################

def main():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config['TESTING'] = True

    # Static pages
    @app.route('/', defaults={'page': 'index'})
    @app.route('/<page>')
    def show(page):
        try:
            rendering_page = 'pages/%s.html' % page
            return render_template(rendering_page, title='Cronner', versions=list(filter(lambda x: x[0]=='v', os.listdir('api'))))
        except TemplateNotFound:
            print('render_template could not display page %s'%(rendering_page))
            abort(404)

    #Debug(app)
    app.register_blueprint(api_v1.api, url_prefix='/v1')
    #app.register_blueprint(api_v1_1, url_prefix='/v1.1')
    #app.register_blueprint(api_v2, url_prefix='/v2')
    #app.run()

    #for rule in app.url_map.iter_rules():
    #    print(rule)

    app.run(debug=False)

if __name__ == "__main__":
    main()
