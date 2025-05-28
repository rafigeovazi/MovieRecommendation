import streamlit as st
from auth import login_user, register_user

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    st.image("logo.jpg", width=700)
    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["🔐 Login", "🦇 Register"])

        with tab1:
            st.subheader("Login Pageeeeeeee")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", key="login_btn"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.just_logged_in = True
                    st.success("🦸 Login successful!")
                else:
                    st.error("Identity not recognized. Are you a villain?")

        with tab2:
            st.subheader("Register as a New Hero")
            new_user = st.text_input("Username", key="reg_user")
            new_pass = st.text_input("Password", type="password", key="reg_pass")
            if st.button("Register"):
                if register_user(new_user, new_pass):
                    st.success("Registration complete! Go to Login page.")
                else:
                    st.warning("Hero already exists. Try a different username.")
        return False

    return True
