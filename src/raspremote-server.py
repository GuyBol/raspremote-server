#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, jsonify, abort, request
import subprocess
from command_line import CommandLine

API_PATH = "/raspremote/api/"
CURRENT_API_VERSION = "v1.0/"

app = Flask("raspremote-server")


@app.route(API_PATH + CURRENT_API_VERSION)
def index():
    return "It works!"

# temporary, for demo purpose
@app.route(API_PATH + CURRENT_API_VERSION + 'ps')
def ps():
    p = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in p.stdout:
        lines.append(line)
    return jsonify({'lines': lines})

''' Command line input '''
@app.route(API_PATH + CURRENT_API_VERSION + 'cli', methods=['POST'])
def cli():
    if not request.json:
        abort(400)
    command_line = CommandLine()
    if command_line.process(request):
        return command_line.result
    else:
        return command_line.error

if __name__ == '__main__':
    app.run(debug=True)

