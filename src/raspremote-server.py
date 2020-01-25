#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, jsonify, abort, request
import subprocess
import sys
from command_line import CommandLine
from launcher import Launcher
from ps import Ps
from ls import Ls

API_PATH = "/raspremote/api/"
CURRENT_API_VERSION = "v1.0/"

app = Flask("raspremote-server")


@app.route(API_PATH + CURRENT_API_VERSION)
def index():
    return "It works!"


''' Command line input '''
@app.route(API_PATH + CURRENT_API_VERSION + 'cli', methods=['POST'])
def cli():
    command_line = CommandLine()
    if command_line.process(request):
        return jsonify(command_line.result)
    else:
        abort(command_line.error)

''' Launch a program '''
@app.route(API_PATH + CURRENT_API_VERSION + 'launch', methods=['POST'])
def launch():
    launch = Launcher()
    if launch.process(request):
        return jsonify(launch.result)
    else:
        abort(launch.error)
        
''' Structured ps '''
@app.route(API_PATH + CURRENT_API_VERSION + 'ps')
def ps():
    ps = Ps()
    if ps.process(request):
        return jsonify(ps.result)
    else:
        abort(ps.error)

''' List files in a path '''
@app.route(API_PATH + CURRENT_API_VERSION + 'ls', methods=['POST'])
def ls():
    ls = Ls()
    if ls.process(request):
        return jsonify(ls.result)
    else:
        abort(ls.error)
    
        
def main():
    if len(sys.argv) < 2:
        print("Missing host")
        return False
    app.run(debug=True, host=sys.argv[1])

if __name__ == '__main__':
    main()

