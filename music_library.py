import sqlite3, os, sys
import argparse
import yaml, hashlib

class MusicLibrary():

    def __init__(self, music_db):
        self.music_db = music_db
        self.conn = sqlite3.connect(self.music_db)

    def add_to_library(self, directory, songs):
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
