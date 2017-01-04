import sqlite3, os, sys
import argparse
import yaml, hashlib

class MusicLibrary():

    def __init__(self, music_db):
        self.music_db = music_db
        self.conn = sqlite3.connect(self.music_db)

    def add_to_library(self, directory, songs):
        song_ids = []
        with self.conn:
            cursor = self.conn.cursor()
            for song in songs:
                abs_song_path = os.path.abspath(song)
                song_db_details = self.get_song_db_details(abs_song_path, directory)
                if song_db_details["exists"]:
                    print("The song "+os.path.basename(abs_song_path) +" already exists in the database")
                    continue
                unique_song_hash = song_db_details["uniqueid"]
                song_name = abs_song_path[len(directory):len(abs_song_path)]
                print("Adding  "+song_name+" to the Music Library")
                cursor.execute("INSERT INTO MusicFiles(file_name, directory_id, uniqueid) values(?, ?, ?)", (song_name, song_db_details["directory_id"], unique_song_hash))
                song_ids.append(cursor.lastrowid)

    def get_song_db_details(self, abs_song_path, directory):
        song_db_details = {}
        song_db_details["directory_id"] = self.get_directory_id(directory)
        unique_song_hash = hashlib.md5(abs_song_path.encode('utf-8')).hexdigest()[0:15]
        exists_check_result = self.check_if_exists(unique_song_hash, abs_song_path)
        song_db_details.update(exists_check_result)
        return song_db_details
    
    def get_directory_id(self, directory):
        with self.conn:
            existing_dir = self.conn.execute("SELECT id from MusicDirectories where directory = (?)", [directory]).fetchone()
            if existing_dir is None:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO MusicDirectories(directory) values(?)", [directory])
                return cursor.lastrowid
            return existing_dir[0]
        

    def check_if_exists(self, uniqueid, abs_song_path):
        with self.conn:
            existing_uniqueid = self.conn.execute("SELECT file_name from MusicFiles where uniqueid = (?)", [uniqueid]).fetchone()
            if existing_uniqueid is None:
                return {'exists': False, 'uniqueid': uniqueid}
            if os.path.basename(abs_song_path) == existing_uniqueid[0]:
                return {'exists': True}
            new_hash = hashlib.md5(abs_song_path.encode('utf-8')).hexdigest()[16:31]
            return {'exists':False, 'uniqueid': new_hash}
    
    def get_all_songs(self):
        with self.conn:
            songs = self.conn.execute("SELECT file_name from MusicFiles ORDER BY id ASC").fetchall()
            return songs

    def create_playlist(self, playlist_name):
        with self.conn:
            playlist = self.conn.execute("SELECT * from Playlists where playlist_name = (?)", [playlist_name]).fetchone()
            if playlist is not None:
                print("A playlist with the name ",playlist_name," already exists. Please use another name")
                return;
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Playlists(playlist_name) values(?)", [playlist_name])
            if cursor.lastrowid:
                print("Playlist ", playlist_name, "created successfully")
                return cursor.lastrowid
            print("Error while creating playlist. Please try again later.")

    def add_to_playlist(self, song_name, playlist_name):
        playlist_entry_details = self.get_playlist_entries(song_name, playlist_name)
        with self.conn:
            cursor = self.conn.cursor()
            music_id = playlist_entry_details["song_id"]
            playlist_id = playlist_entry_details["playlist_id"]
            playlist_res = cursor.execute("INSERT INTO PlaylistFiles(music_id, playlist_id) values(?,?)", (music_id, playlist_id))
            print("Added ", song_name, "to playlist ",playlist_name)

    def get_playlist_entries(self, song_name, playlist_name):
        if os.path.isfile(song_name):
            base_song_name = os.path.basename(song_name)
        else:
            base_song_name = song_name
        playlist_entry_details = {}
        with self.conn:
            playlist_details = self.conn.execute("SELECT * from Playlists where playlist_name = (?)", [playlist_name]).fetchone()
            if not playlist_details:
                print("Playlist named ", playlist_name," not found. Creating.")
                playlist_entry_details["playlist_id"] = self.create_playlist(playlist_name)
            else:
                playlist_entry_details["playlist_id"] = playlist_details[0]
            song_details = self.conn.execute("SELECT * from MusicFiles where file_name = (?)", [base_song_name]).fetchone()
            if song_details is None:
                if not os.path.isfile(song_name):
                    print("song ", song_name, "not found in either the music library or the path specified.")
                    return
                print("song ", song_name, "found, adding it to Music Library before adding it to playlist.")
                song_id_array = self.add_to_library([base_song_name], os.path.dirname(song_name))
                playlist_entry_details["song_id"] = song_id_array[0]
            else:
                playlist_entry_details["song_id"] = song_details[0]
        return playlist_entry_details

    def get_playlist_songs(self, playlist_name):
        with self.conn:
            playlist_id = self.conn.execute("SELECT id from Playlists where playlist_name = (?)", [playlist_name]).fetchone()
            if not playlist_id:
                print("Playlist named ", playlist_name," not found. Please create it")
                return
            songs = self.conn.execute("SELECT  md.directory, mf.file_name FROM MusicFiles mf join MusicDirectories md on mf.directory_id = md.id \
                    where mf.id IN(SELECT music_id from PlaylistFiles where playlist_id = (?))", [playlist_id[0]]).fetchall()
            return songs
