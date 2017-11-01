#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, jsonify, abort, request
import subprocess
from command_line import CommandLine
import sys
import launcher

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
    launch = launcher.Launcher()
    if launch.process(request):
        return jsonify(launch.result)
    else:
        abort(launch.error)
        
''' Structured ps '''
@app.route(API_PATH + CURRENT_API_VERSION + 'ps')
def ps():
    p = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in p.stdout:
        lines.append(line)
    return jsonify({'lines': lines})
    
        
def main():
    if len(sys.argv) < 2:
        print "Missing host"
        return False
    app.run(debug=True, host=sys.argv[1])

if __name__ == '__main__':
    main()

