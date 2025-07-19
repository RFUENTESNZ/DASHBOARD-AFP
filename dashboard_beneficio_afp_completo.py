
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Simulador de Beneficio AFP", layout="wide")
st.title("📊 Simulador de Beneficio Estatal - AFP")

@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("resumen_beneficio_afp.csv", sep=None, engine='python')
        df.columns = df.columns.str.lower().str.strip()
        df['sexo'] = df['sexo'].str.upper().str.strip()  # Normaliza a 'F' y 'M'
        return df
    except Exception as e:
        st.error(f"❌ Error cargando el archivo CSV: {e}")
        return pd.DataFrame()

df = cargar_datos()

if df.empty:
    st.stop()

st.sidebar.header("🔎 Filtros")
sexo = st.sidebar.selectbox("Sexo", options=["Todos", "F", "M"])
edad_min = st.sidebar.slider("Edad mínima", 18, 90, 65)
edad_max = st.sidebar.slider("Edad máxima", 18, 90, 90)
meses_min = st.sidebar.slider("Meses cotizados mínimos", 0, 500, 0)
solo_pensionados = st.sidebar.checkbox("Solo pensionados", value=True)

# Aplicar filtros
filtro = (df['edad'] >= edad_min) & (df['edad'] <= edad_max)
filtro &= (df['meses_cotizados'] >= meses_min)
if sexo != "Todos":
    filtro &= (df['sexo'] == sexo)
if solo_pensionados:
    filtro &= (df['pensionado'] == 1)

df_filtrado = df[filtro]

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("🔢 Personas filtradas", len(df_filtrado))
col2.metric("✅ Reciben beneficio", int(df_filtrado['consultara_beneficio'].sum()))
col3.metric("❌ No reciben", int(len(df_filtrado) - df_filtrado['consultara_beneficio'].sum()))

st.divider()

# Gráfico 1: barras beneficio
st.subheader("📊 Gráfico 1: Distribución de beneficio (barras)")
conteo = df_filtrado['consultara_beneficio'].value_counts().sort_index()
labels = ['No Reciben', 'Reciben']
values = [conteo.get(0, 0), conteo.get(1, 0)]
fig1, ax1 = plt.subplots()
ax1.bar(labels, values, color=["salmon", "seagreen"])
st.pyplot(fig1)

# Gráfico 2: torta
st.subheader("🥧 Gráfico 2: Distribución de beneficio (torta)")
fig2, ax2 = plt.subplots()
ax2.pie(values, labels=labels, autopct='%1.1f%%', colors=["salmon", "seagreen"], startangle=90)
ax2.axis('equal')
st.pyplot(fig2)

# Gráfico 3: boxplot de edad por beneficio
st.subheader("📦 Gráfico 3: Edad por condición de beneficio")
fig3, ax3 = plt.subplots()
sns.boxplot(data=df_filtrado, x='consultara_beneficio', y='edad', ax=ax3)
ax3.set_xticklabels(['No Reciben', 'Reciben'])
ax3.set_ylabel("Edad")
st.pyplot(fig3)

# Gráfico 4: Histograma meses cotizados
st.subheader("📈 Gráfico 4: Histograma de meses cotizados")
fig4, ax4 = plt.subplots()
df_filtrado['meses_cotizados'].hist(bins=20, color='skyblue', ax=ax4)
ax4.set_xlabel("Meses Cotizados")
ax4.set_ylabel("Cantidad")
st.pyplot(fig4)

# Gráfico 5: Scatterplot edad vs meses cotizados
st.subheader("📌 Gráfico 5: Dispersión Edad vs. Meses Cotizados")
fig5, ax5 = plt.subplots()
sns.scatterplot(data=df_filtrado, x='edad', y='meses_cotizados', hue='consultara_beneficio', palette='Set2', ax=ax5)
ax5.set_title("Edad vs. Meses Cotizados")
st.pyplot(fig5)

st.divider()
st.subheader("🧾 Tabla de personas filtradas")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
