
from flask import Flask, render_template,request, redirect, Blueprint, send_from_directory

def load_camera_page():
    return render_template("camera.html")