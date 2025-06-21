import streamlit as st
import pandas as pd
import pickle
import requests

# Fetch movie details from OMDb API
@st.cache_data
def fetch_movie_details(movie_title):
    url = f"http://www.omdbapi.com/?apikey=7b5b2fbb&t={movie_title}"
    data = requests.get(url)
    return data.json()

# Search for trailers on YouTube
def fetch_trailer_url(movie_title):
    youtube_api_key = 'AIzaSyCs9m0FMbdcoz_w9whkW8gcP23f-csIGgo'  
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={movie_title} trailer&type=video&key={youtube_api_key}"
    response = requests.get(search_url)
    results = response.json()
    
    if 'items' in results and len(results['items']) > 0:
        video_id = results['items'][0]['id']['videoId']
        return f"https://www.youtube.com/embed/{video_id}"
    return None

# Define the recommend function
def recommend(movie, num_recommendations=5):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(enumerate(distance), reverse=True, key=lambda x: x[1])[1:num_recommendations + 1]
    
    recommended_movies = []
    recommended_posters = []
    
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))
        
    return recommended_movies, recommended_posters

# Fetch movie poster from OMDb API
def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?apikey=7b5b2fbb&t={movie_title}"
    data = requests.get(url)
    data = data.json()
    poster_url = data.get('Poster', 'https://via.placeholder.com/150')  # Fallback poster if not found
    return poster_url

# Function to show movie details
def show_movie_details(movie_data):
    trailer_url = fetch_trailer_url(movie_data['Title'])
    
    st.markdown(
        f"""
        <style>
        .movie-details {{
            display: flex;
            flex-direction: column;
            background-color: #141414;
            border-radius: 12px;
            padding: 20px;
            color: #e0e0e0;
            font-family: 'Arial', sans-serif;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
        }}
        
        .movie-header {{
            margin-bottom: 20px;
        }}

        .movie-header h1 {{
            color: #f5c518;
            font-size: 2rem;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        
        .movie-content {{
            display: flex;
            flex-direction: row;
        }}
        
        .movie-content .movie-poster {{
            flex: 1;
            margin-right: 20px;
        }}
        
        .movie-content .movie-poster img {{
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
            width: 100%;
            max-width: 300px;
            transition: transform 0.3s;
        }}
        
        .movie-content .movie-poster:hover img {{
            transform: scale(1.1);
        }}
        
        .movie-content .movie-trailer {{
            flex: 1;
            border: 2px solid #f5c518;
            border-radius: 8px;
            padding: 10px;
            transition: transform 0.3s;
        }}
        
        .movie-content .movie-trailer iframe {{
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
            width: 100%;
            height: 315px;
        }}
        
        .movie-content .movie-trailer:hover {{
            transform: scale(1.05);
        }}
        
        .movie-info {{
            background-color: #1c1c1c;
            border-radius: 8px;
            padding: 20px;
        }}
        
        .movie-info p {{
            color: #e0e0e0;
            font-size: 1rem;
            margin-bottom: 8px;
        }}
        
        .movie-info p strong {{
            color: #f5c518;
        }}
        
        .movie-info a {{
            color: #f5c518;
            text-decoration: none;
            font-weight: bold;
        }}
        
        .movie-info a:hover {{
            color: #ffffff;
            text-decoration: underline;
        }}

        .zoom {{
            transition: transform 0.2s;
        }}

        .zoom:hover {{
            transform: scale(1.2);
        }}

        .poster-container {{
            text-align: center;
        }}
        
        .trailer-container {{
            text-align: center;
        }}
        
        .trailer-container iframe {{
            transition: transform 0.3s;
        }}

        .trailer-container:hover iframe {{
            transform: scale(1.05);
        }}

        .recommendations {{
            margin-top: 40px;
            background-color: #1c1c1c;
            border-radius: 8px;
            padding: 20px;
        }}

        .recommendations h2 {{
            color: #f5c518;
            font-size: 1.5rem;
            margin-bottom: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="movie-details">
        <div class="movie-header">
            <h1>{movie_data['Title']}</h1>
        </div>
        <div class="movie-content">
            <div class="movie-poster">
                <img src="{movie_data['Poster']}" alt="{movie_data['Title']} poster">
            </div>
            <div class="movie-trailer">
                {f'<iframe src="{trailer_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' if trailer_url else '<p>No trailer available</p>'}
            </div>
        </div>
        <div class="movie-info">
            <p><strong>Year:</strong> {movie_data['Year']}</p>
            <p><strong>Genre:</strong> {movie_data['Genre']}</p>
            <p><strong>Director:</strong> {movie_data['Director']}</p>
            <p><strong>Actors:</strong> {movie_data['Actors']}</p>
            <p><strong>Plot:</strong> {movie_data['Plot']}</p>
            <p><a href="https://www.imdb.com/title/{movie_data['imdbID']}" target="_blank">View on IMDb</a></p>
        </div>
        <div class="back-button">
            <a href="/" style="text-decoration: none;">
                <button style="
                    background-color: #f5c518;
                    border: none;
                    color: #141414;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 10px 0;
                    cursor: pointer;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                ">Return </button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch more recommendations
    recommended_movie_names, recommended_movie_posters = recommend(movie_data['Title'], num_recommendations=6)
    
    st.markdown(f"""
    <div class="recommendations">
        <h2>More Recommendations</h2>
        <div class="recommendation-items">
            {''.join(f'<div class="poster-container" style="display: inline-block; margin: 10px;"><a href="?movie={name}"><img src="{poster}" class="zoom" width="150"></a><p>{name}</p></div>' for name, poster in zip(recommended_movie_names, recommended_movie_posters))}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Custom CSS for hover effect on all posters and trailers
st.markdown(
    """
    <style>
    .zoom {
        transition: transform 0.2s;
    }

    .zoom:hover {
        transform: scale(1.2);
    }

    .poster-container {
        text-align: center;
    }
    
    .trailer-container {
        text-align: center;
    }
    
    .trailer-container iframe {
        transition: transform 0.3s;
    }

    .trailer-container:hover iframe {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the movie data and similarity matrix
movies_dict = pickle.load(open(r'C:\Users\Nikhil\Downloads\Machine learning projects\movie_recommender_system\movie_list.pkl', 'rb'))
similarity = pickle.load(open(r'C:\Users\Nikhil\Downloads\Machine learning projects\movie_recommender_system\similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

# Routing Logic
query_params = st.query_params





if 'movie' in query_params:
    movie_title = query_params['movie']
    
    movie_details = fetch_movie_details(movie_title)
    
    show_movie_details(movie_details)


else:
    st.header('Movie Recommender System')

    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movies['title'].values
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, num_recommendations=5)  # Hardcoded number of recommendations
        
        cols = st.columns(len(recommended_movie_names))
        for col, movie_name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                 if st.markdown(
                    f'''
                    <div class="poster-container">
                        <a href="?movie={movie_name}">
                            <img src="{poster}" class="zoom" width="150">
                        </a>
                    </div>
                    ''', 
                    unsafe_allow_html=True
                ):
                   st.text(movie_name)
                   pass
