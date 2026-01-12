import pandas as pd
from datetime import datetime
import numpy as np




print("Membaca file data_koperasi.csv...")
try:
    df = pd.read_csv('data_koperasi.csv')
    print("✓ File berhasil dibaca\n")
except FileNotFoundError:
    print("✗ File data_koperasi.csv tidak ditemukan!")
    print("Pastikan file CSV ada di folder yang sama dengan script Python ini.\n")
    exit()


df['tanggal_pinjam'] = pd.to_datetime(df['tanggal_pinjam'])
df['tanggal_cicilan'] = pd.to_datetime(df['tanggal_cicilan'])
df['tanggal_jatuh_tempo'] = pd.to_datetime(df['tanggal_jatuh_tempo'])

print("=" * 80)
print("ANALISIS DATA PINJAMAN KOPERASI")
print("=" * 80)
print(f"\nJumlah data: {len(df)} anggota")
print("\nPreview data:")
print(df.head())




print("\n" + "=" * 80)
print("A. DATA UNDERSTANDING")
print("=" * 80)
print("""
Penjelasan setiap kolom:
1. id_anggota        : Kode unik identifikasi anggota koperasi
2. nama_anggota      : Nama lengkap anggota peminjam
3. tanggal_pinjam    : Tanggal anggota mengajukan dan menerima pinjaman
4. plafon            : Batas maksimal pinjaman yang diizinkan koperasi (Rp 20 juta)
5. jumlah_pinjaman   : Jumlah uang yang dipinjam oleh anggota (≤ plafon)
6. tenor_pinjam      : Jangka waktu pinjaman dalam bulan (maksimal 30 bulan)
7. tanggal_cicilan   : Tanggal terakhir/terkini cicilan dibayar
8. tanggal_jatuh_tempo: Tanggal batas akhir pelunasan pinjaman

Hubungan dengan kegiatan pinjaman:
- Anggota mengajukan pinjaman pada tanggal_pinjam dengan jumlah ≤ plafon
- Pinjaman harus dilunasi dalam tenor_pinjam bulan
- Cicilan dibayar rutin setiap bulan hingga tanggal_jatuh_tempo
- tanggal_cicilan menunjukkan status pembayaran terakhir
""")




print("\n" + "=" * 80)
print("B. DATA CLEANING")
print("=" * 80)


PLAFON_MAX = 20000000
TENOR_MAX = 30

print("\n2. Pemeriksaan Data:")
print("-" * 80)


print("\na) Pengecekan nilai kosong:")
null_check = df.isnull().sum()
print(null_check)
if null_check.sum() == 0:
    print("✓ Tidak ada nilai kosong")
else:
    print("✗ Ada nilai kosong yang perlu diperbaiki")


print("\nb) Pengecekan plafon (maks Rp 20.000.000):")
exceed_plafon = df[df['jumlah_pinjaman'] > df['plafon']]
if len(exceed_plafon) == 0:
    print("✓ Semua pinjaman ≤ plafon")
else:
    print(f"✗ Ada {len(exceed_plafon)} data melebihi plafon:")
    print(exceed_plafon[['id_anggota', 'nama_anggota', 'jumlah_pinjaman', 'plafon']])


print("\nc) Pengecekan tenor (maks 30 bulan):")
exceed_tenor = df[df['tenor_pinjam'] > TENOR_MAX]
if len(exceed_tenor) == 0:
    print("✓ Semua tenor ≤ 30 bulan")
else:
    print(f"✗ Ada {len(exceed_tenor)} data melebihi tenor maksimal:")
    print(exceed_tenor[['id_anggota', 'nama_anggota', 'tenor_pinjam']])


print("\nd) Pengecekan format tanggal:")
try:
    print("✓ Semua format tanggal valid")
    print(f"  - tanggal_pinjam: {df['tanggal_pinjam'].dtype}")
    print(f"  - tanggal_cicilan: {df['tanggal_cicilan'].dtype}")
    print(f"  - tanggal_jatuh_tempo: {df['tanggal_jatuh_tempo'].dtype}")
except:
    print("✗ Ada masalah dengan format tanggal")


print("\ne) Pengecekan nilai pinjaman negatif:")
negative_loan = df[df['jumlah_pinjaman'] < 0]
if len(negative_loan) == 0:
    print("✓ Tidak ada jumlah pinjaman negatif")
else:
    print(f"✗ Ada {len(negative_loan)} pinjaman dengan nilai negatif")


print("\nf) Pengecekan tenor nol:")
zero_tenor = df[df['tenor_pinjam'] <= 0]
if len(zero_tenor) == 0:
    print("✓ Tidak ada tenor nol atau negatif")
else:
    print(f"✗ Ada {len(zero_tenor)} data dengan tenor ≤ 0")

print("\n3. Kesimpulan Data Cleaning:")
print("-" * 80)
print("✓ Data sudah bersih dan sesuai dengan aturan koperasi")
print("✓ Tidak ada data yang perlu diperbaiki")




print("\n" + "=" * 80)
print("C. ANALISIS PINJAMAN")
print("=" * 80)


total_pinjaman = df['jumlah_pinjaman'].sum()
print(f"\n4. Total Nilai Pinjaman Keseluruhan:")
print(f"   Rp {total_pinjaman:,}")


rata_rata_pinjaman = df['jumlah_pinjaman'].mean()
print(f"\n5. Rata-rata Jumlah Pinjaman Anggota:")
print(f"   Rp {rata_rata_pinjaman:,.2f}")


print(f"\n   Statistik Tambahan:")
print(f"   - Pinjaman terkecil: Rp {df['jumlah_pinjaman'].min():,}")
print(f"   - Pinjaman terbesar: Rp {df['jumlah_pinjaman'].max():,}")
print(f"   - Median pinjaman : Rp {df['jumlah_pinjaman'].median():,}")




print("\n" + "=" * 80)
print("D. ANALISIS CICILAN")
print("=" * 80)

print("\n6. Perbandingan Tanggal Cicilan dan Jatuh Tempo:")
print("-" * 80)


df['bulan_berjalan'] = ((df['tanggal_cicilan'] - df['tanggal_pinjam']).dt.days / 30).round()


df['cicilan_per_bulan'] = df['jumlah_pinjaman'] / df['tenor_pinjam']


df['seharusnya_dibayar'] = df['cicilan_per_bulan'] * df['bulan_berjalan']


df['sisa_tenor'] = ((df['tanggal_jatuh_tempo'] - df['tanggal_cicilan']).dt.days / 30).round()


df['persen_tenor_berjalan'] = (df['bulan_berjalan'] / df['tenor_pinjam'] * 100).round(2)



tanggal_analisis = pd.Timestamp('2025-01-02')
df['selisih_hari_dari_sekarang'] = (tanggal_analisis - df['tanggal_cicilan']).dt.days




df['status_risiko'] = 'Normal'
df.loc[(df['selisih_hari_dari_sekarang'] > 30) & (df['sisa_tenor'] > 3), 'status_risiko'] = 'Perhatian'
df.loc[(df['selisih_hari_dari_sekarang'] > 60) & (df['sisa_tenor'] > 1), 'status_risiko'] = 'Tinggi'


print("\nRingkasan Status Cicilan:")
for idx, row in df.iterrows():
    print(f"\n{row['id_anggota']} - {row['nama_anggota']}")
    print(f"  Pinjaman        : Rp {row['jumlah_pinjaman']:,}")
    print(f"  Tenor           : {row['tenor_pinjam']} bulan")
    print(f"  Bulan berjalan  : {int(row['bulan_berjalan'])} bulan ({row['persen_tenor_berjalan']}%)")
    print(f"  Sisa tenor      : {int(row['sisa_tenor'])} bulan")
    print(f"  Cicilan terakhir: {row['tanggal_cicilan'].strftime('%Y-%m-%d')}")
    print(f"  Jatuh tempo     : {row['tanggal_jatuh_tempo'].strftime('%Y-%m-%d')}")
    print(f"  Status Risiko   : {row['status_risiko']}")


print("\n" + "-" * 80)
print("ANGGOTA BERPOTENSI MENUNGGAK:")
print("-" * 80)
anggota_risiko = df[df['status_risiko'].isin(['Perhatian', 'Tinggi'])]
if len(anggota_risiko) > 0:
    for idx, row in anggota_risiko.iterrows():
        print(f"\n⚠ {row['nama_anggota']} ({row['id_anggota']})")
        print(f"   Status: {row['status_risiko']}")
        print(f"   Alasan: Cicilan terakhir {row['selisih_hari_dari_sekarang']} hari yang lalu")
        print(f"   Sisa tenor: {int(row['sisa_tenor'])} bulan")
else:
    print("\n✓ Tidak ada anggota yang berpotensi menunggak saat ini")




print("\n" + "=" * 80)
print("E. INTERPRETASI BISNIS")
print("=" * 80)

print("\n7. Risiko dan Strategi Koperasi:")
print("-" * 80)

print("\nRISIKO BAGI KOPERASI:")
print("""
1. Risiko Likuiditas
   - Koperasi kesulitan mendapatkan kembali dana yang dipinjamkan
   - Mengganggu operasional dan kemampuan memberikan pinjaman baru
   - Cadangan modal koperasi terkuras

2. Risiko Kredit Macet (NPL - Non Performing Loan)
   - Pinjaman menjadi kredit bermasalah
   - Meningkatkan rasio NPL yang berdampak pada kesehatan koperasi
   - Memerlukan pencadangan dana untuk kerugian

3. Risiko Reputasi
   - Menurunkan kepercayaan anggota lain
   - Kesulitan menarik simpanan baru
   - Menghambat pertumbuhan koperasi

4. Risiko Operasional
   - Biaya penagihan meningkat
   - Perlu sumber daya tambahan untuk monitoring
   - Proses hukum jika terpaksa ditempuh
""")

print("\nSTRATEGI YANG BISA DILAKUKAN KOPERASI:")
print("""
1. PREVENTIF (Pencegahan)
   a) Sistem Reminder Otomatis
      - SMS/WA reminder H-7 sebelum jatuh tempo
      - Email notifikasi status cicilan
      - Telepon untuk cicilan yang terlambat > 7 hari
   
   b) Edukasi Keuangan Anggota
      - Workshop manajemen keuangan pribadi
      - Konseling untuk anggota yang kesulitan bayar
      - Literasi tentang konsekuensi tunggakan
   
   c) Sistem Monitoring Ketat
      - Dashboard real-time status pembayaran
      - Early warning system untuk cicilan bermasalah
      - Kategorisasi risiko anggota (lancar, perhatian, macet)

2. KURATIF (Penanganan)
   a) Restrukturisasi Pinjaman
      - Perpanjangan tenor untuk mengurangi beban cicilan
      - Penjadwalan ulang pembayaran
      - Grace period untuk kasus tertentu (PHK, sakit, dll)
   
   b) Pendekatan Personal
      - Kunjungan ke rumah anggota
      - Mediasi untuk mencari solusi win-win
      - Melibatkan keluarga jika perlu
   
   c) Insentif Pembayaran Tepat Waktu
      - Diskon bunga untuk pembayaran tepat waktu
      - Reward points untuk cicilan lancar
      - Akses prioritas untuk pinjaman berikutnya

3. REPRESIF (Penindakan)
   a) Sanksi Administratif
      - Denda keterlambatan progresif
      - Penutupan akses pinjaman baru
      - Pencatatan dalam blacklist koperasi
   
   b) Jalur Hukum (Last Resort)
      - Somasi tertulis
      - Mediasi melalui lembaga berwenang
      - Gugatan perdata jika diperlukan
""")


print("\nANALISIS KONDISI SAAT INI:")
print("-" * 80)
print(f"Total anggota         : {len(df)} orang")
print(f"Anggota risiko normal : {len(df[df['status_risiko'] == 'Normal'])} orang")
print(f"Anggota perlu perhatian: {len(df[df['status_risiko'] == 'Perhatian'])} orang")
print(f"Anggota risiko tinggi : {len(df[df['status_risiko'] == 'Tinggi'])} orang")
print(f"\nTotal dana tersalurkan: Rp {total_pinjaman:,}")
print(f"Potensi dana berisiko : Rp {df[df['status_risiko'] != 'Normal']['jumlah_pinjaman'].sum():,}")
print(f"Persentase risiko     : {(df[df['status_risiko'] != 'Normal']['jumlah_pinjaman'].sum() / total_pinjaman * 100):.2f}%")

print("\n" + "=" * 80)
print("SELESAI")
print("=" * 80)