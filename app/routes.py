from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import CubeForm
from cube.rubiks_cube.rubiks_cube import RubiksCube
import pickle
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/solver', methods=['GET', 'POST'])
def solver():
    path = os.path.join('app', 'saved_states', 'state.pkl')
    if os.path.exists(path):
        with open(path, 'rb') as f:
            rc = pickle.load(f)
        form = CubeForm()
        if form.validate_on_submit():
            flash(f'Cube colour submitted {form.colour.data}')
            rc.initialise_step(form.colour.data)
            with open(path, 'wb') as f:
                pickle.dump(rc, f)
            return redirect(url_for('solver'))
    else:
        rc = RubiksCube(init_state='uninitialised')
        with open(path, 'wb') as f:
            pickle.dump(rc, f)
        return redirect(url_for('solver'))
    return render_template('solver.html', title='Solver', form=form)
