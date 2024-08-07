import streamlit as st
import pickle
import pandas as pd
from mlxtend.frequent_patterns import association_rules
import base64

# Path gambar
image_path = "apk-removebg-preview.png"

# Membaca file gambar dan mengonversinya menjadi string base64
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# CSS untuk mengatur gambar dan teks overlay
st.markdown(f"""
<style>
.container {{
    position: relative;
    text-align: center;
    color: white;
    margin-bottom: 20px; /* Spasi vertikal dari bawah */
}}

.centered {{
    position: absolute;
    top: 50%; /* Atur jarak vertikal dari teks */
    left: 65%; /* Atur jarak dari kiri */
    transform: translate(-50%, -50%); /* Menyesuaikan transformasi agar tetap di tengah */
    font-family: Garamond;
    font-size: 2.5vw; /* Ukuran font relatif terhadap lebar viewport */
    font-weight: bold;
  color: #fff;
text-shadow: 
    0px 0px 1px #000, 
    0px 0px 2px #000,
    0px 0px 3px #000,
    0px 0px 4px #000,
    0px 0px 5px #000,
    0px 0px 6px #000,
    0px 0px 7px #000,
    0px 0px 8px #000,
    0px 0px 9px #000;
}}
</style>
<div class="container">
  <img src="data:image/png;base64,{encoded_string}" alt="Image" style="width:100%;  border-radius: 50%; /* Membuat gambar menjadi bulat */">
  <div class="centered">Aplikasi Analisis Asosiasi dengan <em>FP-Growth</em></div>
  <div style="margin-top: 20px;"</div>
</div>
""", unsafe_allow_html=True)


try:
    # Muat model pickle
    with open('frequent_itemsets_new_model_0.015.pkl', 'rb') as file:
        frequent_itemsets = pickle.load(file)

    # Muat dataset atau objek data yang berisi nama produk
    data = pd.read_excel('file_bersih_new_dataset.xlsx')

    # Ambil semua nama produk dari kolom 'Description'
    products = data['Description'].unique().tolist()
    # Tambahkan opsi kosong di awal daftar produk
    products.insert(0, "")
    # Buat dropdown menu untuk memilih produk sebagai antecedent
    selected_product = st.selectbox(
        '**Pilih item sebagai *Antecedent*:**', products)

    # Tambahkan dropdown menu untuk memilih kriteria lift
    selected_lift = st.selectbox(
        '**Pilih Kriteria *Lift*:**', ['','Lift = 1', 'Lift > 1', 'Lift < 1'])
    
    st.info(f"**Keterangan Nilai *Support*:**\n\n"
    "Parameter ini, mengukur seberapa sering kombinasi item muncul dalam *dataset* penjualan ritel non-toko, dinyatakan dalam persentase.")
    st.info(f"**Keterangan Nilai *Confidence*:**\n\n"
    "Parameter ini, mengukur seberapa kuat aturan asosiasi yang terbentuk dari kemunculan item B dalam transaksi yang sudah mengandung item A, dinyatakan dalam persentase.")
    # Menampilkan keterangan Lift dengan list bulat menggunakan Markdown
    st.info("""
    **Keterangan Nilai *Lift*:**
    
    Parameter ini, mengukur kevalidan aturan asosiasi yang dihasilkan, dinyatakan dalam bentuk rasio, sebagai berikut.
    - *Lift* > 1: Aturan Asosiasi positif, sering terjadi/sering dibeli bersamaan.
    - *Lift* = 1: Aturan Asosiasi tidak memiliki pengaruh, hanya kebetulan dibeli bersamaan.
    - *Lift* < 1: Aturan Asosiasi negatif, jarang terjadi/jarang dibeli bersamaan.
    """)

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
    if selected_lift == '':
        association_rules = association_rules.rename(columns={'lift': 'lift ratio'})
        association_rules['lift ratio'] = (association_rules['lift ratio']).apply(lambda x: f"{x:.2f}")
        association_rules['support'] = (association_rules['support'] * 100).apply(lambda x: f"{x:.2f}%")
        association_rules['confidence'] = (association_rules['confidence'] * 100).apply(lambda x: f"{x:.2f}%")


    # Filter aturan berdasarkan kriteria lift jika lift = 1
    if selected_lift == 'Lift < 1':
        association_rules = association_rules[association_rules['lift'] < 1.0]
        # Kalikan nilai lift dengan 100
        association_rules = association_rules.rename(columns={'lift': 'lift ratio'})
        association_rules['lift ratio'] = (association_rules['lift ratio']).apply(lambda x: f"{x:.2f}")
        association_rules['support'] = (association_rules['support'] * 100).apply(lambda x: f"{x:.2f}%")
        association_rules['confidence'] = (association_rules['confidence'] * 100).apply(lambda x: f"{x:.2f}%")


    # Filter aturan berdasarkan kriteria lift jika lift = 1
    if selected_lift == 'Lift > 1':
        association_rules = association_rules[association_rules['lift'] > 1.0]
        # Kalikan nilai lift dengan 100
        association_rules = association_rules.rename(columns={'lift': 'lift ratio'})
        association_rules['lift ratio'] = (association_rules['lift ratio']).apply(lambda x: f"{x:.2f}")
        association_rules['support'] = (association_rules['support'] * 100).apply(lambda x: f"{x:.2f}%")
        association_rules['confidence'] = (association_rules['confidence'] * 100).apply(lambda x: f"{x:.2f}%")
        

    # Filter aturan berdasarkan kriteria lift jika lift = 1
    if selected_lift == 'Lift = 1':
        association_rules = association_rules[association_rules['lift'] == 1.0]
        # Kalikan nilai lift dengan 100
        association_rules = association_rules.rename(columns={'lift': 'lift ratio'})
        association_rules['lift ratio'] = (association_rules['lift ratio']).apply(lambda x: f"{x:.2f}")
        association_rules['support'] = (association_rules['support'] * 100).apply(lambda x: f"{x:.2f}%")
        association_rules['confidence'] = (association_rules['confidence'] * 100).apply(lambda x: f"{x:.2f}%")

    # Tampilkan aturan asosiasi yang diperoleh
    if selected_product == "":
        st.write("Silakan pilih item terlebih dahulu.")
    elif selected_lift == "":
        st.write("Silakan pilih kriteria *lift*.")
    elif not association_rules.empty:
        st.write(f"### **Aturan Asosiasi untuk item:**", selected_product)
       
        st.write(association_rules[['consequents',
                                    'support', 'confidence', 'lift ratio']])
        st.info(f"**Representasi Pengetahuan:** \n\n Item dengan *antecedent* A ({selected_product}) dan *consequent* B yang terdapat dalam tabel harus ditempatkan berdekatan dalam gudang oleh karyawan ritel. Selain itu, item tersebut dapat direkomendasikan secara *online* kepada pelanggan untuk membeli item selanjutnya.")
    else:
        st.write(f"Tidak ada aturan asosiasi yang ditemukan pada nilai ({selected_lift}).")
except FileNotFoundError:
    st.error("File not found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred: {e}")
