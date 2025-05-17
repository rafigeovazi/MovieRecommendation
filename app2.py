import streamlit as st
import pickle
import requests
from login_page import login
import requests
import io

# Run login page
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    if login():
        st.experimental_rerun()  # Rerun aman, langsung masuk main page
    # -----------------------------
    # ✅ Main Page
    # -----------------------------
    st.title("🎬 Geosling's Movie Recommendation")
    st.write(f"Welcome, **{st.session_state.get('username', 'Unemployed')}**!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.just_logged_out = True
        st.experimental_rerun()

    if st.session_state.get("just_logged_out"):
        st.session_state.just_logged_out = False
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
    response = requests.get(similarity_url)
    similarity = pickle.load(io.BytesIO(response.content))

    st.write("Let's find your new fav movie Pal!!👊")

    import streamlit.components.v1 as components
    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

    imageUrls = [
        fetch_poster(157336),
        fetch_poster(37799),   
        fetch_poster(693134),      
        fetch_poster(155),  
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
