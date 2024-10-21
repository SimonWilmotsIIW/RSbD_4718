from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'astronauts.db'


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS astronauts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mission TEXT,
            rank TEXT,
            achievements TEXT,
            picture TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VerySensitiveData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

def prefill():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    astronauts = [
        ('Neil Armstrong', 'Apollo 11', 'Commander', 'First person to walk on the moon', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Neil_Armstrong_pose.jpg/1200px-Neil_Armstrong_pose.jpg'),
        ('Howard Wolowitz', 'Apollo 11', 'Payload Specialist', 'Installation of the Wolowitz Waste Deposit System', 'https://yt3.googleusercontent.com/ytc/AIdro_nrUCA3ICcPgx6_8J_rdEFlh8MU4Q4HaoweIZRHiTzrLg=s900-c-k-c0x00ffffff-no-rj'),
        ('Yuri Gagarin', 'Vostok 1', 'Pilot', 'First human in space', 'https://upload.wikimedia.org/wikipedia/commons/e/e5/Yuri_Gagarin_%281961%29_-_Restoration.jpg'),
        ('Sally Ride', 'STS-7', 'Mission Specialist', 'First American woman in space', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Sally_Ride_%281984%29.jpg/1200px-Sally_Ride_%281984%29.jpg'),
        ('Dirk Frimout', 'STS-45 ', 'Payload Specialist', 'First Belgian astronaut', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Frimout.jpg/440px-Frimout.jpg'),
        ('Frank De Winne', 'ISS Expedition 21', 'Commander', 'First Belgian ESA astronaut', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Frank_De_Winne_2009.jpg/440px-Frank_De_Winne_2009.jpg'),
        ('Simon Wilmots', 'OSCAR', 'Wannabe astronaut', 'First astronaut from Hasselt University', 'https://media.licdn.com/dms/image/v2/D4E03AQEvqJVZ042IpQ/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1720721310891?e=2147483647&v=beta&t=JKMiVPwx0zuFO2F0QXngejAL3P1pOzm-2wtO4J-sfC8'),

    ]

    cursor.executemany('''
        INSERT INTO astronauts (name, mission, rank, achievements, picture)
        VALUES (?, ?, ?, ?, ?)
    ''', astronauts)

    sensitive_data = [
        ('admin', 'admin'),
        ('superuser', '12345'),
        ('user', 'supra'),
    ]

    cursor.executemany('''
        INSERT INTO VerySensitiveData (username, password)
        VALUES (?, ?)
    ''', sensitive_data)

    conn.commit()
    conn.close()

with app.app_context():
    create_table()
    prefill()


@app.route('/astronauts', methods=['GET'])
def get_astronauts():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM astronauts')
    astronauts = cursor.fetchall()

    conn.close()

    return jsonify(astronauts)

@app.route('/search', methods=['POST'])
def search():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    name = request.form['query']

    """"
    SQL injection is possible here with:
    query = f"SELECT * FROM astronauts WHERE name ='{name}'"
    Exploitations tried:
        - test' OR 1=1; --
        - Simon' UNION SELECT 1, username, password, NULL, NULL, NULL FROM VerySensitiveData--
    """ 

    # SQL Injection vulnerability:
    # query = f"SELECT * FROM astronauts WHERE name ='{name}'"
    # astronauts = cursor.execute(query)

    # SQL Injection fix:
    query = "SELECT * FROM astronauts WHERE name = ?"
    astronauts = cursor.execute(query, (name,))

    return render_template('index.html', astronauts=astronauts)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        mission = request.form.get('mission', '')
        rank = request.form.get('rank', '')
        achievements = request.form.get('achievements', '')
        picture = request.form.get('picture', '')

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO astronauts (name, mission, rank, achievements, picture) 
            VALUES (?, ?, ?, ?, ?)
        ''', (name, mission, rank, achievements, picture))
        conn.commit()

        conn.close()

        return redirect(url_for('home'))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM astronauts')
    astronauts = cursor.fetchall()

    conn.close()

    return render_template('index.html', astronauts=astronauts)


if __name__ == '__main__':
    app.run()

