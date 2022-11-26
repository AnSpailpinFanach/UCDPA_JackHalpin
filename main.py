# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#import python packages
import numpy as np
import pandas as pd
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sns

def categorise(row):
    if row['year'] >= 2010:
        return "The Tens"
    elif row['year'] <2010:
        return "The Noughties"

def runAnalysis():
    ### PREPERATION ###
    Spotify_df = pd.read_csv('songs_normalize.csv')
    dupes = Spotify_df[Spotify_df.duplicated(keep=False)]
    # Sorting the duplicate dataset to see the dupes in order
    dupes_sorted = dupes.sort_values(by=['song'], ascending=True)
    # dropping the duplicate values
    Spotify_df_no_dupes = Spotify_df
    Spotify_df_no_dupes.drop_duplicates(inplace=True)

    Spotify_years_drop = Spotify_df_no_dupes[
        (Spotify_df_no_dupes['year'] < 2000) | (Spotify_df_no_dupes['year'] > 2019)].index

    # remove rows from dataset based on a condition
    Spotify_analysis = Spotify_df_no_dupes.drop(Spotify_years_drop)

    Spotify_oos = pd.read_csv('songs_outofscope.csv')

    # Concatenating DataFrames together & checking shape matched the original dataset
    Spotify_joined = pd.concat([Spotify_analysis, Spotify_oos])

    Spotify_analysis = Spotify_analysis.sort_values(by=['year'], ascending=True)

    Spotify_analysis['Period'] = Spotify_analysis.apply(lambda row: categorise(row), axis=1)

    ### ANALYSIS
    insights_dictonary = {}
    most_popular = Spotify_analysis.query('popularity>=75', inplace=False).sort_values('popularity', ascending=False)
    insights_dictonary['insight_1'] = {'most_popular': most_popular}
    least_popular = Spotify_analysis.query('popularity<=5', inplace=False).sort_values('popularity', ascending=False)
    insights_dictonary['insight_1'] = {'least_popular': least_popular}

    artist = Spotify_analysis['artist'].value_counts()
    insights_dictonary['insight_2'] = {'artist': artist}

    tp_artists_songs = artist[:5]
    tp_artists_name = artist[:5].index
    fig = plt.figure(figsize=(10, 5))
    plt.bar(tp_artists_name, tp_artists_songs, width=0.4, color="dodgerblue")
    plt.xlabel("Artists")
    plt.ylabel("No of Songs")
    plt.title('Top Artists with Hit Songs', color='red', fontsize=20)
    plt.show()

    # Used groupedby function for artists
    songs_by_artist = Spotify_analysis.groupby('artist', as_index=False)['song'] \
        .count().sort_values(['song'], ascending=False)

    insights_dictonary['insight_2'] = {'songs_by_artist': songs_by_artist}

    # Thereafter looked at the top artists by 'popularity' which showcases the different popularity of each song
    popularity_by_artist = Spotify_analysis.groupby('artist', as_index=False)['popularity'] \
        .sum().sort_values(['popularity'], ascending=False)

    insights_dictonary['insight_2'] = {'popularity_by_artist': popularity_by_artist}

    # I then wanted join a dataframe for the amount of hit songs and the popularity
    pop_and_hits_by_artist = pd.merge(popularity_by_artist, \
                                      songs_by_artist, \
                                      on='artist', \
                                      how='outer')

    insights_dictonary['insight_2'] = {'pop_and_hits_by_artist': pop_and_hits_by_artist}

    pop_and_hits_by_artist['song'] = pop_and_hits_by_artist['song'].astype('Int64')
    pop_and_hits_by_artist['popularity'] = pop_and_hits_by_artist['popularity'].astype('Int64')

    # pop_and_hits_by_artist.set_index('artist',inplace=True)

    pop_and_hits_by_artist = insights_dictonary['insight_2']['pop_and_hits_by_artist'].head(10)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runAnalysis

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
