import streamlit as st
import pandas as pd
from functions import data

def select_clusters():
    st.write("")
    st.write("Fragebogen anpassen:")
    cluster_table = data.get_cluster_table()
    selected_clusters = []
    for cluster_number, cluster_name in cluster_table.itertuples():
        checked = st.checkbox(cluster_name, value=True)
        selected_clusters.append({
            "Cluster-Nummer": cluster_number, 
            "Cluster-Name": cluster_name,
            "Selected": checked})
    selected_clusters_df = pd.DataFrame(selected_clusters)
    selected_clusters_df.set_index("Cluster-Nummer", inplace=True)
    return selected_clusters_df

def get_amount_questions():
    fragebogen = pd.read_csv("fragebögen/2025-06-25_Finalversion_Fragebogen_pro-kom_aufbereitet_UTF-8.csv", sep=';', encoding='utf-8')
    return fragebogen.shape[0]