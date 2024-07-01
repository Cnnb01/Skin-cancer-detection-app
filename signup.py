#https://www.youtube.com/watch?v=pdzGoozLEHU&list=PLvRfcAN-QbYnxloydunJlfES_m6GblyEt&index=2
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import home

cred = credentials.Certificate('skindet-963bb-de14d3d13811.json')
firebase_admin.initialize_app(cred) #only run once

def app():
    if st.session_state.get('signout', False):
        home.app()
        return
    st.title('Welcome to :blue[Skidet]')
    # choice = st.selectbox('Login/SignUp', ['Login','Sign Up'])

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    
    def f():
        try:
            user = auth.get_user_by_email(email)
            st.write('Login Successfully')
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True
            st.experimental_rerun()
            
        except:
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    if not st.session_state['signedout']:
        choice = st.selectbox('Login/Signup', ['Login','Sign Up']) 

        if choice == 'Login':
            email = st.text_input('Email Adress')
            password = st.text_input('Password', type='password')
            st.button('Login', on_click=f)
        else:
            email = st.text_input('Email Adress')
            password = st.text_input('Password', type='password')
            username = st.text_input('Enter unique username')
            if st.button('Create my account'):
                user = auth.create_user(email = email, password = password, uid = username)
                st.success('Account created successfully!')
                st.markdown('You can now login using your email and password')

    if st.session_state.signout:
        # st.text('Name ' +st.session_state.username)
        st.text('Email ' +st.session_state.useremail)
        st.button('Sign out', on_click=t)
