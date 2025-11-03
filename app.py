import streamlit as st
import pandas as pd
import zipfile
import io
import os

# =========================
# TEMPLATE HTML DE BASE
# =========================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relevé de Notes - Concours Blanc</title>
<style>
@page { size: A4; margin: 0; }
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 40px; background: white; color: #333; }
.container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border: 2px solid #2c3e50; }
.header { text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 20px; margin-bottom: 30px; }
.logo-area { font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
.header h1 { color: #2c3e50; margin: 10px 0; font-size: 28px; }
.header .subtitle { color: #7f8c8d; font-size: 16px; margin-top: 5px; }
.info-section { background: #ecf0f1; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
.info-row { display: flex; justify-content: space-between; margin-bottom: 12px; padding: 8px 0; }
.info-label { font-weight: bold; color: #2c3e50; width: 40%; }
.info-value { color: #34495e; width: 55%; border-bottom: 1px solid #bdc3c7; padding-bottom: 2px; }
.notes-section { margin: 30px 0; }
.notes-title { background: #3498db; color: white; padding: 12px; font-size: 18px; font-weight: bold; margin-bottom: 20px; border-radius: 5px; }
.note-item { display: flex; justify-content: space-between; padding: 15px; border-bottom: 2px solid #ecf0f1; align-items: center; }
.note-item:hover { background: #f8f9fa; }
.matiere { font-weight: 600; color: #2c3e50; font-size: 16px; }
.note { font-size: 24px; font-weight: bold; color: #3498db; }
.moyenne-generale { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 30px 0; }
.moyenne-generale .label { font-size: 18px; margin-bottom: 10px; }
.moyenne-generale .valeur { font-size: 36px; font-weight: bold; }
.footer { margin-top: 50px; display: flex; justify-content: flex-end; align-items: flex-end; }
.signature-section { text-align: right; }
.footer-label { font-weight: bold; color: #2c3e50; margin-bottom: 40px; }
.signature-line { border-top: 2px solid #2c3e50; width: 200px; margin-top: 50px; }
.stamp-area { height: 80px; border: 2px dashed #bdc3c7; width: 150px; display: inline-block; margin-top: 10px; border-radius: 50%; }
.signature-brand { margin-top: 15px; font-style: italic; color: #3498db; font-weight: bold; font-size: 16px; }
@media print { body { padding: 0; } .container { border: none; padding: 20px; } }
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo-area">Diploma Santé</div>
        <h1>RELEVÉ DE NOTES</h1>
        <div class="subtitle">Premier Concours Blanc - Année Scolaire 2025-2026</div>
    </div>
    
    <div class="info-section">
        <div class="info-row">
            <span class="info-label">Nom :</span>
            <span class="info-value">{nom}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Prénom :</span>
            <span class="info-value">{prenom}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Classe :</span>
            <span class="info-value">{classe}</span>
        </div>
    </div>
    
    <div class="notes-section">
        <div class="notes-title">RÉSULTATS PAR MATIÈRE</div>
        <div class="note-item"><span class="matiere">Mathématiques</span><span class="note">{maths} / 20</span></div>
        <div class="note-item"><span class="matiere">Physique-Chimie</span><span class="note">{physique} / 20</span></div>
        <div class="note-item"><span class="matiere">Sciences de la Vie et de la Terre (SVT)</span><span class="note">{svt} / 20</span></div>
    </div>
    
    <div class="moyenne-generale">
        <div class="label">MOYENNE GÉNÉRALE</div>
        <div class="valeur">{moyenne} / 20</div>
    </div>
    
    <div class="footer">
        <div class="signature-section">
            <div class="footer-label">La Direction</div>
            <div class="stamp-area"></div>
            <div class="signature-line"></div>
            <div class="signature-brand">Diploma Santé</div>
        </div>
    </div>
</div>
</body>
</html>"""

# =========================
# APP STREAMLIT
# =========================
st.title("📄 Générateur de Relevés HTML - Diploma Santé")

st.write("Cette application génère automatiquement un fichier ZIP contenant un relevé de notes HTML pour chaque élève à partir d’un fichier Excel.")

uploaded_file = st.file_uploader("📂 Importer le fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"✅ Fichier chargé : {uploaded_file.name}")
    st.write("Aperçu des données :")
    st.dataframe(df.head())

    # Vérification des colonnes nécessaires
    colonnes_requises = ["Nom", "Prénom", "Classe", "Mathématiques", "Physique-Chimie", "SVT", "Moyenne"]
    if all(col in df.columns for col in colonnes_requises):
        if st.button("🚀 Générer les fichiers HTML et ZIP"):
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as zipf:
                for _, row in df.iterrows():
                    html_content = HTML_TEMPLATE.format(
                        nom=row["Nom"],
                        prenom=row["Prénom"],
                        classe=row["Classe"],
                        maths=row["Mathématiques"],
                        physique=row["Physique-Chimie"],
                        svt=row["SVT"],
                        moyenne=row["Moyenne"]
                    )
                    filename = f"{row['Nom']}_{row['Prénom']}.html".replace(" ", "_")
                    zipf.writestr(filename, html_content)
            buffer.seek(0)

            st.success("🎉 Génération terminée ! Télécharge ton fichier ZIP ci-dessous.")
            st.download_button(
                label="⬇️ Télécharger le ZIP",
                data=buffer,
                file_name="releves_diploma_sante.zip",
                mime="application/zip"
            )
    else:
        st.error(f"❌ Le fichier Excel doit contenir les colonnes suivantes : {', '.join(colonnes_requises)}")
