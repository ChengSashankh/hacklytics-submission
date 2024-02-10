# import streamlit as st
# from streamlit_chat import message
# import folium
# from streamlit_folium import st_folium
# from main import search, OPTIONS_TEMPLATE
#
# # call to render Folium map in Streamlit
# st_data = st_folium(m, width=725)
#
# message("Let's find what you need. What is the service you're looking for?")
# search_term = "My arm hurts, and I think I need an xray"
# message(search_term, is_user=True)
#
# message("Sure, let's find that service for you.")
# result = search(search_term)
#
# # st.json(result.json())
# message(f"Do any of these {len(result.json())} look like what you're looking for?")
# for procedure in result.json():
#     message(OPTIONS_TEMPLATE.format(procedure['cpt_code'], procedure['metadata']['source']))
#
# message("")

import streamlit as st
import pandas as pd
import pydeck as pdk


# Placeholder for the search function - to be implemented
def search(query):
    # Assume this function returns a list of results based on the query
    return ["Result 1", "Result 2", "Result 3"]  # Example results

# Placeholder for the get_from_database function - to be implemented
def get_from_database(selection):
    # Assume this function returns a list of location coordinates based on the selection
    return [(34.0522, -118.2437, 'Hospital1', 'red'), (40.7128, -74.0060, 'Hospital2', 'red')]  # Example coordinates for locations

# Streamlit app
def main():
    st.title("Transparent Healthcare. For you.")

    # Step 1: Ask the user for their complaint
    user_complaint = st.text_input("What are you looking for today?")

    if user_complaint:
        # Step 2: Call the search function with the user complaint
        results = search(user_complaint)

        # Step 3: Display results and ask the user if any of them matches their query
        selected_result = st.selectbox("Do any of these procedures match what you're looking for?", results)

        if st.button("Yeah"):
            # Step 4: Call the get_from_database function with the selected result
            locations = get_from_database(selected_result)

            scatterplot_layer = pdk.Layer(
                type='ScatterplotLayer',
                id='scatterplot-layer',
                data=pd.DataFrame(locations, columns=['lat', 'lon', 'Location', 'fill_color']),
                pickable=True,
                get_position=['lon', 'lat'],
                get_radius=100,
                radius_min_pixels=15,
                radius_max_pixels=15,
                get_fill_color='fill_color',
                get_line_color=[128, 128, 128, 200],
                get_line_width=4000,
                stroked=True,
                filled=True,
                # opacity=opacity
            )
            # text_layer = pdk.Layer(
            #     type='TextLayer',
            #     id='text-layer',
            #     data=pd.DataFrame(locations, columns=['lat', 'lon', 'Location']),
            #     pickable=True,
            #     get_position=['longitude', 'latitude'],
            #     get_text='Location',
            #     # get_color=text_colour,
            #     billboard=False,
            #     get_size=18,
            #     get_angle=0,
            #     # Note that string constants in pydeck are explicitly passed as strings
            #     # This distinguishes them from columns in a data set
            #     get_text_anchor='"middle"',
            #     get_alignment_baseline='"center"'
            # )

            # Step 5: Plot the locations on the map
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    # mapboxApiAccessToken=settings.MAPBOX_ACCESS_TOKEN,
                    longitude=-118.4,
                    latitude=34,
                    zoom=5,
                    min_zoom=1,
                    max_zoom=5,
                    pitch=0
                ),
                layers=[scatterplot_layer],
                tooltip={
                    "html": "{Location}",
                    "style": {"color": "red"}}
            ))
            # st.map(data=pd.DataFrame(locations, columns=['lat', 'lon']), tooltip={"html": "{Location}, {Indicator}<br/>Year: {Year}, Value: {Value}<br/>{Units > Scale} in {Measurement}", "style": {"color": "white"}})

if __name__ == "__main__":
    main()


    def temp():
        result_dict = [{"desc": doc[0].page_content.split('\n')[1],
                        "cpt_code": doc[0].page_content.split('\n')[0].split('cpt_code: ')[-1],
                        "metadata": doc[0].metadata} for doc in result]
        codes = [r["cpt_code"] for r in result_dict]
        print(codes)
        locations = [l._asdict() for l in get_locations_using_cpt(codes)]
        return json.dumps(locations)