import streamlit as st
import pickle
import pandas as pd
from mlxtend.frequent_patterns import association_rules




st.title('Aplikasi Analisis Asosiasi dengan FP-Growth')

try:
    # Muat model pickle
    with open('frequent_itemsets_new_model.pkl', 'rb') as file:
        frequent_itemsets = pickle.load(file)

    # Muat dataset atau objek data yang berisi nama produk
    data = pd.read_excel('file_bersih_new_dataset.xlsx')

    # Ambil semua nama produk dari kolom 'Description'
    products = data['Description'].unique().tolist()

    # Buat dropdown menu untuk memilih produk sebagai anteseden
    selected_product = st.selectbox(
        'Pilih Produk sebagai Anteseden:', products)

    # Tambahkan dropdown menu untuk memilih kriteria lift
    selected_lift = st.selectbox(
        'Pilih Kriteria Lift:', ['','Lift > 1', 'Lift = 1', 'Lift < 1'])
    
    st.info(f"Keterangan Nilai Support")
    st.info(f"Keterangan Nilai Confidence")
    st.info("Keterangan: Lift adalah ukuran kekuatan asosiasi antara produk. Lift > 1 menunjukkan asosiasi yang lebih kuat dari yang diharapkan secara acak, Lift = 1 menunjukkan asosiasi yang tidak lebih kuat dari yang diharapkan secara acak, dan Lift < 1 menunjukkan asosiasi yang lebih lemah dari yang diharapkan secara acak.")

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
    if not association_rules.empty:
        st.write("### Aturan Asosiasi untuk Produk:", selected_product)
        st.write(association_rules[['consequents',
                                    'support', 'confidence', 'lift ratio']])
        st.info(f"Item dengan antecedent A ({selected_product}) dan consequent B yang terdapat dalam tabel harus ditempatkan berdekatan dalam gudang oleh karyawan ritel serta, dapat direkomendasikan kepada pelanggan untuk membeli item/produk selanjutnya.")

    else:
        st.write(
            "Tidak ada aturan asosiasi yang ditemukan untuk produk yang dipilih.")

except FileNotFoundError:
    st.error("File not found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred: {e}")
