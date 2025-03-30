# DS4200 Final Project Group 28 

**Research Topic:** Spotify Music Trends

**Data link:** [Kaggle](https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset/data)

**Group Members:** Misha Ankudovych, Samantha Cheung, Rylin Lubash


## About The Project
Music is an ever-evolving form of art, mirroring cultural shifts over time. Analyzing the history of music can highlight the influence of technology and the shifting popularity of different sounds. With streaming platforms like Spotify, we can analyze these changes by examining features such as danceability, energy, and genres. Through a mix of interactive and static data visualizations, this website explores the evolution of music, uncovering how musical styles shift across decades.

**Background**

The project starts off by providing a high level overview into the breakdown of music on Spotify; with a Sankey diagram that shows the proportion of artists and their primary genre of releases by decade. Building on this idea, the network chart explores the relationships between different genres on Spotify by showing how often they co-occur.

**Music Attribute Trends**

Then, with a background on genres and music on spotify, the next segment explores how the prevalence of the different musical attributes has changed over time. Starting with the line chart, which shows all the attributes and their average value over the years.

Building on that idea, the bar chart goes further to show what musical attributes the average song in each decade had, showing how this has changed over time.

**Popularity Analysis**

With all of that context, the final visualization is a scatter plot that explores the relationship between the value for each musical attribute in a song, and its current popularity on Spotify.

All in all: this project walks you through how music is related on Spotify, how the typical song has changed over time, and how a song's attributes relate to its current popularity.

## About the Data
The dataset is sourced from Spotify’s API and published on Kaggle. It includes a number of categorical and quantitative data points. In the dataset, there are a number of different views, with data from 1921 to 2020. They include data on specific songs, as well as averaged by genre, year, and artist. The full dataset features this information for over 170,000 songs, and there are 19 total attributes for each. This project will focus mainly on the songs data, which includes data on each song, such as genre, artists, release date and popularity. It also includes ‘vibe’ based metrics about the song, which are defined in detail below. We focused on these attributes of songs that capture aspects that make people like specific songs over others. Musical Attributes:

All attributes are scored on a scale from 0.0 to 1.0, and determined by the Spotify Algorithm. 

**Speechiness** - The presence of spoken words in a track. The more exclusively speech-like the recording, the higher the value. Values above 0.66 describe tracks that are likely entirely spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, including rap music. Values below 0.33 are likely only music.

**Acousticness** - A confidence measure of whether the track is acoustic, where 1.0 is highly likely to be acoustic.

**Liveness** - Detects the presence of an audience in the recording. A value above 0.8 provides strong likelihood that the track was performed live.

**Danceability** - How suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity, higher values being more danceable.

**Valence** - A measure of the musical positiveness conveyed by a track. Tracks with high valence values sound more positive, while tracks with low valence sound more negative.

**Instrumentalness**- Predicts whether a track contains no vocals, values above 0.5 having a good likelihood of containing no vocal content. Vocals here refers to words, not sounds such as “ooh” and “aah”.

The data included a massive pull from the Spotify API, **with over 170,000 songs,made by almost 29,000 artists, seperated into almsot 3,000 genres.**
