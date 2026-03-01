import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

# CONFIGURACIÓN
CLIENT_ID = beaalvval@hotmail.com
CLIENT_SECRET = <V4lder4s_88>

auth_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=auth_manager)


def extraer_id(url):
    match = re.search(r"playlist/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else url


def obtener_canciones(playlist_url):
    playlist_id = extraer_id(playlist_url)
    results = sp.playlist_tracks(playlist_id)
    canciones = set()

    for item in results["items"]:
        track = item["track"]
        if track:
            titulo = track["name"].strip().lower()
            artista = track["artists"][0]["name"].strip().lower()
            canciones.add((titulo, artista))

    return canciones


st.title("Spotify Playlist Comparator")

playlist_a = st.text_input("Enlace Playlist A")
playlist_b = st.text_input("Enlace Playlist B")

if st.button("Comparar"):
    try:
        set_a = obtener_canciones(playlist_a)
        set_b = obtener_canciones(playlist_b)

        comunes = set_a & set_b
        solo_a = set_a - set_b
        solo_b = set_b - set_a

        st.subheader("Canciones en común")
        for t, a in sorted(comunes):
            st.write(f"{t} — {a}")

        st.subheader("Solo en Playlist A")
        for t, a in sorted(solo_a):
            st.write(f"{t} — {a}")

        st.subheader("Solo en Playlist B")
        for t, a in sorted(solo_b):
            st.write(f"{t} — {a}")

    except Exception as e:
        st.error(str(e))
