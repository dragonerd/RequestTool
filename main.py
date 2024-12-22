from configs import app, server_host, server_port, db, text_data, dummy_database
from flask import render_template
from models.songs import SongInfo
from modules.requests import admin_song 
from data.data import request_data
import webbrowser

@app.route('/')
@app.route('/index')
def index():
    if app.config['DUMMY_DATABASE']:
        songs = request_data
        return render_template('index.html', text_data=text_data, songs=songs)
    else:
        songs = db.session.query(SongInfo).limit(2).all()
        return render_template('index.html', text_data=text_data, songs=songs)



##################################         add request song          ############################################
app.register_blueprint(admin_song, url_prefix='/req')

if __name__ == "__main__":
   webbrowser.open_new('http://127.0.0.1:5000/')
   app.run(port=server_port, host=server_host)

