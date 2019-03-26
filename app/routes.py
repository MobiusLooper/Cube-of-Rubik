from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import CubeForm
from cube.rubiks_cube.functions import build_cube, save_cube
from cube.rubiks_cube.controller import RubiksCubeController
import pickle
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/solver', methods=['GET', 'POST'])
def solver():
    rc = build_cube('test')
    form = CubeForm()
    if form.validate_on_submit():
        flash(f'Cube colour submitted {form.colour.data}')
        controller = RubiksCubeController()
        controller.initialise_step(rc, form.colour.data)
        save_cube(rc)
        return redirect(url_for('solver'))
    else:
        return render_template('solver.html', title='Solver', form=form)
