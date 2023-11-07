 
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Experiments page
@app.route('/experiments')
def experiments():
    # Connect to the database
    conn = sqlite3.connect('experiments.db')
    # Create a cursor
    c = conn.cursor()

    # Get all the experiments
    c.execute('SELECT * FROM experiments')
    experiments = c.fetchall()

    # Close the connection
    conn.close()

    return render_template('experiments.html', experiments=experiments)

# Experiment details page
@app.route('/experiments/<int:experiment_id>')
def experiment_details(experiment_id):
    # Connect to the database
    conn = sqlite3.connect('experiments.db')
    # Create a cursor
    c = conn.cursor()

    # Get the experiment details
    c.execute('SELECT * FROM experiments WHERE id=?', (experiment_id,))
    experiment = c.fetchone()

    # Close the connection
    conn.close()

    return render_template('experiment_details.html', experiment=experiment)

# Add experiment page
@app.route('/add_experiment', methods=['GET', 'POST'])
def add_experiment():
    if request.method == 'POST':
        # Get the form data
        title = request.form['title']
        description = request.form['description']

        # Connect to the database
        conn = sqlite3.connect('experiments.db')
        # Create a cursor
        c = conn.cursor()

        # Insert the experiment into the database
        c.execute('INSERT INTO experiments (title, description) VALUES (?, ?)', (title, description))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

        # Redirect to the experiments page
        return redirect(url_for('experiments'))

    return render_template('add_experiment.html')

# Edit experiment page
@app.route('/edit_experiment/<int:experiment_id>', methods=['GET', 'POST'])
def edit_experiment(experiment_id):
    if request.method == 'POST':
        # Get the form data
        title = request.form['title']
        description = request.form['description']

        # Connect to the database
        conn = sqlite3.connect('experiments.db')
        # Create a cursor
        c = conn.cursor()

        # Update the experiment in the database
        c.execute('UPDATE experiments SET title=?, description=? WHERE id=?', (title, description, experiment_id))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

        # Redirect to the experiments page
        return redirect(url_for('experiments'))

    # Connect to the database
    conn = sqlite3.connect('experiments.db')
    # Create a cursor
    c = conn.cursor()

    # Get the experiment details
    c.execute('SELECT * FROM experiments WHERE id=?', (experiment_id,))
    experiment = c.fetchone()

    # Close the connection
    conn.close()

    return render_template('edit_experiment.html', experiment=experiment)

# Delete experiment page
@app.route('/delete_experiment/<int:experiment_id>')
def delete_experiment(experiment_id):
    # Connect to the database
    conn = sqlite3.connect('experiments.db')
    # Create a cursor
    c = conn.cursor()

    # Delete the experiment from the database
    c.execute('DELETE FROM experiments WHERE id=?', (experiment_id,))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    # Redirect to the experiments page
    return redirect(url_for('experiments'))

if __name__ == '__main__':
    app.run(debug=True)
