import sqlite3, os, sys
import argparse
import yaml

with open("config.yaml", "r") as config_ptr:
    config = yaml.load(config_ptr)
bajao_db = config["BAJAO_DB"]

if len(bajao_db) == 0:
    print("Please check if you have a valid config.yaml file")

conn = sqlite3.connect(bajao_db)
with conn:
    cursor = conn.cursor()
    cursor.execute("drop table if exists MusicDirectories")
    cursor.execute("drop table if exists PlaylistFiles")
    cursor.execute("drop table if exists MusicFiles")
    cursor.execute("drop table if exists Playlists")
    cursor.execute("create table MusicDirectories(id INTEGER PRIMARY KEY NOT NULL, directory TEXT)")
    cursor.execute("create virtual table MusicFiles USING fts4(file_name TEXT, uniqueid VARCHAR(32), directory_id INT, \
            FOREIGN KEY(directory_id) REFERENCES MusicDirectories(id))")
    cursor.execute("create table Playlists(id INTEGER PRIMARY KEY NOT NULL, playlist_name)")
    cursor.execute("create table PlaylistFiles(id INTEGER PRIMARY KEY NOT NULL, music_id INT, playlist_id INT, \
    FOREIGN KEY (music_id) REFERENCES MusicFiles(id), FOREIGN KEY (playlist_id) REFERENCES Playlists(id))")
    print("Setup completed. You can now start using the Music Player.")

