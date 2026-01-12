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

# Perbaiki format tanggal
df["tanggal_pinjam"] = pd.to_datetime(df["tanggal_pinjam"], errors="coerce")
df["tanggal_kembali"] = pd.to_datetime(df["tanggal_kembali"], errors="coerce")

# Tangani missing value
df["tanggal_kembali"] = df["tanggal_kembali"].fillna(
    df["tanggal_pinjam"] + pd.to_timedelta(df["jumlah_hari_pinjam"], unit="D")
)

df["denda"] = df["denda"].fillna(0)

# Hapus data tidak logis
df = df[df["jumlah_hari_pinjam"] >= 0]

# Pastikan tipe data sesuai
df["jumlah_hari_pinjam"] = df["jumlah_hari_pinjam"].astype(int)
df["denda"] = df["denda"].astype(int)

print("=== Data Setelah Cleaning ===")
print(df)
print("\n")

dataset_bersih = df.copy()

# =========================
# ANALISIS DATA
# =========================
total_peminjaman = len(dataset_bersih)
kategori_terbanyak = dataset_bersih["kategori"].value_counts().idxmax()
rata_rata_hari = dataset_bersih["jumlah_hari_pinjam"].mean()
total_denda = dataset_bersih["denda"].sum()
persentase_terlambat = (
    dataset_bersih["status_pengembalian"]
    .value_counts(normalize=True)["Terlambat"] * 100
)

# =========================
# OUTPUT
# =========================
print("=== HASIL ANALISIS DATA PERPUSTAKAAN ===")
print("Total peminjaman buku:", total_peminjaman)
print("Kategori buku paling sering dipinjam:", kategori_terbanyak)
print("Rata-rata jumlah hari peminjaman:", round(rata_rata_hari, 2))
print("Total denda yang diperoleh perpustakaan: Rp", total_denda)
print("Persentase pengembalian terlambat:", round(persentase_terlambat, 2), "%")

# =========================
# VISUALISASI (1 GRAFIK SAJA)
# =========================
print("\nMenampilkan grafik jumlah peminjaman per kategori...")

jumlah_per_kategori = dataset_bersih["kategori"].value_counts()

plt.figure()
jumlah_per_kategori.plot(kind="bar")
plt.xlabel("Kategori Buku")
plt.ylabel("Jumlah Peminjaman")
plt.title("Grafik Jumlah Peminjaman Buku per Kategori")
plt.show()
