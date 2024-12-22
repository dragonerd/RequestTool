from configs import db, app
from models.songs import SongInfo
from data.data import request_data



def get_all_song_data():
    if app.config['DUMMY_DATABASE']:
        songs_entries = request_data
        song_data = []
        for entry in songs_entries:
          return songs_entries

    else:
        songs_entries = db.session.query(SongInfo).all()
        song_data = []
        for entry in songs_entries:
            song_data.append({"id_song":entry.id_song,"song": entry.song,"user": entry.user,"selected": False
        })

    db.session.close()
    return song_data
