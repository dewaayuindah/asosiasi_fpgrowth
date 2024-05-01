import streamlit as st
import pickle
import pandas as pd
from mlxtend.frequent_patterns import association_rules

st.title('Aplikasi Analisis Asosiasi dengan FP-Growth')

try:
    # Muat model pickle
    with open('frequent_itemsets_new1.pkl', 'rb') as file:
        frequent_itemsets = pickle.load(file)

    # Muat dataset atau objek data yang berisi nama produk
    data = pd.read_excel('file_bersih_new_3.xlsx')

    # Ambil semua nama produk dari kolom 'Description'
    products = data['Description'].unique().tolist()

    # Buat dropdown menu untuk memilih produk sebagai anteseden
    selected_product = st.selectbox(
        'Pilih Produk sebagai Anteseden:', products)

    # Tambahkan dropdown menu untuk memilih kriteria lift
    selected_lift = st.selectbox(
        'Pilih Kriteria Lift:', ['Lift > 1', 'Lift = 1', 'Lift < 1'])

    def analyze_association(selected_product, frequent_itemsets):
        # Gunakan algoritma Association Rules untuk mendapatkan aturan asosiasi
        rules_association = association_rules(
            frequent_itemsets, metric="lift")

        # Filter aturan untuk hanya mencakup anteseden yang dipilih
        rules_association = rules_association[rules_association['antecedents'].apply(
            lambda x: selected_product in x)]

        return rules_association

    # Gunakan fungsi untuk mendapatkan aturan asosiasi
    association_rules = analyze_association(
        selected_product, frequent_itemsets)

    # Filter aturan berdasarkan kriteria lift jika lift = 1
    if selected_lift == 'Lift < 1':
        association_rules = association_rules[association_rules['lift'] < 1.0]

    # Filter aturan berdasarkan kriteria lift jika lift = 1
    if selected_lift == 'Lift > 1':
        association_rules = association_rules[association_rules['lift'] > 1.0]

    # Filter aturan berdasarkan kriteria lift jika lift = 1
    if selected_lift == 'Lift = 1':
        association_rules = association_rules[association_rules['lift'] == 1.0]

    # Tampilkan aturan asosiasi yang diperoleh
    if not association_rules.empty:
        st.write("### Aturan Asosiasi untuk Produk:", selected_product)
        st.write(association_rules[['consequents',
                                    'support', 'confidence', 'lift']])
    else:
        st.write(
            "Tidak ada aturan asosiasi yang ditemukan untuk produk yang dipilih.")

except FileNotFoundError:
    st.error("File not found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred: {e}")
