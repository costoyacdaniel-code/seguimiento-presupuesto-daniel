import streamlit as st
import pandas as pd
from datetime import date

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Seguimiento de Presupuesto", layout="centered")
st.title("💰 Seguimiento de Presupuesto y Albaranes")

# MEMORIA DE DATOS (Para que no se borren al escribir)
if 'datos_presupuesto' not in st.session_state:
    st.session_state.datos_presupuesto = []

# FORMULARIO DE ENTRADA
with st.form("form_presupuesto", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        n_albaran = st.text_input("Número de Albarán:")
        fecha = st.date_input("Fecha:", date.today())
        trabajador = st.text_input("Trabajador:")
    
    with col2:
        partida = st.selectbox("Partida del presupuesto:", 
                              ["Material Eléctrico", "Fontanería", "Tabiquería", "Pintura", "Otros"])
        gasto = st.number_input("Gastos de esta partida (€):", min_value=0.0, step=0.01)

    comentarios = st.text_area("Comentarios:")
    foto = st.file_uploader("Subir foto del albarán (Opcional)", type=["jpg", "png", "pdf"])
    
    boton_guardar = st.form_submit_button("Registrar Gasto")

# LÓGICA PARA GUARDAR
if boton_guardar:
    if n_albaran and trabajador:
        nuevo_registro = {
            "Albarán": n_albaran,
            "Fecha": fecha,
            "Trabajador": trabajador,
            "Partida": partida,
            "Gasto (€)": gasto,
            "Comentarios": comentarios,
            "Foto": "Subida" if foto else "No"
        }
        st.session_state.datos_presupuesto.append(nuevo_registro)
        st.success("✅ Gasto registrado con éxito")
    else:
        st.error("⚠️ Por favor, rellena el número de albarán y el trabajador.")

# MOSTRAR TABLA Y TOTAL
if st.session_state.datos_presupuesto:
    df = pd.DataFrame(st.session_state.datos_presupuesto)
    st.write("### Resumen de Gastos")
    st.table(df)
    
    total = df["Gasto (€)"].sum()
    st.metric("Total Gastado acumulado", f"{total} €")

    # Botón para descargar
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Informe CSV", csv, "presupuesto.csv", "text/csv")
