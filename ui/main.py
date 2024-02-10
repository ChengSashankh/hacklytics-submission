from typing import List

import streamlit as st
import requests
from sqlalchemy.orm import DeclarativeBase

OPTIONS_TEMPLATE = """
### {}

{}

</div>"""

def main():
    menu = ["Home", "About"]
    # choice = st.sidebar.selectbox("Menu", menu)

    st.title("Transparency. For you")

    # if choice == 'Home':
    # st.subheader("Home")
    # Search box

    with st.form(key='search'):
        nav1, nav2, nav3 = st.columns([3, 2, 1])

        with nav1:
            search_term = st.text_input("Ask Healthlytics!")

        with nav2:
            location = st.text_input("Location")

        with nav3:
            st.text("Search")
            submit_search = st.form_submit_button("Go")

    # Results
    col1, col2 = st.columns([2, 1])

    with col1:
        if submit_search:
            # center on Liberty Bell, add marker
            result = search(search_term)
            # st.json(result.json())
            st.write(f"Do any of these {len(result.json())} look like what you're looking for?")

            for procedure in result.json():
                st.markdown(OPTIONS_TEMPLATE.format(procedure['cpt_code'], procedure['metadata']['source']), unsafe_allow_html=True)
    # elif choice == 'About':
    #     st.subheader("About")


def search(query: str):
    return requests.post("http://127.0.0.1:5000/search", json={"query": query})

if __name__ == "__main__":
    main()