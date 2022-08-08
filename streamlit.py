import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
from vega_datasets import data

dataset = pd.read_csv('dataset.csv')
world_count = pd.read_csv('world_count.csv')
usa = pd.read_csv('usa.csv')
usa_count = pd.read_csv('usa_count.csv')
rest_of_world = pd.read_csv('rest_of_world.csv')

def main_page():
    st.markdown("## UFO Report Worldwide 👽")
    st.write("Move the slider for rotation and hover over for more info.")

    countries = alt.topo_feature(data.world_110m.url, 'countries')

    values = st.slider(
     'Rotate',
        -180.0, 180.0, 0.0, 5.0)

    background = alt.Chart(countries).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project(
        type= 'orthographic',
        rotate= [-values, -10 ,0]
    ).properties(
        width=1000,
        height=600
    )


    mapping = alt.Chart(countries).mark_geoshape().encode(
        color=alt.Color('count:Q', title='UFO Sightings', scale=alt.Scale(domain=[0,100,700,70000],scheme='inferno')),
        tooltip=['Country:N', 'count:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(world_count, 'Code', ['count', 'Country'])  
    )

    st.altair_chart((background + mapping).interactive(), use_container_width=True)

def page2():

    st.markdown("## UFO Report US 👽")
    st.write("Hover over for more info.")

    states = alt.topo_feature(data.us_10m.url, feature='states')

    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        title='UFO Sightings since 1949 in USA per State',
        width=1000,
        height=600
    )

    mapping = alt.Chart(states).mark_geoshape().encode(
        color=alt.Color('count:Q', title='UFO Sightings', scale=alt.Scale(domain=[0,1000,10000],scheme='magma')),
        tooltip=['State:N', 'count:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(usa_count, 'Code', ['count', 'State'])
    
    )

    st.altair_chart(background + mapping, use_container_width=True)

def page3():
    
    st.markdown("## UFO Report over the years 👽")
    st.write("Move the slider to explore the years and hover over for more info.")

    year = st.slider(
     'Year', 1950, 2014, step=1)

    current = rest_of_world[rest_of_world.Year == year]

    hist = alt.Chart(current).transform_window(
        rank='rank(Count)',
        sort=[alt.SortField('Count', order='descending')]
    ).mark_bar().encode(
        y=alt.Y('Area:N', sort='-x'),
        x='Count:Q',
        color= alt.Color('Area:N', sort='-x', scale=alt.Scale(scheme='greenblue'), legend=None),
        tooltip=['Area:N', 'Count:Q']
    ).properties(
        width=700,
        height=600
    )

    st.altair_chart(hist)
    

def page4():
    st.write("## About page❓")
    st.write('#### This report includes more than 80.000 sightings of UFOs over the last century.')
    st.write('Source: [https://www.kaggle.com/datasets/NUFORC/ufo-sightings](https://www.kaggle.com/datasets/NUFORC/ufo-sightings)')
    st.write('### Pages Description')
    st.write('Page 1: Worldwide')
    st.write("This page includes an orthographic view of the world with sighting count per country. This visualization can be rotated by slider and includes a tooltip with country name and sighting count.")
    st.write("Note: This view doesn't include US, as it has its own view.")
    st.write("Page 2: US")
    st.write("This page includes a 2D view of US separated by state, includes colormap for sighting count and tooltip as Page 1.")
    st.write("Page 3: Timelapse")
    st.write("This page shows the UFO sighting along the years by world area. It includes an slider to select the year to show and a tooltip with area and count.")
    st.write("Page 4: About")
    st.write("Info about the dataset and pages content.")



page_names_to_funcs = {
    "Worldwide": main_page,
    "US": page2,
    "Timelapse": page3,
    "About": page4
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()


