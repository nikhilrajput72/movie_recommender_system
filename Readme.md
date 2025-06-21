# Movie Recommender System

This is a content-based movie recommendation system developed using Python and Streamlit. It allows users to select a movie and receive similar movie suggestions based on precomputed similarity scores. The application fetches additional information such as posters, metadata, and trailers using external APIs and displays it in a visually styled interface inspired by IMDb.

## Overview

The application provides:

- A user-friendly interface to select or search for a movie.
- Real-time movie metadata (poster, plot, genre, director, actors) fetched from the OMDb API.
- Trailers embedded from YouTube using the YouTube Data API.
- Content-based recommendations using cosine similarity between movies.
- Custom HTML/CSS styling to mimic the layout and aesthetics of IMDb.
- Clickable movie posters that navigate to detailed views for seamless exploration.

## Features

- Dropdown selection for movie titles.
- Dynamic content rendering with poster, trailer, and full movie information.
- Embedded YouTube trailers based on movie titles.
- Recommendations generated using a machine learning similarity matrix.
- Responsive layout with hover effects and dark theme styling.

## Technology Stack

| Component       | Description                              |
|------------------|------------------------------------------|
| Python           | Core programming language                |
| Streamlit        | Web application framework                |
| Pandas           | Data manipulation and analysis           |
| Pickle           | Serialized ML data (movies and similarity) |
| OMDb API         | Fetch movie metadata and posters         |
| YouTube Data API | Fetch YouTube trailer links              |
| HTML/CSS         | Custom styling and layout                |



