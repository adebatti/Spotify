import code
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
#Loosely based on this tutorial --> https://www.youtube.com/watch?v=jSOrEmKUd_c
#print(json.dumps(pre_playlist_tracks,sort_keys=4,indent=4)) <-- helpful

""" 
TASKS:
- get rid of redundant code
- fix issue where songs are being added more than once 
- make more efficient
- make modular 
"""

scope = 'playlist-modify-public'
username = '12145383885'

token = SpotifyOAuth(scope=scope,username=username)
spotifyObject = spotipy.Spotify(auth_manager = token)

#Ask user for name of playlist to split
playlist_name_user_input = input('Enter the name of your playlist: ').lower()

#Parse through user playlists to find most recently created playlist with matching name and retrive URI
playlist_name = ''
i = 0
while (playlist_name.lower() != playlist_name_user_input):
    pre_user_playlists = spotifyObject.current_user_playlists(limit=i+1,offset=i) #Current playlist information  
    playlist_name = pre_user_playlists['items'][0]['name'] #Current playlist name 
    i += 1
    # POSSIBLE BUG: if no playlist matches user input. 
playlist_uri = pre_user_playlists['items'][0]['uri'] #Playlist URI 


#Get playlist track information (track and main artist uri)
pre_playlist_tracks = spotifyObject.playlist_tracks(playlist_id=playlist_uri)['items'] #Playlist track information
playlist_tracks_data = []
for pre_playlist_track in pre_playlist_tracks:
    #track_name = track['track']['name']
    track_uri = pre_playlist_track['track']['uri']
    artist_uri = pre_playlist_track['track']['artists'][0]['uri'] #only getting first artist as they probably most representative of genre and saves time
    playlist_tracks_data.append({'track uri':track_uri,'artist uri':artist_uri})

#CLEANED UP TO HERE

# find genre occurances for each artist
pre_genres = []
for playlist_track in playlist_tracks_data:
    pre_artists = spotifyObject.artists(playlist_track['artist uris'])['artists']


genres = {}
for artist_genres in pre_genres:
    for genre in artist_genres[0]:
        if genre in genres:
            genres[genre].append(artist_genres[1])
        else:
            genres[genre] = [artist_genres[1]]

sorted_genres_keys = sorted(genres, key=lambda genre: len(genres[genre]), reverse=True)
sorted_genres = {key: {'size':len(genres[key]),'track uris':genres[key]} for key in sorted_genres_keys}

print(playlist_name + ' is comprised of the following genres:')

for genre in sorted_genres:
    if sorted_genres[genre]['size'] <= 5:
        print(genre + ': ' + str(sorted_genres[genre]['size']) + ' songs')

playlist_genre = ''
while playlist_genre != 'quit':
    playlist_genre = input('Which genre would you like to create a playlist of? ')
    if playlist_genre == 'quit':
        continue 
    playlist_name = playlist_name_user_input + ' (' + playlist_genre + ')'
    spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True)
    #maybe add a descriptopm
    prePlaylist = spotifyObject.user_playlists(user=username)
    playlist = prePlaylist['items'][0]['id']
    spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=genres[playlist_genre])
#add catch for incorect spelling and whatnot 

