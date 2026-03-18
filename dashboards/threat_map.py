import streamlit as st
import pydeck as pdk

def show_attack_map(df):

    if df.empty:
        st.warning("No data to display on the map")
        return

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_radius=150000,
        get_fill_color=[255, 0, 0],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1
    )

    deck = pdk.Deck(
        map_provider="carto",
        map_style="dark",
        initial_view_state=view_state,
        layers=[layer],
        tooltip={"text": "Country: {country}\nAttack: {attack_type}"}
    )

    st.pydeck_chart(deck)