import streamlit as st

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

# Hanya tampilkan input nilai saat ini setelah nilai variabel disimpan
if st.session_state.get("nilai_variabel_tersimpan", False):
    soal = {}
    for i in range(len(nama_var) - 1):  # Asumsi variabel terakhir adalah yang ditanyakan
        val = st.number_input(f"Masukkan nilai {nama_var[i]} saat ini:", key=f"soal_{nama_var[i]}")
        soal[nama_var[i]] = val

    # Tombol Submit
    if st.button("Submit Perhitungan"):
        # Variabel yang ditanyakan
        dit = nama_var[-1]  # Asumsi variabel terakhir adalah yang ditanyakan

        # Fungsi keanggotaan
        def turun(b, a, x):
            if x <= a:
                return 1
            elif a < x < b:
                return (b - x) / (b - a)
            else:
                return 0
        
        def naik(b, a, x):
            if x <= a:
                return 0
            elif a < x < b:
                return (x - a) / (b - a)
            else:
                return 1
        
        def agregasi_turun(b, a, alfa):
            return b - (alfa * (b - a))
        
        def agregasi_naik(b, a, alfa):
            return alfa * (b - a) + a

        # Hitung derajat keanggotaan
        nk = {}
        for i in nama_var:
            if i != dit:  # Lewati variabel yang ditanyakan
                nk[i + "_naik"] = naik(variabel[i + "_naik"], variabel[i + "_turun"], soal[i])
                nk[i + "_turun"] = turun(variabel[i + "_naik"], variabel[i + "_turun"], soal[i])

        # Tampilkan derajat keanggotaan
        st.subheader("Derajat Keanggotaan:")
        for key, value in nk.items():
            st.write(f"{key}: {value:.4f}")

        # Definisikan aturan fuzzy berdasarkan variabel input
        aturan_fuzzy = []
        for i in range(2**len(nama_var[:-1])):  # Generate semua kombinasi aturan
            rule = []
            for j, var in enumerate(nama_var[:-1]):
                if (i >> j) & 1:
                    rule.append(var + "_naik")
                else:
                    rule.append(var + "_turun")
            
            if i % 2 == 0:  # Aturan sederhana - bisa disesuaikan
                rule.append(dit + "_turun")
            else:
                rule.append(dit + "_naik")
            
            aturan_fuzzy.append(tuple(rule))

        # Hitung nilai alfa dan z
        alfa = []
        z = []

        for rule in aturan_fuzzy:
            kesimpulan = rule[-1]
            kondisi = rule[:-1]
            
            # Hitung fire strength
            a = min(nk[k] for k in kondisi)
            alfa.append(a)

            if kesimpulan == f"{dit}_turun":
                zz = agregasi_turun(variabel[f"{dit}_naik"], variabel[f"{dit}_turun"], a)
            else:  # it's naik
                zz = agregasi_naik(variabel[f"{dit}_naik"], variabel[f"{dit}_turun"], a)
            z.append(zz)

        # Tampilkan hasil agregasi
        st.subheader("Hasil Agregasi:")
        for i in range(len(aturan_fuzzy)):
            st.write(f"Aturan {i+1}: IF {' AND '.join(aturan_fuzzy[i][:-1])} THEN {aturan_fuzzy[i][-1]}")
            st.write(f" - α = {alfa[i]:.4f}, z = {z[i]:.4f}")
            
        # Hindari pembagian dengan nol
        if sum(alfa) > 0:
            z_final = sum(a * zz for a, zz in zip(alfa, z)) / sum(alfa)
            st.success(f"{dit.capitalize()} yang dihasilkan: {z_final:.4f}")
        else:
            st.error(f"Tidak dapat menentukan {dit} (semua alfa = 0)")
