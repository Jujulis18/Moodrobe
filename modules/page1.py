import streamlit as st
from datetime import datetime
from PIL import Image
import time
from scripts.yolov8n_cloth import predict_clothes
from scripts.color_detector import detect_colors


##if 'page' not in st.session_state:
##    st.session_state.page = 'page1'

def show():
	##if st.session_state.page == 'page1':
	##st.set_page_config(layout="wide")

	# --- Titre ---
	st.title("Analyse de mes vêtements")

	# --- Upload de l'image ---
	uploaded_file = st.file_uploader("Upload une photo de ton vêtement", type=["jpg", "png", "jpeg"])
	done = False

	col1, col2 = st.columns(2)

	with col1:

		if uploaded_file:
			# Affichage immédiat de l'image
			image = Image.open(uploaded_file)
			st.image(image, caption="Image uploadée", width=200 )
			
			# --- Section d'analyse ---
			with st.spinner("Analyse en cours... ⏳"):
				#time.sleep(2)  
				detected_items, img_predict, results = predict_clothes(image)
				st.write(detected_items)
				detected_colors, real_colors = detect_colors(image, results)
				season = "Été"  
			done = True

			
	with col2:
		if done == True:
			st.success("Analyse terminée ✅")
			
			# --- Résumé de ce qui a été trouvé ---
			st.subheader("Résumé de l'analyse")
			st.write(f"**Date :** {datetime.today().strftime('%Y-%m-%d')}")
			st.write(f"**Vêtements :** {', '.join(detected_items)}")

			cols = st.columns(len(detected_colors))

			color_detected_list = []
			color_real_list = []
			for col, (c, count) in zip(cols, detected_colors):
				color = "#" + c
				color_detected_list.append(color)
				with col:
					st.markdown(f"**Couleur :** {color}")
					st.markdown(
						f"""<div style="width:50px; height:50px; background-color:{color}; border:1px solid #000;"></div>""",
						unsafe_allow_html=True
					)

			st.write(f"**Saison :** {season}")
			st.image(img_predict, caption="Résultat YOLO", width=200)
			cols = st.columns(len( real_colors.items()))
			for col, (rgb, count) in zip(cols, real_colors.items()):
				color = '#%02x%02x%02x' % rgb
				color_real_list.append(color)
				with col:
					st.markdown(
						f"""<div style="width:20px; height:20px; background-color:{color}; border:1px solid #000;"></div>""",
						unsafe_allow_html=True
						)

			IS_PUBLIC = st.session_state.IS_PUBLIC
			sheet_api = st.session_state.sheet_api
			sheet_api.save_data([
			    datetime.today().strftime('%Y-%m-%d'),
			    ', '.join(detected_items),
			    ', '.join(map(str, color_detected_list)),
			    ', '.join(map(str, color_real_list)),
			    str(season)
			])

			st.success("Sauvegarde terminée ✅")
	  