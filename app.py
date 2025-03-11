import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    movie_data = response.json()
    movie_name = movie_data['title']
    movie_info_url = f"https://www.themoviedb.org/movie/{movie_id}"
    return movie_name, movie_info_url


def fetch_availability(movie_id):
    # Using the TMDb Watch Providers API to get streaming information
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key=8265bd1679663a7ea12ac168da84d2e8"
    response = requests.get(url)
    data = response.json()

    # The availability info comes from the 'results' dictionary
    if 'results' in data:
        available_platforms = []
        # Only considering the US availability (can be extended for other countries)
        if 'US' in data['results']:
            providers = data['results']['US'].get('flatrate', [])
            for provider in providers:
                available_platforms.append(provider['provider_name'])

        if not available_platforms:
            return "Not available on streaming platforms"
        return ", ".join(available_platforms)
    return "Not available on streaming platforms"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    movie_info_urls = []
    availability_info = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_name, movie_info_url = fetch_movie_details(movie_id)
        availability = fetch_availability(movie_id)
        recommended_movie_names.append(movie_name)
        recommended_movie_posters.append(fetch_poster(movie_id))
        movie_info_urls.append(movie_info_url)
        availability_info.append(availability)

    return recommended_movie_names, recommended_movie_posters, movie_info_urls, availability_info


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, movie_info_urls, availability_info = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.markdown(f"[More Info]({movie_info_urls[0]})")
        st.text(f"Available on: {availability_info[0]}")

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.markdown(f"[More Info]({movie_info_urls[1]})")
        st.text(f"Available on: {availability_info[1]}")

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.markdown(f"[More Info]({movie_info_urls[2]})")
        st.text(f"Available on: {availability_info[2]}")

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.markdown(f"[More Info]({movie_info_urls[3]})")
        st.text(f"Available on: {availability_info[3]}")

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.markdown(f"[More Info]({movie_info_urls[4]})")
        st.text(f"Available on: {availability_info[4]}")
