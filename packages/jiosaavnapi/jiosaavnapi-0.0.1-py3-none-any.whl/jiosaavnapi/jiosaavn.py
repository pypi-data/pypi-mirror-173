import requests
from jiosaavnapi import endpoints
from jiosaavnapi.songs.songs import Songs
from jiosaavnapi.albums.albums import Albums
from jiosaavnapi.playlists.playlists import Playlists
from jiosaavnapi.artists.artists import Artists
from jiosaavnapi.functions import Functions

class JioSaavn(Songs, Albums, Playlists, Artists, Functions): ## Inherit all classes.
    """Class containing all objects for jiosaavnapi. 
    Allows to perform various requests in order to search get info on: Songs, Albums, Playlists and Artists.
    
    Available options: 

    search_songs: Allows to search Jiosaavn for tracks.
    search_albums: Allows to search Jiosaavn for albums.
    search_playlists:Allows to search Jiosaavn for playlists.
    song_info: Retrieve info on a track using it's track_id.
    album_info: Retrieve info on an album using it's album_id.
    playlist_info: Retrieve info on a playlist using it's playlist_id.
    """
    def __init__(self):
        self.requests = requests.Session() ## Use the same request session for all functions.
        self.endpoints = endpoints ## API endpoints.