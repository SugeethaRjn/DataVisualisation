# Imporation des bibliothèques
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import random
import os

# Titre
st.set_page_config(page_title="Dashboard des Gares", layout="wide")

# Menu de navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Menu pincipal",
        options=["Accueil", "CV", "Analyse", "Contact"],
        icons=["house", "person", "bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

# ACCUEIL : Page principale pour charger le fichier
if selected == "Accueil":
    st.title("Bienvenue sur le Dashboard des Gares 🚉")
    
    st.subheader("📁 Choisir un fichier Excel")
    uploaded_file = st.file_uploader("Téléversez un fichier Excel", type=["xlsx"])
    
    # Fonction pour charger et traiter le fichier Excel, avec mise en cache
    @st.cache_data
    def charger_fichier_excel(uploaded_file):
        # Charger la feuille normalisation qui contient les bonnes données
        df = pd.read_excel(uploaded_file, sheet_name='normalisation')
        
        # Vérifier si la colonne 'Nom de la gare normalisé' est présente
        if 'Nom de la gare normalisé' in df.columns:
            df['Nom de la gare'] = df['Nom de la gare normalisé']
        else:
            # Sinon, on va les normaliser
            df['Nom de la gare'] = df['Nom de la gare'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        
        return df
    
    if uploaded_file:
        # Appeler la fonction pour charger le fichier
        df = charger_fichier_excel(uploaded_file)
        
        # Stockage du df dans l'état de session
        st.session_state.df = df 
        st.success("Fichier chargé avec succès")
        
        # Affichage des premières lignes pour s'assurer que le fichier chargé
        st.write("Voici un aperçu des données :")
        st.dataframe(df.head())

        # Afficher les colonnes pour vérifier aussi
        st.write("Voici les colonnes disponibles dans du fichier :")
        st.write(df.columns)

# PAGE CV : Présentation de mon profil accadémique
elif selected == "CV":
    st.title("Mon Curriculum Vitae 🌟")
    
    # Ma photo de profil
    st.image("photo_profil.png", caption="Sugeetha SUGUNAPARAJAN", width=300)

    # Mes principales informations et contacts pour me joindre
    st.subheader("Informations Personnelles")
    st.write("**Nom :** Sugeetha SUGUNAPARAJAN")
    st.write("**Adresse :** 92130 Issy-Les-Moulineaux")
    st.write("**Téléphone :** 07 70 37 13 44")
    st.write("**Email :** [sugeetha92@hotmail.fr](mailto:sugeetha92@hotmail.fr)")
    st.write("**LinkedIn :** [linkedin.com/in/sugeetha-sugunaparajan](https://www.linkedin.com/in/sugeetha-sugunaparajan)")
    st.write("**Permis de conduire :** Permis B")

    # Mes expériences professionnelles
    st.subheader("Expériences Professionnelles 🏢")
    st.write("""
    **Refonte de la base de données - THALES**  
    *Avril 2023 - Juin 2023*  
    - Création de tableaux de bord et graphiques dynamiques sur Excel
    - Développement de formulaires de saisie de données personnalisés en VBA
    - Refonte des données du système de suivi des réparations

    **Stage - Gestionnaire de Données -  ARVAL BNP Paribas**  
    *Juillet 2022 - Août 2022*  
    - Gestion de la base de données sur EXCEL
    - Chargé du suivi des réparations
    - Répartition des tâches en équipe
    """)

    # Mes compétences techniques
    st.subheader("Compétences Techniques 💻")
    st.write("""
    - **Langages de programmation :** SQL3, PL/SQL, VBA, Python
    - **Outils de gestion de bases de données :** Oracle, MySQL Live, Microsoft Access
    - **Outils de visualisation :** Power BI, Microsoft Excel, Streamlit
    - **Modélisation :** Modèle Conceptuel de Données (MCD), Modèle Logique des Données (MLD)
    """)

    # Formations
    st.subheader("Formations 🎓")
    st.write("""
    **M1 Business Intelligence & Analytics** - EFREI Paris  
    *2024 - en cours*

    **BUT Informatique** - IUT de Paris Descartes  
    *2021 - 2023*  
    - Spécialisation : Administration, gestion et exploitation des données
    """)

    # Projet académique
    st.subheader("Projet Académique 📚")
    st.write("""
    **Modélisation d'une base de données pour une agence de location de voitures**  
    En binôme, création d'une base de données optimisée pour centraliser les données des locations et des clients. Utilisation de SQL3 pour garantir la sécurité des données.
    """)

    # Langues
    st.subheader("Langues 🌍")
    st.write("""
    - **Français :** Langue maternelle
    - **Anglais :** Niveau B2 (TOEIC : 795)
    - **Tamil :** Courant
    - **Espagnol :** Niveau A2
    """)

    # Centres d'intérêt
    st.subheader("Centres d'Intérêt 🎯")
    st.write("""
    - **Voyages**
    - **Pâtisserie**
    - **Sport :** Musculation
    """)

# ANALYSE : Visualisation des données
elif selected == "Analyse":
    st.title("Analyse de la Fréquentation des Gares 🧐")

    # S'assurer qu'un fichier est bien chargé pour faire l'analyse
    if 'df' in st.session_state:
        df = st.session_state.df
        
        # Création df_pie
        df_pie = df[['Nom de la gare', 'Total Voyageurs 2023']].copy()

        # Affichage chiffres clés
        st.subheader("Chiffres Clés 📊")
        
        # Gare avec la fréquentation maximale en 2023
        gare_max_2023 = df.loc[df['Total Voyageurs 2023'].idxmax()]['Nom de la gare']
        max_value_2023 = int(df['Total Voyageurs 2023'].max())
        st.metric("Gare avec le plus grand nombre de voyageurs en 2023", gare_max_2023, max_value_2023)
        
        # Gare avec la fréquentation minimale en 2023
        gare_min_2023 = df.loc[df['Total Voyageurs 2023'].idxmin()]['Nom de la gare']
        min_value_2023 = int(df['Total Voyageurs 2023'].min())
        st.metric("Gare avec le plus petit nombre de voyageurs en 2023", gare_min_2023, min_value_2023)

        # Graphique en barres horizontales (Top 10 gares par nombre de voyageurs en 2023)
        st.subheader("Top 10 des Gares par Nombre de Voyageurs en 2023")
        top_10_gares = df.nlargest(10, 'Total Voyageurs 2023')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(top_10_gares['Nom de la gare'], top_10_gares['Total Voyageurs 2023'], color='skyblue')
        ax.set_xlabel('Nombre de Voyageurs en 2023')
        ax.set_title('Top 10 des Gares par Nombre de Voyageurs en 2023')
        st.pyplot(fig)

        # Sélection de gare pour filtrage
        st.subheader("Filtrer par Gare")
        gare_selection = st.selectbox("Choisissez une gare :", df['Nom de la gare'].unique())
        filtered_df = df[df['Nom de la gare'] == gare_selection]
        
        # Carte avec fréquence des voyageurs
        st.subheader("Carte des Gares en France avec Fréquentation")
        
        # Vérifier si colonne "Geo Shape" existe
        if 'Geo Shape' in df.columns:
            # Prendre que les données ayant des coordonnées dans "Geo Shape"
            df_geo = df[df['Geo Shape'].notna()].copy()
        
            # Extraire les coordonnées de "Geo Shape"
            df_geo['Latitude'] = df_geo['Geo Shape'].apply(lambda x: eval(x)['coordinates'][1])
            df_geo['Longitude'] = df_geo['Geo Shape'].apply(lambda x: eval(x)['coordinates'][0])
            
            # Récupérer coordonnées de la gare sélectionnée
            selected_gare_coords = df_geo[df_geo['Nom de la gare'] == gare_selection][['Latitude', 'Longitude']].values[0]
            
            # Affichage gares sur une carte
            fig_map = px.scatter_mapbox(
                df_geo, 
                lat="Latitude", 
                lon="Longitude", 
                hover_name="Nom de la gare", 
                size="Total Voyageurs 2023", 
                color="Total Voyageurs 2023", 
                color_continuous_scale=px.colors.cyclical.IceFire, 
                zoom=12,  # Zoom plus serré
                center={"lat": selected_gare_coords[0], "lon": selected_gare_coords[1]},
                height=600,
                title=f"Répartition des Gares avec Fréquentation en 2023 (Zoom sur {gare_selection})"
            )
            
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":30,"l":0,"b":0})
            st.plotly_chart(fig_map)
        else:
            st.error("La colonne 'Geo Shape' est introuvable dans le fichier.")

        # Créer df_pie
        df_pie = df[['Nom de la gare', 'Total Voyageurs 2023']].copy()
        
        # Regrouper les gares avec moins de 50 000 voyageurs
        df_pie['Category'] = df_pie['Total Voyageurs 2023'].apply(lambda x: 'Autres' if x < 50000 else 'Gare')
        
        # Calculer la somme des "Autres"
        autres_sum = df_pie[df_pie['Category'] == 'Autres']['Total Voyageurs 2023'].sum()
        
        # Filtrer les gares ayant plus de 50 000 voyageurs
        df_pie_filtered = df_pie[df_pie['Category'] == 'Gare'].copy()
        
        # Nouveau DataFrame pour les catégories, avec "Autres" en tant que catégorie unique
        df_pie_final = pd.concat([
            df_pie_filtered[['Nom de la gare', 'Total Voyageurs 2023']],
            pd.DataFrame({'Nom de la gare': ['Autres'], 'Total Voyageurs 2023': [autres_sum]})
        ])
        
        # Histogramme avec filtre
        st.subheader("Nombre de Voyageurs par Gare en 2023 (Trié avec Filtre)")
        
        # Slider pour filtrer par seuil minimum de voyageurs
        min_voyageurs = st.slider('Seuil minimum de voyageurs', min_value=0, max_value=int(df['Total Voyageurs 2023'].max()), value=50000, step=10000)
        
        # Filtrer le DataFrame en fonction seuil de voyageurs
        filtered_df = df[df['Total Voyageurs 2023'] >= min_voyageurs]
        
        # Tri des données par nombre de voyageurs en 2023
        sorted_df = filtered_df.sort_values(by='Total Voyageurs 2023', ascending=False)
        
        # Affichage d'un nombre limité de gares
        top_n = st.slider('Nombre de gares à afficher', min_value=5, max_value=len(sorted_df), value=10, step=1)
        
        # Garder uniquement le top N gares
        sorted_df = sorted_df.head(top_n)
        
        # Créer l'histogramme trié
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(sorted_df['Nom de la gare'], sorted_df['Total Voyageurs 2023'], color='teal')
        ax.set_title('Nombre de Voyageurs par Gare en 2023')
        plt.xticks(rotation=90)
        plt.tight_layout()
        
        # Afficher l'histogramme
        st.pyplot(fig)
        
        # Bar Chart comparatif
        years = ['Total Voyageurs 2023', 'Total Voyageurs 2022', 'Total Voyageurs 2021', 'Total Voyageurs 2020']
        df_bar = df.melt(id_vars=['Nom de la gare'], value_vars=years, var_name='Année', value_name='Voyageurs')
        
        fig_bar = px.bar(df_bar, x='Nom de la gare', y='Voyageurs', color='Année', barmode='group',
                         color_discrete_sequence=px.colors.qualitative.Set1, title='Fréquentation des Gares sur Plusieurs Années')
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar)
        
        # Comparaison avec courbe
        if st.checkbox("Afficher la comparaison des voyageurs sur plusieurs années"):
            fig_comp = px.line(df_bar, x='Nom de la gare', y='Voyageurs', color='Année',
                               line_group='Année', hover_name='Nom de la gare',
                               title='Comparaison de la Fréquentation des Gares sur Plusieurs Années')
            fig_comp.update_traces(line=dict(width=3))
            st.plotly_chart(fig_comp)

    else:
        st.error("Veuillez téléverser un fichier Excel dans la section Accueil.")

# CONTACT : Formulaire de Contact
elif selected == "Contact":
    # Nom du fichier CSV qui va receuillir les informations des visiteurs
    csv_file = "messages_contact.csv"

    def contact_form():
        st.title("Contactez-moi 📞")
        st.write("Pour me contacter, veuillez remplir le formulaire ci-dessous.")

        with st.form("contact_form"):
            nom = st.text_input("Votre nom")
            email = st.text_input("Votre adresse e-mail")
            message = st.text_area("Votre message")

            submit_button = st.form_submit_button(label="Envoyer")

            if submit_button:
                if nom and email and message:
                    new_message = {'NOM': nom, 'MAIL': email, 'MESSAGE': message}
                    messages_df = pd.DataFrame([new_message])

                    # Si fichier n'existe pas, création du fichier
                    if not os.path.exists(csv_file):
                        messages_df.to_csv(csv_file, mode='w', header=True, index=False, sep=';')
                    else:
                        messages_df.to_csv(csv_file, mode='a', header=False, index=False, sep=';')

                    st.success("Merci! Votre message a été envoyé.")
                else:
                    st.error("Veuillez remplir tous les champs du formulaire.")

    contact_form()
