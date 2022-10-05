from flask import Blueprint, request, flash, render_template, redirect, url_for, escape, session


index = Blueprint('index', __name__)

@index.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('newworld.home'))