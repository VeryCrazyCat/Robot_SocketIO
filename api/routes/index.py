
from flask import Flask, render_template,request, redirect, Blueprint, send_from_directory
import json
import ast
import api.routes.emitter as emitter
import api.sockets.nodemcu_action as nodemcu_action

def load_index():
    if request.method == "POST":
        
        data = ast.literal_eval(str(request.data.decode('ASCII')))
        print(data["data"])
        nodemcu_action.emit_nodemcu_status(data["data"])
        return "hello back"

    return render_template("index.html")