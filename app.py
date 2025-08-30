import joblib
import streamlit as st
import pandas as pd
# import sklearn

st.set_page_config(page_title="Prediksi Emisi Gas Karbon Monoksida Turbin")

input_cols = ['AT', 'AP', 'AH', 'AFDP', 'GTEP', 'TIT', 'TAT', 'TEY', 'CDP']
input_desc = [
      'Suhu Sekitar (◦C)',
      'Tekanan Sekitar (mbar)',
      'Kelembapan Sekitar (%)',
      'Tekanan Perbedaan Filter Udara (mbar)',
      'Tekanan Buang Turbin Gas (mbar)',
      'Suhu Masuk Turbin (◦C)',
      'Suhu Setelah Turbin (◦C)',
      'Hasil Energi Turbin (MWH)',
      'Tekanan Buang Kompresor (mbar)'
      ]

cols_stats = pd.read_csv('csv/cols_stats.csv', index_col=0)

model = joblib.load('model/model_RFR_local_compressed.pkl')

st.header("Prediksi Emisi Gas Karbon Monoksida Turbin")

inputs = {}
col1, col2 = st.columns(2)
for col, desc in zip(input_cols[0:5], input_desc[0:5]):
      with col1:
            inputs[col] = st.slider(
                  f"{desc}",
                  float(cols_stats.loc['min', col]),
                  float(cols_stats.loc['max', col]),
                  float(cols_stats.loc['mean', col])
            )

for col, desc in zip(input_cols[5:9], input_desc[5:9]):
      with col2:
            inputs[col] = st.slider(
                  f"{desc}",
                  float(cols_stats.loc['min', col]),
                  float(cols_stats.loc['max', col]),
                  float(cols_stats.loc['mean', col])
            )

df_inputs = pd.DataFrame(inputs, columns=input_cols, index=[0])

# df_inputs

submit = st.button("Prediksi")

if submit:
      results = model.predict(df_inputs)
      results = results.round(4)

      if results:
            st.subheader("Emisi gas karbon monoksida (CO) yang dihasilkan:")
            st.header(f"{results[0]} mg/m3")