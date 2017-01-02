import sqlite3, os, sys
import argparse
import yaml, hashlib

class MusicLibrary():

    def __init__(self, music_db):
        self.music_db = music_db
        self.conn = sqlite3.connect(self.music_db)

    def add_to_library(self, songs):
        with self.conn:
            cursor = self.conn.cursor()
            for song in songs:
                abs_song_path = os.path.abspath(song)
                unique_song_hash = hashlib.md5(abs_song_path.encode('utf-8')).hexdigest()[0:15]
                exists_check_result = self.check_if_exists(unique_song_hash, abs_song_path)
                if exists_check_result["exists"]:
                    print("The song "+os.path.basename(abs_song_path) +" already exists in the database")
                    continue
                unique_song_hash = exists_check_result["uniqueid"]
                print("inserting "+abs_song_path)
                cursor.execute("INSERT INTO MusicFiles(full_name, uniqueid) values(?, ?)", (abs_song_path, unique_song_hash))

    def check_if_exists(self, uniqueid, abs_song_path):
        with self.conn:
            existing_uniqueid = self.conn.execute("SELECT full_name from MusicFiles where uniqueid = (?)", [uniqueid]).fetchone()
            if existing_uniqueid is None:
                return {'exists': False, 'uniqueid': uniqueid}
            if abs_song_path == existing_uniqueid[0]:
                return {'exists': True}
            new_hash = hashlib.md5(abs_song_path.encode('utf-8')).hexdigest()[16:31]
            return {'exists':False, 'uniqueid': new_hash}
