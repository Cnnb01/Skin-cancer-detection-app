import streamlit as st
import signup, home

# st.set_page_config(
#     page_title="Skin",
# )

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
    def run(self):
            app = st.selectbox(
                'Navigate',
                [app['title'] for app in self.apps]
            )
        
            for application in self.apps:
                if application['title'] == app:
                    application['function']()

app = MultiApp()
app.add_app("Home", home.app)
app.add_app("Signup", signup.app)

app.run()

#https://www.kaggle.com/datasets/hasinisadunikasilva/skincancerdetectiondcnn/data
