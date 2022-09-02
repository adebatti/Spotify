import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
#https://www.youtube.com/watch?v=jSOrEmKUd_c

scope = 'playlist-modify-public'
username = '12145383885'

token = SpotifyOAuth(scope=scope,username=username)
spotifyObject = spotipy.Spotify(auth_manager = token)

#find playlist uri
playlist_name_user_input = input('Enter the name of your playlist: ').lower()
playlist_name = ''
i = 0
while (playlist_name.lower() != playlist_name_user_input):
    pre_user_playlists = spotifyObject.current_user_playlists(limit=i+1,offset=i) #only gets past 100 playlists
    #print(json.dumps(pre_user_playlists,sort_keys=4,indent=4))
    playlist_name = pre_user_playlists['items'][0]['name']
    i += 1
playlist_uri = pre_user_playlists['items'][0]['uri']
#print('Playlist Name: ' + playlist_name)
#print('Playlist URI: ' + playlist_uri)

#get tracks
pre_playlist_tracks = spotifyObject.playlist_tracks(playlist_id=playlist_uri)['items']
#print(json.dumps(pre_playlist_tracks,sort_keys=4,indent=4))
playlist_tracks = []
for track in pre_playlist_tracks:
    #track_name = track['track']['name']
    track_uri = track['track']['uri']
    artist_uris = []
    track_artists = track['track']['artists']
    for artist in track_artists:
        artist_uri = artist['uri']
        artist_uris.append(artist_uri)
    playlist_tracks.append({'track uri':track_uri,'artist uris':artist_uris})
#print(playlist_tracks)
# find genre occurances for each artist
pre_genres = []
for playlist_track in playlist_tracks:
    pre_artists = spotifyObject.artists(playlist_track['artist uris'])['artists']
    #print(json.dumps(pre_artists,sort_keys=4,indent=4))
    for artist in pre_artists:
        pre_genres.append([artist['genres'],playlist_track['track uri']])
    



genres = {}
for artist_genres in pre_genres:
    for genre in artist_genres[0]:
        if genre in genres:
            genres[genre].append(artist_genres[1])
        else:
            genres[genre] = [artist_genres[1]]

sorted_genres_keys = sorted(genres, key=lambda genre: len(genres[genre]), reverse=True)
sorted_genres = {key: {'size':len(genres[key]),'track uris':genres[key]} for key in sorted_genres_keys}

#print(sorted_genres)
print('This playlist is comprised of the following genres:')

for genre in sorted_genres:
    if sorted_genres[genre]['size'] <= 5:
        print(genre + ': ' + str(sorted_genres[genre]['size']) + ' songs')

""" for genre in sorted_genres:
    sorted_genres[genre] = [*set(sorted_genres[genre])]
    if sorted_genres[genre]['size'] > 10:
        print(genre + ': ' + str(sorted_genres[genre]['size']) + ' songs') """

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




""" track_artists = track['track']['artists']
    for artist in track_artists:
        track_artist_name = artist['name']
        track_artist_uri = artist['uri']
        look up genres related to artist
        track_artist_genres = """ """

# go through track artist genres and make dict w key being genre and value being list of song uri. length of each list will tell how many songs fit certain genre. reorder from longest to shortest and ask user which genres theyd like to make playlists abt
#{{song_name:'song name',song_uri:123,artists:['artist1','artist2'],genres:[genre1,genre2,genre3]}}
#genre_occurance = {genre1:2,genre2:5:10,genre4:4,genre5:1}

#user_playlists = {pre_user_playlists['items'][:]['name']:pre_user_playlists['items'][:]['name']} #search in the dict babes <3
#searched_playlist = spotifyObject.search(q=playlist_name_user_input,limit=1,offset=0,type='playlist',market=None)
#large_playlist = searched_playlist[]
#add bit about if playlist doesnt exit and also verifying w user thtcorrect but for now we bool
#print(searched_playlist)

""" #create the playlist 
""" playlist_name = input('Enter a playlist name: ') # CHANGE
playlist_description = input('Enter a playlist description: ') # CHANGE

spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True,description=playlist_description)"""

# CHANGE NEXT CHUNK
""" user_input = input('Enter the song: ')
list_of_songs = []

while user_input != 'quit':
    result = spotifyObject.search(q=user_input)
    #print(json.dumps(result,sort_keys=4,indent=4)) # NOTE THIS
    list_of_songs.append(result['tracks']['items'][0]['uri'])
    user_input = input('Enter the song: ')

#find the new playlist
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

#add songs
spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_songs)  """