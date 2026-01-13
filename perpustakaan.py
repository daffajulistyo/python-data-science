import pandas as pd
import matplotlib.pyplot as plt

# =========================
# MEMBACA DATASET
# =========================
df = pd.read_csv("pinjaman_buku.csv")

print("=== Data Awal ===")
print(df)
print("\n")

# =========================
# DATA CLEANING
# =========================

# --- NORMALISASI STRING TANGGAL ---
df["tanggal_pinjam"] = (
    df["tanggal_pinjam"]
    .astype(str)
    .str.strip()
    .str.replace("/", "-", regex=False)
)

df["tanggal_kembali"] = (
    df["tanggal_kembali"]
    .astype(str)
    .str.strip()
    .str.replace("/", "-", regex=False)
)

# Konversi ke datetime
df["tanggal_pinjam"] = pd.to_datetime(df["tanggal_pinjam"], errors="coerce")
df["tanggal_kembali"] = pd.to_datetime(df["tanggal_kembali"], errors="coerce")

# Tangani missing value
df["tanggal_kembali"] = df["tanggal_kembali"].fillna(
    df["tanggal_pinjam"] + pd.to_timedelta(df["jumlah_hari_pinjam"], unit="D")
)

df["denda"] = df["denda"].fillna(0)

# Hitung ulang jumlah hari pinjam dari tanggal
df["jumlah_hari_pinjam"] = (
    df["tanggal_kembali"] - df["tanggal_pinjam"]
).dt.days


# Pastikan tipe data sesuai
df["jumlah_hari_pinjam"] = df["jumlah_hari_pinjam"].astype(int)
df["denda"] = df["denda"].astype(int)

# Print tipe data setiap kolom
print("=== Tipe Data Setiap Kolom Setelah Cleaning ===")
print(df.dtypes)
print("\n")

dataset_bersih = df.copy()

print("=== Data Setelah Cleaning ===")
print(dataset_bersih)
print("\n")

# =========================
# ANALISIS DATA
# =========================


total_peminjaman = len(dataset_bersih)
kategori_terbanyak = dataset_bersih["kategori"].value_counts().idxmax()
rata_rata_hari = dataset_bersih["jumlah_hari_pinjam"].mean()
total_denda = dataset_bersih["denda"].sum()
terlambat_per_kategori = dataset_bersih[dataset_bersih['status_pengembalian' ]=='Terlambat']['kategori'].value_counts()
persentase_terlambat = (dataset_bersih["status_pengembalian"].value_counts(normalize=True)["Terlambat"] * 100)

# =========================
# OUTPUT
# =========================
print("=== HASIL ANALISIS DATA PERPUSTAKAAN ===")
print("Total peminjaman buku:", total_peminjaman)
print("Kategori buku paling sering dipinjam:", kategori_terbanyak)
print("Rata-rata jumlah hari peminjaman:", round(rata_rata_hari, 2))
print("Total denda yang diperoleh perpustakaan: Rp", total_denda)
print("Jumlah peminjaman terlambat per kategori:", terlambat_per_kategori.head(2))
print("Persentase pengembalian terlambat:", round(persentase_terlambat, 2), "%")

# =========================
# VISUALISASI (1 GRAFIK)
# =========================
terlambat_per_kategori.plot(kind='bar')
plt.title('Jumlah Keterlambatan per Kategori Buku')
plt.xlabel('Kategori')
plt.ylabel('Jumlah Terlambat')
plt.show()
