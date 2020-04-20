from flask import Flask, jsonify, request
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_cors import CORS
from Time_Matters_Query import ArquivoPT


def main():
    """The main function for this script."""
    app.run(host='127.0.0.1', port='5000', debug=True)
    CORS(app)


app = Flask(__name__)
SCRIPT_NAME = "/timematters"
app.config['JSON_SORT_KEYS'] = False

app.config['SWAGGER'] = {
    "title": "Time Matters Query! API",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "false"),
    ],
    "info": {
        "title": "Time Matters Query API",
        "description": "Welcome to Time Matters Query! API webpage. Here you can try Time Matters Query directly calling our HTTP API. Alternatively you can play with our python package at https://github.com/LIAAD/Time-Matters-query",
        "contact": {
            "responsibleOrganization": "INESC TEC",
            "responsibleDeveloper": "Ricardo Campos",
            "email": "ricardo.campos@ipt.pt",
            "url": "http://www.ccc.ipt.pt/~ricardo/",
        },
        "termsOfService": "https://github.com/LIAAD/Time-Matters-Query",
        "version": "0.0.1"
    },
    "schemes": [
        "http",
        "https"
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    #"basePath": SCRIPT_NAME,
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

Swagger(app)

def handle_time_matters_query(query, max_items=50, newspaper3k=False, domains=[], beginDate='', endDate='', title=False,snippet=True,fullContent=False, link=''):

    APT = ArquivoPT(max_items, newspaper3k=newspaper3k)
    result = APT.getResult(query,  domains=domains, beginDate=beginDate, endDate=endDate, title=title,snippet=snippet,fullContent=fullContent, link=link)

    model = {
        'Statistical_info': result[0],
        'Result_articles': result[1]
    }

    return model


@app.route("/api/v1.0/arquivopt", methods=['POST'])
@swag_from('Arquivo_pt.yml')
def Arquivo_pt():
    try:
        data = request.form
        print(data['query'])
    except Exception as e:
        return jsonify({'message': str(e)})


if __name__ == '__main__':
    main()
