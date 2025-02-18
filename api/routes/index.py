
from flask import Flask, render_template,request, redirect, Blueprint, send_from_directory

def load_index():
    return render_template("index.html")