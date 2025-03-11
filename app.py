import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Judul aplikasi
st.title("Aplikasi Fuzzy Logic")

# Input jumlah variabel
var = st.number_input("Jumlah variabel:", min_value=1, value=2, step=1)

# Input nama variabel
nama_var = []
for i in range(var):
    nama = st.text_input(f"Masukkan nama variabel ke-{i+1}:", key=f"var_{i}")
    if nama:
        nama_var.append(nama)

# Tombol Submit untuk nama variabel
if st.button("Simpan Nama Variabel"):
    st.session_state["nama_variabel_tersimpan"] = True

# Hanya tampilkan input nilai jika semua variabel sudah diisi
if st.session_state.get("nama_variabel_tersimpan", False) and len(nama_var) == var:
    variabel = {}
    for i in nama_var:
        st.subheader(f"Masukkan nilai untuk variabel: {i}")
        up = st.number_input(f"Masukkan nilai naik untuk {i}:", key=f"up_{i}")
        down = st.number_input(f"Masukkan nilai turun untuk {i}:", key=f"down_{i}")
        variabel[i + "_naik"] = up
        variabel[i + "_turun"] = down

    # Tombol Submit untuk nilai variabel
    if st.button("Simpan Nilai Variabel"):
        st.session_state["nilai_variabel_tersimpan"] = True

# Definisikan fungsi keanggotaan
def turun(b, a, x):
    return 1 if x <= a else (b - x) / (b - a) if a < x < b else 0

def naik(b, a, x):
    return 0 if x <= a else (x - a) / (b - a) if a < x < b else 1

# Hanya tampilkan input nilai saat ini setelah nilai variabel disimpan
if st.session_state.get("nilai_variabel_tersimpan", False):
    soal = {}
    for i in range(len(nama_var) - 1):  # Asumsi variabel terakhir adalah yang ditanyakan
        val = st.number_input(f"Masukkan nilai {nama_var[i]} saat ini:", key=f"soal_{nama_var[i]}")
        soal[nama_var[i]] = val

    # Tombol Submit
    if st.button("Submit Perhitungan"):
        dit = nama_var[-1]  # Variabel yang ditanyakan

        # Hitung derajat keanggotaan
        nk = {}
        for i in nama_var:
            if i != dit:
                nk[i + "_naik"] = naik(variabel[i + "_naik"], variabel[i + "_turun"], soal[i])
                nk[i + "_turun"] = turun(variabel[i + "_naik"], variabel[i + "_turun"], soal[i])
        
        st.subheader("Derajat Keanggotaan:")
        for key, value in nk.items():
            st.write(f"{key}: {value:.4f}")

    # Tombol untuk menampilkan grafik
    if st.button("Tampilkan Grafik Keanggotaan"):
        plt.figure(figsize=(8, 4))
        x = np.linspace(variabel[nama_var[0] + "_turun"], variabel[nama_var[0] + "_naik"], 100)
        y_turun = [turun(variabel[nama_var[0] + "_naik"], variabel[nama_var[0] + "_turun"], xi) for xi in x]
        y_naik = [naik(variabel[nama_var[0] + "_naik"], variabel[nama_var[0] + "_turun"], xi) for xi in x]
        
        plt.plot(x, y_turun, label=f"{nama_var[0]} Turun", color='blue')
        plt.plot(x, y_naik, label=f"{nama_var[0]} Naik", color='red')
        plt.xlabel("Nilai Variabel")
        plt.ylabel("Derajat Keanggotaan")
        plt.title(f"Fungsi Keanggotaan untuk {nama_var[0]}")
        plt.legend()
        st.pyplot(plt)
