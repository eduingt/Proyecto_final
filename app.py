import streamlit as st
import pandas as pd
import os
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="IP Threat Predictor", layout="centered")
st.title("🛡️ IP Threat Predictor")
st.markdown("Predice si una IP es maliciosa o benigna con base en características conocidas.")

# Rutas locales
db_path = r"C:\Users\forense\Downloads\ip-predictor\predicciones.db"
blacklist_path = r"C:\Users\forense\Downloads\ip-predictor\blacklist.txt"

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("ip_prediction_dataset_10000.csv")

df = cargar_datos()

le_country = LabelEncoder()
le_isp = LabelEncoder()
le_proxy = LabelEncoder()

df["Country"] = le_country.fit_transform(df["Country"])
df["ISP"] = le_isp.fit_transform(df["ISP"])
df["Proxy"] = le_proxy.fit_transform(df["Proxy"])

X = df.drop(["Class", "IP"], axis=1)
y = df["Class"]

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X, y)

# Formulario
st.header("🔍 Ingresar características de la IP")

with st.form("formulario"):
    ip = st.text_input("IP a verificar", value="0.0.0.0")
    country = st.selectbox("País", le_country.classes_)
    isp = st.selectbox("ISP", le_isp.classes_)
    rpm = st.slider("Conexiones por minuto", 0, 100, 50)
    proxy = st.selectbox("¿Usa proxy?", le_proxy.classes_)
    vt_score = st.slider("Reputación en VirusTotal (0 = buena, 1 = mala)", 0.0, 1.0, 0.5, step=0.01)
    submitted = st.form_submit_button("Predecir")

if submitted:
    entrada = pd.DataFrame([[
        le_country.transform([country])[0],
        le_isp.transform([isp])[0],
        rpm,
        le_proxy.transform([proxy])[0],
        vt_score
    ]], columns=X.columns)

    prediccion = modelo.predict(entrada)[0]
    resultado = "⚠️ Maliciosa" if prediccion == 1 else "✅ Benigna"
    st.success(f"Resultado de la predicción: **{resultado}**")

    # Guardar predicción
    try:
        conn = sqlite3.connect(db_path)
        entrada["Prediction"] = prediccion
        entrada.to_sql("historico", conn, if_exists="append", index=False)
        conn.close()
        st.info("📥 Predicción guardada en la base de datos local.")
    except Exception as e:
        st.error(f"❌ Error al guardar en base de datos: {e}")

    # Validar contra blacklist
    try:
        if os.path.exists(blacklist_path):
            with open(blacklist_path, "r") as f:
                lista_negra = [line.strip() for line in f]
            if ip in lista_negra:
                st.warning("⚠️ Esta IP está registrada en la lista negra local.")
            else:
                st.info("✅ Esta IP no está en la lista negra local.")
        else:
            st.warning("⚠️ No se encontró el archivo de lista negra.")
    except Exception as e:
        st.error(f"❌ Error al verificar lista negra: {e}")

# Métricas
st.header("📊 Rendimiento del modelo")
y_pred = modelo.predict(X)
cm = confusion_matrix(y, y_pred)

fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Benigna", "Maliciosa"], yticklabels=["Benigna", "Maliciosa"], ax=ax)
ax.set_xlabel("Predicción")
ax.set_ylabel("Real")
st.pyplot(fig)

st.text("Reporte de clasificación:")
st.text(classification_report(y, y_pred))
#Eduin cambios
