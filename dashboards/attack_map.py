import streamlit as st
import pydeck as pdk

def show_attack_map(df):

    view_state = pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1.2,
        pitch=45
    )

    arc_layer = pdk.Layer(
        "ArcLayer",
        data=df,
        get_source_position='[lon, lat]',
        get_target_position='[46.67,24.71]',
        get_source_color='[255,0,0]',
        get_target_color='[0,255,255]',
        pickable=True
    )

    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=[arc_layer],
        tooltip={"text":"Attack from {country}"}
    )

    st.pydeck_chart(deck)