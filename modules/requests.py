from flask import redirect, request, flash, url_for, render_template, Blueprint
from models.songs import SongInfo, SongForm
from configs import app, db, text_data, dummy_database
from filters.songrequestfilter import get_all_song_data
from data.data import request_data

admin_song = Blueprint('admin_song', __name__)

@admin_song.route('/add', methods=['GET', 'POST'])
def add_request():
    form = SongForm()
    if request.method == 'POST':
### Base de datos no relacional ###       
        if app.config['DUMMY_DATABASE']:
            add_song = request.form.get('song')
            add_user = request.form.get('user')
            add_new_request = {"user": add_user, "song": add_song} 
            request_data.append(add_new_request)
            print('Solicitud agregada exitosamente.')
            print(request_data)
            return redirect(url_for('admin_song.show_all_request'))
### Base de datos relacional ###
        else:
            song = request.form.get('song')
            user = request.form.get('user')
            new_request = SongInfo(song=song, user=user)
            db.session.add(new_request)
            db.session.commit()
            print('Solicitud agregada exitosamente.', 'success')
            return redirect(url_for('admin_song.show_all_request'))
    else:
            flash('Error en el formulario.', 'error')
            return render_template('request.html', form=form, text_data=text_data)



        
@admin_song.route('/all')
def show_all_request():
    song_data = get_all_song_data()
    return render_template('index.html', song_data=song_data, text_data=text_data)



@admin_song.route('/delete', methods=['POST'])
def delete_request():
    form = SongForm()
    if request.method == 'POST':       
### Base de datos no relacional ### 
        if app.config['DUMMY_DATABASE']:
            song_ids = request.form.getlist('song_ids')
            if song_ids:
                 session = request_data
                 for song_entry in session:
                        if song_entry['song'] in song_ids:
                            session.remove(song_entry)
                 return redirect(url_for('admin_song.show_all_request', song_entry=session))
                
### Base de datos relacional ###
        else:
            song_ids = request.form.getlist('song_ids')
        if song_ids:
            session = db.session()
            try:
                for song_id in song_ids:
                    song_entry = session.query(SongInfo).filter_by(id_song=song_id).first()
                    if song_entry:
                        session.delete(song_entry)
                session.commit()
                flash('Noticias eliminadas con éxito', 'success')
            except Exception as e:
                session.rollback()
                flash(f'Error al eliminar noticias: {str(e)}', 'error')
            else:
                flash('No se seleccionaron noticias para eliminar', 'warning')

        return redirect(url_for('admin_song.show_all_request'))
    else:
        
        pass 
