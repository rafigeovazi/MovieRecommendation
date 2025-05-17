import streamlit as st
import pickle
import requests
from login_page import login
import urlib.request

# Run login page
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    logged_in = login()
    if logged_in:
        st.experimental_rerun()
else:
    # -----------------------------
    # ✅ Main Page
    # -----------------------------
    st.title("🎬 Geosling's Movie Recommendation")
    st.write(f"Welcome, **{st.session_state.get('username', 'Unemployed')}**!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    # Function to fetch movie poster
    def fetch_poster(movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url).json()
        poster_path = data['poster_path']
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"

    movies = pickle.load(open("movie_list.pkl", 'rb'))
    movies_list = movies['title'].values
    similarity_url = "https://huggingface.co/datasets/Geosling/MovieRecommendation/resolve/main/similarity.pkl"
    with urllib.request.urlopen(similarity_url) as f:
        similarity = pickle.load(f)
   

    st.header("Absolute Cinema ✋🏻😶🤚🏻!")

    import streamlit.components.v1 as components
    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

    imageUrls = [
        fetch_poster(1632),
        fetch_poster(299536),
        fetch_poster(17455),
        fetch_poster(2830),
        fetch_poster(429422),
        fetch_poster(9722),
        fetch_poster(13972),
        fetch_poster(240),
        fetch_poster(155),
        fetch_poster(598),
        fetch_poster(914),
        fetch_poster(255709),
        fetch_poster(572154)
    ]

    imageCarouselComponent(imageUrls=imageUrls, height=200)
    selectvalue = st.selectbox("Select movie from dropdown", movies_list)

    def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = []
        recommended_posters = []
        for i in distance[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_posters

    if st.button("Show Recommend"):
        names, posters = recommend(selectvalue)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
