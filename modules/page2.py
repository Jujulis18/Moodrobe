import streamlit as st
import os
import pandas as pd
import calendar
from datetime import date
from scripts.color_detector import get_palette


##if 'page' not in st.session_state:
##    st.session_state.page = 'page1'

def show():
##  if st.session_state.page == 'page1':
    ##st.set_page_config(layout="wide")

    IS_PUBLIC = st.session_state.IS_PUBLIC
    sheet_api = st.session_state.sheet_api
    df = sheet_api.get_all_data()
    st.dataframe(df)

    # --- Exemple de données : dictionnaire {jour: [couleur1, couleur2, couleur3]}
    colors_per_day = {
        1: ["#FF0000", "#00FF00", "#0000FF"],
        2: ["#FFFF00", "#FFA500"],
        3: ["#FFC0CB"],
        5: ["#8A2BE2", "#00FFFF", "#FF69B4"]
    }

    # Mois et année
    year = 2025
    month = 8
    cal = calendar.monthcalendar(year, month)  # liste de semaines

    # CSS pour le calendrier
    st.markdown("""
    <style>
    .calendar { 
        display: grid; 
        grid-template-columns: repeat(7, 1fr); 
        gap: 5px; 
    }
    .day { 
        border: 1px solid #ccc; 
        padding: 5px; 
        height: 80px; 
        position: relative; 
    }
    .color-box { 
        width: 20px; 
        height: 20px; 
        display: inline-block; 
        margin: 2px; 
        border-radius: 4px; 
    }
    .day-number { 
        font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)

    # Construction du calendrier HTML
    html = '<div class="calendar">'

    # Titres des jours
    for d in ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]:
        html += f'<div class="day"><div class="day-number">{d}</div></div>'

    # Cases pour chaque semaine
    for week in cal:
        for day in week:
            if day == 0:
                html += '<div class="day"></div>'
            else:
                day_colors = colors_per_day.get(day, [])
                color_html = "".join([f'<div class="color-box" style="background-color:{c}"></div>' for c in day_colors])
                html += f'<div class="day"><div class="day-number">{day}</div>{color_html}</div>'

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)


    st.markdown("season_color")
    palette = get_palette()
    cols = st.columns(len(palette))
    for col, c in zip(cols, palette):
        color = "#" + c
        with col:
            #st.markdown(f"{color}")
            st.markdown(
                f"""<div class="color-box" style="width:20px; height:20px; background-color:{color};"></div>""",
                unsafe_allow_html=True
            )
