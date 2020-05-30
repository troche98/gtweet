#!/usr/bin/env python3
from modules.ir import IR
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/api/v1", methods=['GET'])
def version():
    return jsonify("This is version 1.0.0")

@app.route("/api/", methods=['POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            print(request.form.to_dict())
            print(request.form.get('tweet'))
            if request.form.get('tweet') == None:
                return jsonify(None)
            i = IR()
            i.indexer()
            return jsonify(
                answer=i.searcher(request.form.get('tweet'))
            )
        except Exception as e:
            print(e)
            return jsonify(e)
    else:
        return "Bad request: not found", 404

if __name__ == "__main__":
    app.run()