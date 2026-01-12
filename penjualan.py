import pandas as pd
import numpy as np

# ========== DATA AWAL ==========
print("="*80)
print("SOAL LATIHAN DATA SCIENCE - ANALISIS PENJUALAN")
print("="*80)

data = {
    "id_transaksi": ["T001", "T002", "T003", "T004", "T005", "T006", "T007", 
                     "T008", "T009", "T010", "T011", "T012", "T013", "T014", "T015"],
    "produk": ["Laptop", "Mouse", "Keyboard", "Monitor", "Printer", "Flashdisk", 
               "Headset", "Webcam", "Speaker", "Harddisk Eksternal", "Mousepad", 
               "SSD", "Router", "Kabel HDMI", "Power Bank"],
    "jumlah": [2, 5, None, 1, -1, 10, 3, None, 4, -2, 8, 1, 2, None, 6],
    "harga": [7500000, 150000, 350000, 2500000, 1800000, 75000, 450000, 
              600000, 550000, 1200000, 50000, 1500000, 900000, 85000, 350000]
}

df_original = pd.DataFrame(data)
print("\n📊 DATA AWAL (Sebelum Cleaning):")
print(df_original)
print("\n⚠️ Masalah pada data:")
print(f"- Missing values pada kolom 'jumlah': {df_original['jumlah'].isna().sum()} record")
print(f"- Nilai negatif pada kolom 'jumlah': {(df_original['jumlah'] < 0).sum()} record")

# ========== PERTANYAAN 1 & 2: DATA CLEANING ==========
print("\n" + "="*80)
print("JAWABAN 1 & 2: PROSES DATA CLEANING")
print("="*80)

print("\n📋 LANGKAH-LANGKAH DATA CLEANING:")
print("\n1. Identifikasi Missing Values")
print("   - Kolom 'jumlah' memiliki missing values (NaN/kosong)")
print("   - Strategi: Isi dengan 0 atau hapus record (pilih: isi dengan 0)")

print("\n2. Identifikasi Nilai Anomali")
print("   - Kolom 'jumlah' memiliki nilai negatif (-1, -2)")
print("   - Nilai negatif tidak logis untuk jumlah penjualan")
print("   - Strategi: Konversi ke nilai absolut")

print("\n3. Validasi Tipe Data")
print("   - Pastikan kolom 'jumlah' bertipe numeric")
print("   - Pastikan kolom 'harga' bertipe numeric")

print("\n4. Pengecekan Duplikasi")
print("   - Cek apakah ada id_transaksi yang duplikat")

# ========== PERTANYAAN 3: IMPLEMENTASI DATA CLEANING ==========
print("\n" + "="*80)
print("JAWABAN 3: IMPLEMENTASI DATA CLEANING MENGGUNAKAN PYTHON (PANDAS)")
print("="*80)

# Copy data untuk cleaning
df = df_original.copy()

print("\n🔧 Proses Cleaning:")

# Step 1: Handle Missing Values
print("\nStep 1: Handle Missing Values")
print(f"   Before: {df['jumlah'].isna().sum()} missing values")
df["jumlah"] = df["jumlah"].fillna(0)
print(f"   After: {df['jumlah'].isna().sum()} missing values")
print(f"   ✓ Missing values diisi dengan 0")

# Step 2: Handle Negative Values
print("\nStep 2: Handle Negative Values")
negative_count = (df["jumlah"] < 0).sum()
print(f"   Before: {negative_count} negative values")
df["jumlah"] = df["jumlah"].apply(lambda x: abs(x) if x < 0 else x)
print(f"   After: {(df['jumlah'] < 0).sum()} negative values")
print(f"   ✓ Nilai negatif dikonversi ke absolut")

# Step 3: Ensure Numeric Type
print("\nStep 3: Validasi Tipe Data")
df["jumlah"] = pd.to_numeric(df["jumlah"], errors='coerce')
df["harga"] = pd.to_numeric(df["harga"], errors='coerce')
print(f"   ✓ Tipe data 'jumlah': {df['jumlah'].dtype}")
print(f"   ✓ Tipe data 'harga': {df['harga'].dtype}")

# Step 4: Check Duplicates
print("\nStep 4: Cek Duplikasi")
duplicates = df.duplicated(subset=['id_transaksi']).sum()
print(f"   ✓ Jumlah duplikat: {duplicates}")

print("\n✅ DATA CLEANING SELESAI!")
print("\n📊 DATA SETELAH CLEANING:")
print(df)

# ========== PERTANYAAN 4: PENGOLAHAN DATA ==========
print("\n" + "="*80)
print("JAWABAN 4: PENGOLAHAN DATA MENGGUNAKAN PYTHON")
print("="*80)

# Tambahkan kategori produk
kategori_map = {
    "Laptop": "Komputer & Laptop",
    "Mouse": "Aksesoris Komputer",
    "Keyboard": "Aksesoris Komputer",
    "Monitor": "Komputer & Laptop",
    "Printer": "Perangkat Output",
    "Flashdisk": "Storage",
    "Headset": "Audio & Video",
    "Webcam": "Audio & Video",
    "Speaker": "Audio & Video",
    "Harddisk Eksternal": "Storage",
    "Mousepad": "Aksesoris Komputer",
    "SSD": "Storage",
    "Router": "Networking",
    "Kabel HDMI": "Aksesoris Komputer",
    "Power Bank": "Aksesoris Mobile"
}

df["kategori"] = df["produk"].map(kategori_map)

# Hitung total penjualan
df["total_penjualan"] = df["jumlah"] * df["harga"]

print("\n📦 Data dengan Kategori dan Total Penjualan:")
print(df[["id_transaksi", "produk", "kategori", "jumlah", "harga", "total_penjualan"]])

# ========== PERTANYAAN 5: TOTAL PENJUALAN PER PRODUK ==========
print("\n" + "="*80)
print("JAWABAN 5: TOTAL PENJUALAN PER PRODUK")
print("="*80)

total_per_produk = df.groupby("produk").agg({
    "total_penjualan": "sum",
    "jumlah": "sum"
}).reset_index()
total_per_produk.columns = ["Produk", "Total Penjualan (Rp)", "Total Unit Terjual"]
total_per_produk = total_per_produk.sort_values("Total Penjualan (Rp)", ascending=False)

print("\n📊 Tabel Total Penjualan per Produk:")
print(total_per_produk.to_string(index=False))

# ========== PERTANYAAN 6: TOTAL PENJUALAN PER KATEGORI ==========
print("\n" + "="*80)
print("JAWABAN 6: TOTAL PENJUALAN PER KATEGORI")
print("="*80)

total_per_kategori = df.groupby("kategori").agg({
    "total_penjualan": "sum",
    "jumlah": "sum"
}).reset_index()
total_per_kategori.columns = ["Kategori", "Total Penjualan (Rp)", "Total Unit Terjual"]
total_per_kategori = total_per_kategori.sort_values("Total Penjualan (Rp)", ascending=False)

print("\n📊 Tabel Total Penjualan per Kategori:")
print(total_per_kategori.to_string(index=False))

# Hitung persentase kontribusi
total_per_kategori["Persentase (%)"] = (total_per_kategori["Total Penjualan (Rp)"] / 
                                        total_per_kategori["Total Penjualan (Rp)"].sum() * 100).round(2)
print("\n📊 Tabel dengan Persentase Kontribusi:")
print(total_per_kategori.to_string(index=False))

# ========== PERTANYAAN 7: TOP 3 PRODUK ==========
print("\n" + "="*80)
print("JAWABAN 7: TOP 3 PRODUK DENGAN PENJUALAN TERTINGGI")
print("="*80)

top_3_produk = total_per_produk.head(3).copy()
top_3_produk["Ranking"] = [1, 2, 3]
top_3_produk = top_3_produk[["Ranking", "Produk", "Total Penjualan (Rp)", "Total Unit Terjual"]]

print("\n🏆 TOP 3 PRODUK TERLARIS:")
print(top_3_produk.to_string(index=False))

# ========== PERTANYAAN 8a: OUTPUT TABEL ==========
print("\n" + "="*80)
print("JAWABAN 8a: TAMPILAN TABEL HASIL")
print("="*80)

print("\n📊 TABEL 1: Total Penjualan per Produk")
print("-" * 80)
print(total_per_produk.to_string(index=False))

print("\n\n📊 TABEL 2: Total Penjualan per Kategori")
print("-" * 80)
print(total_per_kategori.to_string(index=False))

# ========== PERTANYAAN 8b: OUTPUT TOP 3 ==========
print("\n" + "="*80)
print("JAWABAN 8b: TAMPILAN 3 PRODUK TERLARIS")
print("="*80)

print("\n🏆 TOP 3 PRODUK TERLARIS:")
print("-" * 80)
for idx, row in top_3_produk.iterrows():
    print(f"#{int(row['Ranking'])} {row['Produk']}")
    print(f"   Total Penjualan: Rp {row['Total Penjualan (Rp)']:,.0f}")
    print(f"   Unit Terjual: {int(row['Total Unit Terjual'])} unit")
    print()

# ========== PERTANYAAN 8c: ANALISIS KATEGORI ==========
print("=" * 80)
print("JAWABAN 8c: ANALISIS DAN INTERPRETASI KATEGORI")
print("=" * 80)

kategori_tertinggi = total_per_kategori.iloc[0]
print(f"\n🎯 KATEGORI PALING BERKONTRIBUSI:")
print(f"   Kategori: {kategori_tertinggi['Kategori']}")
print(f"   Total Penjualan: Rp {kategori_tertinggi['Total Penjualan (Rp)']:,.0f}")
print(f"   Kontribusi: {kategori_tertinggi['Persentase (%)']}% dari total penjualan")
print(f"   Unit Terjual: {int(kategori_tertinggi['Total Unit Terjual'])} unit")

print("\n📈 INTERPRETASI KATEGORI:")
print(f"1. {kategori_tertinggi['Kategori']} mendominasi penjualan dengan kontribusi")
print(f"   {kategori_tertinggi['Persentase (%)']}%, menunjukkan bahwa produk-produk dalam kategori ini")
print(f"   memiliki nilai tinggi dan demand yang kuat.")

print("\n2. Urutan kontribusi kategori:")
for idx, row in total_per_kategori.iterrows():
    print(f"   - {row['Kategori']}: {row['Persentase (%)']}%")

print("\n3. Implikasi Bisnis:")
print(f"   - Fokus inventory pada kategori {kategori_tertinggi['Kategori']}")
print(f"   - Tingkatkan marketing untuk kategori dengan persentase rendah")
print(f"   - Pertimbangkan bundle produk antar kategori")

# ========== PERTANYAAN 8d: INTERPRETASI PRODUK TERTINGGI ==========
print("\n" + "="*80)
print("JAWABAN 8d: INTERPRETASI PRODUK DENGAN PENJUALAN TERTINGGI")
print("="*80)

produk_tertinggi = top_3_produk.iloc[0]
print(f"\n🏆 PRODUK DENGAN PENJUALAN TERTINGGI:")
print(f"   Produk: {produk_tertinggi['Produk']}")
print(f"   Total Penjualan: Rp {produk_tertinggi['Total Penjualan (Rp)']:,.0f}")
print(f"   Unit Terjual: {int(produk_tertinggi['Total Unit Terjual'])} unit")

# Hitung harga per unit
produk_data = df[df['produk'] == produk_tertinggi['Produk']].iloc[0]
print(f"   Harga per Unit: Rp {produk_data['harga']:,.0f}")

print("\n💡 INTERPRETASI BISNIS:")
print("\n1. Karakteristik Produk Terlaris:")
print(f"   - {produk_tertinggi['Produk']} adalah produk high-value (harga tinggi)")
print(f"   - Meskipun unit terjual sedikit ({int(produk_tertinggi['Total Unit Terjual'])} unit),")
print(f"     nilai transaksi sangat besar karena harga tinggi")
print(f"   - Margin keuntungan potensial sangat besar")

print("\n2. Strategi Bisnis yang Disarankan:")
print(f"   a. UNTUK PRODUK {produk_tertinggi['Produk'].upper()}:")
print("      • Pastikan stok selalu tersedia (produk flagship)")
print("      • Tingkatkan after-sales service (warranty, support)")
print("      • Tawarkan paket bundle dengan aksesoris")
print("      • Berikan cicilan/payment plan untuk kemudahan pembeli")

print("\n   b. UNTUK PRODUK RANKING 2 & 3:")
for idx in range(1, min(3, len(top_3_produk))):
    prod = top_3_produk.iloc[idx]
    print(f"      • {prod['Produk']}: Pertahankan posisi sebagai produk andalan")

print("\n   c. STRATEGI UMUM:")
print("      • Cross-selling: tawarkan aksesoris saat beli produk utama")
print("      • Up-selling: tawarkan upgrade ke produk premium")
print("      • Loyalty program untuk repeat customer")
print("      • Marketing digital fokus pada produk high-value")

print("\n3. Analisis Perbandingan:")
produk_kedua = top_3_produk.iloc[1] if len(top_3_produk) > 1 else None
if produk_kedua is not None:
    selisih = produk_tertinggi['Total Penjualan (Rp)'] - produk_kedua['Total Penjualan (Rp)']
    print(f"   - Gap penjualan ranking #1 vs #2: Rp {selisih:,.0f}")
    print(f"   - Ini menunjukkan dominasi {produk_tertinggi['Produk']} sangat kuat")

# ========== RINGKASAN AKHIR ==========
print("\n" + "="*80)
print("📊 RINGKASAN STATISTIK KESELURUHAN")
print("="*80)

total_revenue = df["total_penjualan"].sum()
total_units = df["jumlah"].sum()
avg_transaction = df["total_penjualan"].mean()

print(f"\n💰 Total Revenue: Rp {total_revenue:,.0f}")
print(f"📦 Total Unit Terjual: {int(total_units)} unit")
print(f"📈 Rata-rata per Transaksi: Rp {avg_transaction:,.0f}")
print(f"🛍️  Jumlah Transaksi: {len(df)} transaksi")
print(f"📂 Jumlah Kategori: {df['kategori'].nunique()} kategori")
print(f"🏷️  Jumlah Produk Unik: {df['produk'].nunique()} produk")

print("\n" + "="*80)
print("✅ SEMUA SOAL TELAH DIJAWAB LENGKAP!")
print("="*80) 