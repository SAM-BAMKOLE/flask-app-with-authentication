from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    all_notes = Note.query.filter(Note.user_id==current_user.id)

    return render_template("home.html", user=current_user, notes=all_notes)


@views.route("/create-note", methods=["GET", "POST"])
@login_required
def create_new_note():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if len(content) < 20:
            flash("Content is too short, must be at least 20 characters", category="error")
            return render_template("create.html", user=current_user, title=title, content=content)

        new_note = Note(title=title, content=content, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()

        flash("New note created!", category="success")

    return render_template("create.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    data = json.loads(request.data)
    note_id = data['noteId']
    note = Note.query.get(note_id)
    # authenticate
    if note.user_id != current_user.id:
        flash("Unauthorized: This note does not belong to you", category="error")
        return jsonify({})
    db.session.delete(note)
    db.session.commit()

    return jsonify({})


@views.route("/note/<id>")
def view_note(id):
    note = Note.query.get(id)
    # check if exists
    if note == None:
        return render_template("404.html")
    # authenticate
    if note.user_id != current_user.id:
        flash("Cannot view another user's note, this note does not belong to you!", category="error")
        return redirect(url_for("views.home"))
    
    return render_template("view.html", note=note, user=current_user)

@views.route("/edit-note/<id>", methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get(id)

    if note == None:
        return render_template("404.html")
    # authenticate
    if note.user_id != current_user.id:
        flash("Cannot edit another user's note, this note does not belong to you!", category="error")
        return redirect(url_for("views.home"))
    
    if request.method == "POST":
        new_title = request.form.get("title")
        new_content = request.form.get("content")

        if len(new_content) < 20:
            flash("Content must be at least 20 characters", category="error")
            return render_template("edit.html", user=current_user, note=note)

        note.title = new_title
        note.content = new_content

        db.session.commit()

        flash("Note edited successfully!", category="success")
        return redirect(url_for("views.home"))
    return render_template("edit.html", user=current_user, note=note)

"""
# Route needee when there are ownerless notes. All ownerleess notes will be assigned to current user
@views.route("/set-note-owner/", methods=['GET'])
def set_note_owner():
    try:
        notes = Note.query.filter(Note.id==None)
        for note in notes:
            note.user_id = 2
            db.session.commit()

            flash(f"Note owner {current_user.username} set!", category="success")
            return redirect(url_for("views.home"))
    except Exception:
        flash("Unable to set notes users", category="error")
        return redirect(url_for("views.home"))
"""

@views.route("/get-notes")
def get_notes():
    all_notes = Note.query.all()
    return render_template("test.html", notes=all_notes, user=current_user)
