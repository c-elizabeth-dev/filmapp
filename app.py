import sqlite3 as sql
from connect import *
from flask import Flask, render_template, url_for, request, flash, redirect
from werkzeug.exceptions import abort


# def __init__(self):
#     con=sql.connect('filmflix.db')
#     c=con.cursor
#     c.execute("CREATE TABLE filmflix(ID INTEGER NOT NULL PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, is_admin BOOLEAN)")
#     con.commit()


def get_db_connection():
    conn = sql.connect('filmflix.db')
    conn.row_factory = sql.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234sdefddeffdfjy$'



@app.route('/delete', methods=['GET'])
def delete_list():
    conn = get_db_connection()
    filmTable = conn.execute('SELECT * FROM tblFilms').fetchall()
    conn.close()
    return render_template('delete_list.html', filmTable=filmTable)




@app.route('/delete/<int:filmID>', methods=['GET', 'POST'])
def delete_confirm(filmID):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM tblFilms WHERE filmID = ?', (filmID,)).fetchone()

    if film is None:
        abort(404)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'delete':
            # If "Delete" button is clicked, delete the record
            conn.execute('DELETE FROM tblFilms WHERE filmID = ?', (filmID,))
            conn.commit()
            conn.close()
            return redirect(url_for('delete_list'))
        else:
            # If "No" button is clicked, return to the list of records
            conn.close()
            return redirect(url_for('delete_list'))

    conn.close()
    return render_template('delete_record.html', film=film)







@app.route('/update', methods=['GET'])
def update_list():
    conn = get_db_connection()
    filmTable = conn.execute('SELECT * FROM tblFilms').fetchall()
    conn.close()
    return render_template('update_list.html', filmTable=filmTable)


@app.route('/update/<int:filmID>', methods=['GET', 'POST'])
def update_record(filmID):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM tblFilms WHERE filmID = ?', (filmID,)).fetchone()

    if film is None:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title')
        yearReleased = request.form.get('yearReleased')
        rating = request.form.get('rating')
        duration = request.form.get('duration')
        genre = request.form.get('genre')
        if not title:
            flash('Title is required!')
        else:
            conn.execute('UPDATE tblFilms SET title=?, yearReleased=?, rating=?, duration=?, genre=? WHERE filmID=?', (title, yearReleased, rating, duration, genre, filmID))
            conn.commit()
            conn.close()
            return redirect(url_for('update_list'))

    conn.close()
    return render_template('update_record.html', film=film)






@app.route('/create', methods = ('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        yearReleased = request.form.get('yearReleased')
        rating = request.form.get('rating')
        duration = request.form.get('duration')
        genre = request.form.get('genre')

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO tblFilms (title, yearReleased, rating, duration, genre) VALUES (?, ?, ?, ?, ?)', (title, yearReleased, rating, duration, genre))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/index')
def index():
    conn = get_db_connection()
    filmTable = conn.execute('SELECT * FROM tblFilms').fetchall()
    conn.close()
    return render_template('index.html', filmTable=filmTable)

if __name__ == '__main__':
    app.run(debug=True)

