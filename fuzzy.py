var = int(input("Jumlah variabel: "))
nama_var = []

for i in range(var):
    nama = input(f"Masukkan nama variabel ke-{i+1}: ")
    nama_var.append(nama)

variabel = {}

for i in nama_var:
     print(f"\nMasukkan nilai untuk variabel: {i}")
     up = int(input("Masukkan nilai naik: "))
     down = int(input("Masukkan nilai turun: "))
     variabel[i + "_naik"] = up
     variabel[i + "_turun"] = down
print("\nData Variabel yang Dimasukkan:")
for key, value in variabel.items():
     print(f"{key}: {value}")

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

# Get the soal values from user
soal = {}
for i in range(len(nama_var) - 1):  # Assuming last variable is the one being asked
     val = int(input(f"Masukkan nilai {nama_var[i]} saat ini: "))
     soal[nama_var[i]] = val

# Get the variable being asked
dit = nama_var[-1]  # Assuming last variable is the one being asked

# Calculate membership degrees
nk = {}
for i in nama_var:
     if i != dit:  # Skip the variable being asked
          nk[i + "_naik"] = naik(variabel[i + "_naik"], variabel[i + "_turun"], soal[i])
          nk[i + "_turun"] = turun(variabel[i + "_naik"], variabel[i + "_turun"], soal[i])

print("\nDerajat Keanggotaan:")
for key, value in nk.items():
     print(f"{key}: {value:.4f}")

# Define fuzzy rules based on input variables
aturan_fuzzy = []
for i in range(2**len(nama_var[:-1])):  # Generate all rule combinations
     rule = []
     for j, var in enumerate(nama_var[:-1]):
          if (i >> j) & 1:
                rule.append(var + "_naik")
          else:
                rule.append(var + "_turun")
     
     if i % 2 == 0:  # Simple rule assignment - can be customized
          rule.append(dit + "_turun")
     else:
          rule.append(dit + "_naik")
     
     aturan_fuzzy.append(tuple(rule))

alfa = []
z = []

for rule in aturan_fuzzy:
     kesimpulan = rule[-1]
     kondisi = rule[:-1]
     
     # Calculate fire strength
     a = min(nk[k] for k in kondisi)
     alfa.append(a)

     if kesimpulan == f"{dit}_turun":
        zz = agregasi_turun(variabel[f"{dit}_naik"], variabel[f"{dit}_turun"], a)
     else:  # it's naik
        zz = agregasi_naik(variabel[f"{dit}_naik"], variabel[f"{dit}_turun"], a)
     z.append(zz)

print("\nHasil Agregasi:")
for i in range(len(aturan_fuzzy)):
     print(f"Aturan {i+1}: IF {' AND '.join(aturan_fuzzy[i][:-1])} THEN {aturan_fuzzy[i][-1]}")
     print(f" - α = {alfa[i]:.4f}, z = {z[i]:.4f}")
     
# Avoid division by zero
if sum(alfa) > 0:
     z_final = sum(a * zz for a, zz in zip(alfa, z)) / sum(alfa)
     print(f"\n{dit.capitalize()} yang dihasilkan: {z_final:.4f}")
else:
     print(f"\nTidak dapat menentukan {dit} (semua alfa = 0)")