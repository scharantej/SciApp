 
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    topics = conn.execute('SELECT * FROM topics').fetchall()
    conn.close()
    return render_template('index.html', topics=topics)

@app.route('/topic/<topic_id>')
def topic(topic_id):
    conn = get_db_connection()
    topic = conn.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()
    experiments = conn.execute('SELECT * FROM experiments WHERE topic_id = ?', (topic_id,)).fetchall()
    conn.close()
    return render_template('topic.html', topic=topic, experiments=experiments)

@app.route('/experiment/<experiment_id>')
def experiment(experiment_id):
    conn = get_db_connection()
    experiment = conn.execute('SELECT * FROM experiments WHERE id = ?', (experiment_id,)).fetchone()
    conn.close()
    return render_template('experiment.html', experiment=experiment)

@app.route('/progress')
def progress():
    conn = get_db_connection()
    progress = conn.execute('SELECT * FROM progress').fetchall()
    conn.close()
    return render_template('progress.html', progress=progress)

@app.route('/add_progress', methods=('POST',))
def add_progress():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('INSERT INTO progress (topic_id, experiment_id) VALUES (?, ?)',
                     (request.form['topic_id'], request.form['experiment_id']))
        conn.commit()
        conn.close()
        return redirect(url_for('progress'))

if __name__ == '__main__':
    app.run(debug=True)
