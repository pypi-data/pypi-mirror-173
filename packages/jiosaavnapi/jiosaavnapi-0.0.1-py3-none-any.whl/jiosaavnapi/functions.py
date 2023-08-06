from pyDes import *
import base64

class Functions: ## Contains commonly used functions.
    ### From https://github.com/cyberboysumanjay/JioSaavnAPI/blob/12f325d9264d21f61abeddc2dd86860937a347f8/helper.py#L58-L63
    def decrypt_stream_url(self, stream_url: str) -> str:
        des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",pad=None, padmode=PAD_PKCS5)
        enc_url = base64.b64decode(stream_url.strip())
        dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
        dec_url = dec_url.replace("_96.mp4", "_320.mp4")
        return dec_url

    def format_stream_url(self, stream_url: str, kbps320: bool) -> str:
        stream_url = stream_url.replace("preview", "aac")
        if kbps320 == True:
            stream_url = stream_url.replace("_96_p", "_320") ## If the song is 320kbps, provide the 320kbps link.
        else:
            stream_url = stream_url.replace("_96_p", "_160") ## Else, default to 160kbps.
        return stream_url

    def is_explicit(self, value: int) -> bool:
        if value == 1:
            return True
        else:
            return False

    def get_primary_artists(self, artist_json: list) -> str:
        primary_artists = []
        for i in artist_json:
            primary_artists.append(i['name']) ## Collect the names of all the primary artists.
        return ', '.join(primary_artists)

    def get_primary_artists_ids(self, artist_json: list) -> str:
        primary_artists_ids = []
        for i in artist_json:
            primary_artists_ids.append(i['id']) ## Collect the id's of all the primary artists.
        return ', '.join(primary_artists_ids)

    def get_primary_artists_urls(self, artist_json: list) -> str:
        primary_artists_urls = []
        for i in artist_json:
            primary_artists_urls.append(i['perma_url']) ## Collect the urls of all the primary artists.
        return ', '.join(primary_artists_urls)

    def get_featured_artists(self, artist_json: list) -> str:
        if artist_json is None: ## Some songs don't have featured artists.
            return None
        featured_artists = []
        for i in artist_json:
            featured_artists.append(i['name']) ## Collect the names of all the featured artists.
        return ', '.join(featured_artists)

    def get_featured_artists_ids(self, artist_json: list) -> str:
        if artist_json is None:
            return None
        featured_artists_ids = []
        for i in artist_json:
            featured_artists_ids.append(i['id']) ## Collect the id's of all the featured artists.
        return ', '.join(featured_artists_ids)

    def get_featured_artists_urls(self, artist_json: list) -> str:
        if artist_json is None:
            return None
        featured_artists_urls = []
        for i in artist_json:
            featured_artists_urls.append(i['perma_url']) ## Collect the urls of all the featured artists.
        return ', '.join(featured_artists_urls)