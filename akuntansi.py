import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os
import warnings
import datetime
warnings.filterwarnings('ignore')
sns.set(style='dark')

st.set_page_config(page_title='Persamaan Dasar Akuntansi', page_icon=':watermelon:', layout='wide')

st.title('Persamaan Dasar Akuntansi :sparkles:')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

if 'snow_displayed' not in st.session_state:
    st.session_state.snow_displayed = True

# Create First Value of All Columns
st.subheader("Nilai Awal :money_with_wings:")
col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,2,2,1])

with col1:
    tanggal = st.date_input('Tanggal', min_value=datetime.date(2022,1,1), max_value=datetime.date.today(), value=None, format="DD/MM/YYYY")

with col2:
    keterangan = st.text_input("Keterangan", value="Nilai awal", disabled=True)

with col3:
    kas = st.number_input('Kas', min_value=0, value=0, step=100, placeholder='Ex: 50000')

with col4:
    bhp = st.number_input('BHP', min_value=0, value=0, step=100, placeholder='Ex: 50000')

with col5:
    peralatan_kantor = st.number_input('Peralatan kantor', value=0, step=100, placeholder='Ex: 100000')

if 'tanggal' not in st.session_state:
    st.session_state.tanggal = []
    st.session_state.keterangan = []
    st.session_state.kategori_1 = []
    st.session_state.kategori_2 = []
    st.session_state.kas = []
    st.session_state.bhp = []
    st.session_state.peralatan_kantor = []
    st.session_state.persekot_sewa = []
    st.session_state.utang_bank = []
    st.session_state.utang_usaha = []
    st.session_state.modal = []
    st.session_state.prive = []
    st.session_state.pendapatan = []
    st.session_state.biaya = []

with col6:
    if 'input_button_clicked' not in st.session_state:
        st.session_state.input_button_clicked = False

    input_button_clicked = st.button('Input', key='input_button', disabled=st.session_state.input_button_clicked)

    # Check if the "Input" button is clicked
    if input_button_clicked:
        # Set the button state to True in session state
        st.session_state.input_button_clicked = True
        st.session_state.tanggal.append(tanggal)
        st.session_state.keterangan.append(keterangan)
        st.session_state.kas.append(0 if kas is None else kas)
        st.session_state.bhp.append(0 if bhp is None else bhp)
        st.session_state.peralatan_kantor.append(0 if peralatan_kantor is None else peralatan_kantor)
        st.session_state.persekot_sewa.append(0)
        st.session_state.utang_usaha.append(0)
        st.session_state.utang_bank.append(0)
        st.session_state.modal.append(kas + bhp + peralatan_kantor)
        st.session_state.prive.append(0)
        st.session_state.pendapatan.append(0)
        st.session_state.biaya.append(0)
        st.session_state.kategori_1.append('')   
        st.session_state.kategori_2.append('Nilai awal') 

st.write('---')       

# Create dictionary
# table_placeholder = st.empty()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Persamaan Dasar Akuntansi", "Laba Rugi", "Perubahan Ekuitas", "Neraca", "Arus Kas", "Visualisasi"])

with tab1:
    # Input transaction
    st.subheader("Transaksi :heavy_dollar_sign:")

    # Making 5 columns to get input of all required data
    col1, col2, col3, col4, col5, col6 = st.columns([2,3,2,2,2,1])

    # Create date input
    with col1:
        date = st.date_input("Input tanggal transaksi", min_value=tanggal, max_value=datetime.date.today(), value=tanggal, format="DD/MM/YYYY")

    # Create desc input
    with col2:
        desc = st.text_input("Masukkan keterangan transaksi", placeholder="Ex: Beban sewa alat").title()

    # Create category input
    with col3:
        cat1 = st.selectbox("Pilih kategori", options=('Aset', 'Kewajiban', 'Ekuitas'), placeholder='Ex: Aset', index=None)

    # Create category 2
    with col4:
        if cat1 == 'Aset':
            cat2 = st.selectbox('Pilih kategori', options=('Kas','BHP','Peralatan Kantor','Persekot Sewa'), index=None, placeholder='Ex: Kas')
        elif cat1 == 'Kewajiban':
            cat2 = st.selectbox('Pilih kategori', options=('Utang Bank','Utang Usaha'), index=None, placeholder='Ex: Utang Bank')
        else:
            cat2 = st.selectbox('Pilih kategori', options=('Modal','Prive','Pendapatan','Biaya'), index=None, placeholder='Ex: Modal')

    # Create amount input
    with col5:
        if cat2 == "Biaya":
            amount = st.number_input("Masukkan nominal", max_value=0, value=None, placeholder='Ex: -10000')
        else:
            amount = st.number_input("Masukkan nominal", step=1, value=None, placeholder='Ex: 10000')

    col6.markdown("""
        <style>
            div[data-testid="stHorizontalBlock"] > div {
                display: flex;
                align-items: flex-end;
            }
        </style>
    """, unsafe_allow_html=True)

    clicked = col6.button('Simpan')

    if clicked:
        st.session_state.tanggal.append(date)
        st.session_state.keterangan.append(desc)
        st.session_state.kategori_1.append(cat1)
        st.session_state.kategori_2.append(cat2)
        
        # Logika append untuk Kas
        if (desc.__contains__("Pembelian") or desc.__contains__("Membeli")) and cat2 == 'BHP':
            st.session_state.kas.append(-amount)
        elif (desc.__contains__("Menyewa") or desc.__contains__("Persekot")) and cat2 == "Persekot Sewa":
            st.session_state.kas.append(-amount)
        else:
            st.session_state.kas.append(amount if cat2 == "Kas" or (cat2 == 'Biaya' and not desc.__contains__('Penggunaan BHP')) or cat2 == 'Utang Bank' or cat2 == 'Pendapatan' or cat2 == 'Prive' or cat2 == 'Utang Usaha' else 0)
        
        # Logika append untuk BHP
        if desc.__contains__("Membeli") and cat2 == "Kas":
            st.session_state.bhp.append(-amount)
        else:
            st.session_state.bhp.append(amount if cat2 == 'BHP' or (cat2 == 'Biaya' and desc.__contains__("Penggunaan BHP")) else 0)

        # Logika append untuk persekot sewa
        if (desc.__contains__("Menyewa") or desc.__contains__("Persekot")) and cat2 == "Kas":
            st.session_state.persekot_sewa.append(-amount)
        else:
            st.session_state.persekot_sewa.append(amount if cat2 == "Persekot Sewa" else 0)

        st.session_state.peralatan_kantor.append(amount if cat2 == "Peralatan Kantor" else 0)  

        # Logika append untuk utang usaha
        if (desc.__contains__('Angsuran') and cat2 == 'Kas'):
            st.session_state.utang_usaha.append(amount)
        else:
            st.session_state.utang_usaha.append(amount if cat2 == "Utang Usaha" else 0)

        st.session_state.utang_bank.append(amount if cat2 == "Utang Bank" else 0)
        st.session_state.modal.append(amount if cat2 == "Modal" else 0)
        st.session_state.prive.append(amount if cat2 == "Prive" else 0)
        st.session_state.pendapatan.append(amount if (cat2 == "Pendapatan") or 
                                           ((desc.__contains__("Pendapatan") or desc.__contains__("Menerima")) and cat2 == "Kas") 
                                           else 0)
        
        st.session_state.biaya.append(amount if ((desc.__contains__("Bayar") or desc.__contains__("Membayar") or desc.__contains__("Beban") or desc.__contains__("Macam-macam")) and cat2 == "Kas") or 
                                     (cat2 == "Biaya")  or 
                                     ((desc.__contains__("Pemakaian") or desc.__contains__("Penggunaan")) and cat2 == 'BHP') 
                                     else 0)
        
        st.success("Data Berhasil Ditambahkan", icon="🤞")

    formated_dates = [d.strftime('%d/%m/%Y') for d in st.session_state.tanggal]

    dict_items = {
        "Tanggal": formated_dates,
        "Keterangan": st.session_state.keterangan, 
        "Kas": st.session_state.kas,
        "BHP": st.session_state.bhp,
        "Peralatan Kantor": st.session_state.peralatan_kantor,
        "Persekot Sewa": st.session_state.persekot_sewa,
        "Utang Usaha": st.session_state.utang_usaha,
        "Utang Bank": st.session_state.utang_bank,
        "Modal": st.session_state.modal,
        "Prive": st.session_state.prive,
        "Pendapatan": st.session_state.pendapatan,
        "Biaya": st.session_state.biaya,
        "Kategori_1": st.session_state.kategori_1,
        "Kategori_2": st.session_state.kategori_2
    }

    # selected_keys = [key for key in dict_items.keys() if key not in ["Kategori_1", "Kategori_2"]]

    # data = pd.DataFrame(data={key: dict_items[key] for key in selected_keys},
    #                 index=[i + 1 for i in range(len(dict_items["Tanggal"]))],
    #                 columns=selected_keys)

    data = pd.DataFrame(dict_items, index=[i + 1 for i in range(len(dict_items['Tanggal']))])

    df_persamaan = data.drop(columns=['Kategori_1','Kategori_2'])

    col1, col2, col3 = st.columns(3)
    with col1:
        value = data["Kas"].sum() + data["BHP"].sum() + data["Peralatan Kantor"].sum() + data["Persekot Sewa"].sum()
        st.metric(label="Total Aset :chart:", value=value, delta=amount if cat2 == 'Kas' or cat2 == 'BHP' or cat2 == 'Peralatan Kantor' or cat2 == 'Persekot Sewa' or cat2 == 'Pendapatan' or cat2 == 'Biaya' else 0)

    with col2:
        value = data['Utang Bank'].sum() + data['Utang Usaha'].sum()
        st.metric(label="Total Kewajiban :receipt:", value=value, delta=amount if cat2 == 'Utang Bank' or cat2 == 'Utang Usaha' else 0)

    with col3:
        value = (data['Modal'].sum() + data['Prive'].sum() + data['Pendapatan'].sum() + data['Biaya'].sum())
        st.metric(label="Total Ekuitas :moneybag:", value=value, delta=amount if cat2 == 'Modal' or cat2 == 'BHP' or cat2 == 'Prive' or cat2 == 'Pendapatan' or cat2 == 'Biaya' or (cat2 == 'Kas' and (desc.__contains__("Bayar") or desc.__contains__("Membayar") or desc.__contains__("Pendapatan") or desc.__contains__("Menerima") or desc.__contains__("Beban") or desc.__contains__("Macam-macam"))) else 0)

    end_item = ['---------','Total', data['Kas'].sum(), data['BHP'].sum(), data['Peralatan Kantor'].sum(), data['Persekot Sewa'].sum(), data['Utang Usaha'].sum(), data['Utang Bank'].sum(), data['Modal'].sum(), data['Prive'].sum(), data['Pendapatan'].sum(), data['Biaya'].sum()]

    df_persamaan.loc[len(df_persamaan)+1] = end_item

    st.table(df_persamaan)

    st.write('---')

    click = st.button("Export Persamaan")
    path = 'C:/Users/ASUS/Downloads/persamaan.xlsx'

    if click:
        with pd.ExcelWriter(path, mode='w') as writer:
            df_persamaan.to_excel(writer, sheet_name='Persamaan Dasar', index=False)

        st.success("Data Berhasil di Export :white_check_mark:")

with tab2:
    st.subheader("Laporan Laba Rugi :chart:")

    df_labarugi = data[(data['Kategori_2'] == "Pendapatan") | (data['Biaya'] < 0) | (data['Pendapatan'] > 0)]
    df_labarugi.drop(columns=['Tanggal','Kas','BHP','Peralatan Kantor','Persekot Sewa','Utang Usaha','Utang Bank','Modal','Prive','Kategori_1','Kategori_2'], inplace=True)
    
    total = df_labarugi['Pendapatan'].sum() + df_labarugi['Biaya'].sum()

    df_labarugi['Laba'] = ''

    end_items = ["Laba" if total > 0 else "Rugi", "----- Pendapatan + Biaya -----", '-'*15, total]

    df_labarugi.loc[df_labarugi.index[-1]+1] = end_items

    df_labarugi = df_labarugi.set_index(pd.Index([i + 1 for i in range(len(df_labarugi))]))

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Total Pendapatan :chart_with_upwards_trend:", value=data['Pendapatan'].sum())

    with col2:
        st.metric(label='Total Biaya :chart_with_downwards_trend:', value=data['Biaya'].sum())

    st.table(df_labarugi)

    click = st.button('Export Laba Rugi')

    if click:
        with pd.ExcelWriter(path, mode='a', if_sheet_exists='replace') as writer:
            df_labarugi.to_excel(writer, sheet_name='Laporan Laba Rugi', index=False)

        st.success("Data Berhasil di Export :white_check_mark:")

with tab3:
    st.subheader("Perubahan Ekuitas :moneybag:")

    modal_awal = dict_items['Modal'][0]
    prive = data['Prive'].sum()
    laba_bersih = total
    modal_laba = modal_awal + laba_bersih

    total_ekuitas = modal_laba + prive

    df_perb_ekuitas = pd.DataFrame(data=[modal_awal, laba_bersih, modal_laba, prive, total_ekuitas], index=['Modal Awal','Laba Bersih','Modal + Laba','Prive',10*'-'+' Total Ekuitas '+"-"*10], columns=[''])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label='Modal Awal :dollar:', value=modal_awal)

    with col2:
        st.metric(label='Laba Bersih :currency_exchange:', value=total)

    with col3:
        st.metric(label='Prive :euro:', value=prive)

    st.table(df_perb_ekuitas)

    click = st.button('Export Perb.Ekuitas')

    if click:
        with pd.ExcelWriter(path, mode='a', if_sheet_exists='replace') as writer:
            df_perb_ekuitas.to_excel(writer, sheet_name='Perubahan Ekuitas', index=True)

        st.success("Data Berhasil di Export :white_check_mark:")

with tab4:
    st.subheader("Neraca :scales:")

    # Aset
    total_kas = data['Kas'].sum()
    total_bhp = data['BHP'].sum()
    total_peralatan_kantor = data['Peralatan Kantor'].sum()
    total_persekot_sewa = data['Persekot Sewa'].sum()

    # Kewajiban
    total_utg_usaha = data['Utang Usaha'].sum()
    total_utg_bank = data['Utang Bank'].sum()

    # Ekuitas
    jml_kewajiban = total_utg_usaha + total_utg_bank
    ekuitas_akhir = total_ekuitas

    jml_aset = total_kas + total_bhp + total_peralatan_kantor + total_persekot_sewa
    jml_kewajiban = total_utg_usaha + total_utg_bank
    kewajiban_ekuitas = jml_kewajiban + ekuitas_akhir

    dict_neraca = {
        'Aset': '',
        'Kas': [total_kas, '', ''],
        'Bahan Habis Pakai': [total_bhp, '', ''],
        'Peralatan Kantor': [total_peralatan_kantor, '', ''],
        'Persekot Sewa': [total_persekot_sewa, '', ''],
        'Kewajiban': '',
        'Utang Usaha': ['', total_utg_usaha, ''],
        'Utang Bank': ['', total_utg_bank, ''],
        'Ekuitas': ['', '', ekuitas_akhir],
        'Total Aset, Kewajiban, Ekuitas': [10*'-', 10*"-", 10*'-'],
        'Jumlah': [jml_aset, jml_kewajiban, ekuitas_akhir]
    }

    neraca = pd.DataFrame(dict_neraca, index=['Aset','Kewajiban','Ekuitas'])

    neraca_2 = neraca.copy().T

    col1, col2, col3 = st.columns(3)

    with col1:
        value = data["Kas"].sum() + data["BHP"].sum() + data["Peralatan Kantor"].sum() + data["Persekot Sewa"].sum()
        st.metric(label='Aset :chart:', value=value)

    with col2:
        value = data['Utang Bank'].sum() + data['Utang Usaha'].sum()
        st.metric(label='Kewajiban :receipt:', value=value)

    with col3:
        value = (data['Modal'].sum() + data['Prive'].sum() + data['Pendapatan'].sum() + data['Biaya'].sum())
        st.metric(label='Ekuitas :moneybag:', value=value)

    st.table(neraca.T)

    click = st.button('Export Neraca')

    if click:
        with pd.ExcelWriter(path, mode='a', if_sheet_exists='replace') as writer:
            neraca_2.to_excel(writer, sheet_name='Neraca', index=True)

        st.success("Data Berhasil di Export :white_check_mark:")

with tab5:
    st.subheader("Arus Kas")

    # kas = data['Kas'].sum()
    # ttl_peralatan_kantor = data['Peralatan Kantor'].sum()
    

with tab6:
    st.subheader("Visualisasi Data :bar_chart:")

    col1, col2, col3 = st.columns(3)

    with col1:
        value = (data.Kas.sum() + data.BHP.sum() + data['Peralatan Kantor'].sum() + data['Persekot Sewa'].sum())
        st.metric(label="Total Aset :chart:", value=value, delta=amount if cat2 != 'BHP' else -amount)
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(
            x=['Kas','BHP','Peralatan Kantor','Persekot Sewa'],
            y=[data.Kas.sum() if data.Kas.sum() > 0 else 0,
               data.BHP.sum() if data.BHP.sum() > 0 else 0,
               data['Peralatan Kantor'].sum() if data['Peralatan Kantor'].sum() > 0 else 0,
               data['Persekot Sewa'].sum() if data['Persekot Sewa'].sum() > 0 else 0],
            palette='winter',
            saturation=1,
        )
        plt.title('Aset', fontsize=24, fontweight='bold', pad=16)
        plt.tick_params(labelsize=14, axis='both')
        st.pyplot(fig)

    with col2:
        value = (data['Utang Bank'].sum() + data['Utang Usaha'].sum())
        st.metric(label="Total Kewajiban :receipt:", value=value, delta=amount if cat2 == 'Utang Bank' else 0)
        fig, ax = plt.subplots(figsize=(10,8))
        ax = sns.barplot(
            x=['Utang Bank','Utang Usaha'],
            y= [data['Utang Bank'].sum() if data['Utang Bank'].sum() > 0 else 0,
                data['Utang Usaha'].sum() if data['Utang Usaha'].sum() > 0 else 0],
            palette='winter',
            saturation=1,
        )
        plt.title('Kewajiban', fontsize=24, fontweight='bold', pad=12)
        plt.tick_params(labelsize=14, axis='both')
        st.pyplot(fig)

    with col3:
        value = (data['Modal'].sum() + data['Prive'].sum() + data['Pendapatan'].sum() + data['Biaya'].sum())
        st.metric(label="Total Ekuitas :moneybag:", value=value, delta=amount if cat2 == 'Modal' or cat2 == 'Prive' or cat2 == 'Pendapatan' or cat2 == 'Biaya' or cat2 == 'Kas' else 0)
        fig, ax = plt.subplots(figsize=(10,8))
        ax = sns.barplot(
            x=['Modal','Prive','Pendapatan','Biaya'],
            y=[data.Modal.sum() if data.Modal.sum() > 0 else 0,
               data.Prive.sum() if data.Prive.sum() > 0 else 0,
               data.Pendapatan.sum() if data.Pendapatan.sum() > 0 else 0,
               data.Biaya.sum() if data.Biaya.sum() > 0 else 0],
            palette='winter',
            saturation=1
        )
        plt.title('Ekuitas', fontsize=24, fontweight='bold', pad=16)
        plt.tick_params(labelsize=14, axis='both')
        st.pyplot(fig)
