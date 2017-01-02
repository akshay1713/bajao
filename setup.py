import sqlite3, os, sys
import argparse
import yaml


bajao_db = "bajao.db"
conn = sqlite3.connect(bajao_db)
with conn:
    cursor = conn.cursor()
    cursor.execute("drop table if exists PlaylistFiles")
    cursor.execute("drop table if exists MusicFiles")
    cursor.execute("drop table if exists Playlists")
    cursor.execute("create table MusicFiles(id INTEGER PRIMARY KEY NOT NULL, full_name TEXT, uniqueid VARCHAR(32))")
    cursor.execute("create table Playlists(id INTEGER PRIMARY KEY NOT NULL, playlist_name)")
    cursor.execute("create table PlaylistFiles(id INTEGER PRIMARY KEY NOT NULL, music_id INT, playlist_id INT, \
    FOREIGN KEY (music_id) REFERENCES MusicFiles(id), FOREIGN KEY (playlist_id) REFERENCES Playlists(id))")

