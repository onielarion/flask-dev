from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


# Create a blueprint
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Get the data from the form
        note = request.form.get('note')

        # Test the data
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # Add the note to the database
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

            flash('Note added!', category='success')
            return redirect(url_for('views.home'))

    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    # Get the data from the form
    note = json.loads(request.data)
    noteId = note['noteId']

    # Delete the note from the database
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/upload', methods=['POST'])
@login_required
def upload_file():
    file = request.files['file']
    if file:
        # Do something with the file
        import pandas as pd
        df = pd.read_csv(file)
        print(df)

        # Do something with the file
        flash('File selected', category='success')
        return f'File uploaded successfully - {file.filename}'
    else:
        flash('No file selected!', category='error')
        return redirect(url_for('views.home'))
    
