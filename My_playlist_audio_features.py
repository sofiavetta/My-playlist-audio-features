import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import seaborn as sns

#ID CREDENTIALS
cid = '...' #Your API client ID
secret = '...' #Your API secret ID 
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#PLAYLISTS IDS
playlist_id = '3WCDdRaZZRLOEUEm6kd8Jx' # Avetta Rules Playlist ID 

track_name = []
track_id = []
track_energy = []
track_danceability = []
track_valence = []

#REQUEST PLAYLIST DETAILS FROM SPOTIFY API
playlist = sp.playlist(playlist_id, fields=None, market=None)
print (playlist['owner']['display_name'])

for i, t in enumerate (playlist['tracks']['items']):
    track_name.append(playlist['tracks']['items'][i]['track']['name'])
    track_id.append(playlist['tracks']['items'][i]['track']['id'])

#REQUEST TRACK AUDIO FEATURES FROM SPOTIFT API
track_features = sp.audio_features(track_id)

sum_energy = 0
sum_danceability = 0
sum_valence = 0

for i, t in enumerate(track_features):
    track_energy.append(track_features[i]['energy'])
    track_danceability.append(track_features[i]['danceability'])
    track_valence.append(track_features[i]['valence'])
    sum_energy = track_energy[i] + sum_energy
    sum_danceability = track_danceability[i] + sum_danceability
    sum_valence = track_valence[i] + sum_valence

avg_energy = sum_energy / len(track_energy)
avg_daceability = sum_danceability / len (track_danceability)
avg_valence = sum_valence / len (track_valence)

#print (avg_energy)
#print (avg_daceability)
#print (avg_valence)

#LINE GRAPH
rcParams.update({'figure.autolayout': True})
df=pd.DataFrame({'xvalues': track_name, 'y1values': track_energy, 'y2values' : track_danceability, 'y3values' : track_valence, 'y4values' : avg_energy, 'y5values': avg_daceability, 'y6values' :avg_valence })
plt.style.use('seaborn-darkgrid')
plt.plot( 'xvalues', 'y1values', data=df, label='energy', color = 'red', marker = 'o')
plt.plot( 'xvalues', 'y4values', data=df, label='avg energy', color = 'red', linestyle = '--')
plt.plot( 'xvalues', 'y2values', data=df, label='danceability', color = 'gold', marker = 'o')
plt.plot( 'xvalues', 'y5values', data=df, label='avg danceability', color = 'gold', linestyle = '--')
plt.plot( 'xvalues', 'y3values', data=df, label='valence', color = 'skyblue', marker = 'o')
plt.plot( 'xvalues', 'y6values', data=df, label='avg valence', color = 'skyblue', linestyle = '--')
plt.xticks(rotation=90)
plt.title('Playlist audio features: ' + playlist['name'] + ' by ' + playlist['owner']['display_name'], fontsize = 25, color='gray')
plt.xlabel("Track", fontsize = 18)
plt.ylabel("Value", fontsize = 18)
plt.legend()
plt.show()

#HISTOGRAM GRAPH
df=pd.DataFrame({'y1values': track_energy, 'y2values' : track_danceability, 'y3values' : track_valence, 'y4values' : avg_energy, 'y5values': avg_daceability, 'y6values' :avg_valence })
#print (df)
sns.distplot( df["y1values"] , color="skyblue", label="energy")
sns.distplot( df["y2values"] , color="red", label="danceability")
sns.distplot( df["y3values"] , color="gold", label="valence")
plt.title('Histogram | Playlist audio features: ' + playlist['name'] + ' by ' + playlist['owner']['display_name'], fontsize = 25, color = 'gray')
plt.xlabel("value", fontsize = 18)
plt.ylabel("frequency", fontsize = 18)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=18)
plt.show()

