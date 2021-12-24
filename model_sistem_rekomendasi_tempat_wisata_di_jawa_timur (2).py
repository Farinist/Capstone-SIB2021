# -*- coding: utf-8 -*-
"""Model Sistem Rekomendasi Tempat Wisata di Jawa Timur.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fxwSSE2ZGgAs37Sg7ozLVdymw-v5MBUH

# **Sistem Rekomendasi**: Rekomendasi Tempat Wisata di Jawa Timur dengan Content-based Filtering
---
##### Oleh : Samuel Partogi Pakpahan dan Farin Istighfarizky
##### Capstone Project - Studi Independen Bersertifikat x Dicoding

# **Pendahuluan**

Pada proyek ini akan dibuat sistem rekomendasi tempat wisata di Jawa Timur menggunakan ***content-based filtering***. Untuk memudahkan navigasi gunakan menu *Table of Contents* di kanan atas Google Colaboratory.

# **1. Mengimpor library yang dibutuhkan**
"""

# Untuk pengolahan data
import pandas as pd
import numpy as np

"""# **2. Mempersiapkan Dataset dan Pemahaman Data** ***(Data Understanding)***

![Sampul Dataset](https://raw.githubusercontent.com/samuelpakpahan20/Capstone-SIB2021/master/images/sampul.PNG)

Informasi Dataset :

Jenis | Keterangan
--- | ---
Sumber | [Kaggle Dataset : Info Tempat Wisata](https://www.kaggle.com/azharianisah/infotempatwisata)
Lisensi | CC0: Public Domain
Rating Penggunaan | 0.0
Jenis dan Ukuran Berkas | zip (46 kB)

## Memuat Data pada sebuah Dataframe menggunakan *pandas*
"""

# Memuat data pada dataframe di setiap variable
wisata = pd.read_excel("InfoWisata.xlsx")
rating = pd.read_excel("Reviewer.xlsx")

# Pratinjau dataset wisata
wisata.head()

# Pratinjau dataset rating
rating.head()

# Melihat distribusi rating pada data
rating.describe()

"""Dari output di atas, diketahui bahwa nilai maksimum rating adalah 5 dan nilai minimumnya adalah 3.5. Artinya, skala rating berkisar antara 3.5 hingga 5.

# **3. Data Preprocessing**

## Menggabungkan Data Tempat Wisata dengan Data Rating
Tujuannya, agar dapat lebih mudah melihat rating pengguna terhadap suatu tempat wisata.
"""

all_wisata = pd.concat([wisata,rating[['Rating','Review']]], axis=1)
all_wisata

"""# **4. Persiapan Data** ***(Data Preparation)***

## 4.1 Menghapus kolom yang tidak diperlukan
Dari pratinjau diatas, dapat dilihat bahwa kolom `Unnamed: 0` dari awal sudah ada dan kolom ini tidak berhubungan sama projek ini, maka perlu dihapus dengan teknik `drop`.
"""

all_wisata_clean = all_wisata.drop(columns = ['Unnamed: 0'])
all_wisata_clean.head()

"""## 4.2 Menangani Missing Value"""

# Mengecek missing value pada dataframe all_wisata_clean
all_wisata_clean.isnull().sum()

"""## 4.3 Menyamakan Kategori Tempat Wisata
Sebelum masuk tahap akhir (pemodelan), lakukan penyamaan nama kategori tempat wisata. Kadang, tempat wisata yang sama memiliki kategori yang berbeda. Jika dibiarkan, hal ini bisa menyebabkan bias pada data.

Pertama, cek ulang data setelah proses cleaning pada tahap sebelumnya. Buat variabel baru bernama `fix_wisata` untuk menyimpan dataframe.
"""

fix_wisata = all_wisata_clean
fix_wisata

"""Selanjutnya, cek kolom `Category` (kategori tempat wisata) yang unik"""

fix_wisata['Category '].unique()

"""Perhatikanlah, di antara semua kategori tempat wisata pada data, ada kategori yang menjadi 2 (duplikat), yaitu kategori tempat wisata bernama `Air Terjun` dan `Museum`. Jika dilihat dengan seksama, yang membedakan kategori tersebut adalah terdapat spasi di akhir katanya.
Hal-hal seperti ini kadang dapat ditemukan pada data. Penyebabnya bisa beragam, misalnya, kesalahan input data. Jika menemukan data seperti ini, hal yang perlu dilakukan adalah mengeksplorasi datanya lebih lanjut dan melakukan analisis. 

Dari proses analisis, kita akan memahami perbedaan penamaan ini terjadi pada data mana saja dan apa yang bisa kita lakukan untuk mengatasinya. Tentu solusi untuk permasalahan seperti ini akan berbeda tergantung kasusnya. Untuk kasus pada proyek ini, kita akan memilih salah satu penamaan kategori saja untuk digunakan pada data dan mengganti nama kategorinya menjadi tanpa spasi.
"""

# Mengecek kategori tempat wisata Air Terjun (tanpa spasi)
fix_wisata[fix_wisata['Category '] == 'Air Terjun']

# Mengecek kategori tempat wisata Air Terjun (dengan spasi)
fix_wisata[fix_wisata['Category '] == 'Air Terjun ']

"""Dalam sistem rekomendasi ini yang kita kembangkan, penting untuk memastikan satu tempat wisata mewakili satu kategori tempat wisata. Tujuannya supaya tidak terjadi dobel atau rangkap kategori dalam satu tempat wisata. Sehingga, sistem dapat merekomendasikan tempat wisata berdasarkan kategori tempat wisatanya."""

fix_wisata = fix_wisata.replace('Gunung ', 'Gunung')
fix_wisata = fix_wisata.replace('Pantai ', 'Pantai')
fix_wisata = fix_wisata.replace(['Air Terjun ','Air Terjun'], 'Air_Terjun')
fix_wisata = fix_wisata.replace('Taman Hiburan ', 'Taman_Hiburan')
fix_wisata = fix_wisata.replace('Museum ', 'Museum')
fix_wisata['Category '].unique()

"""Sekarang, semua kategori tempat wisata telah berubah menjadi tanpa spasi. Untuk kategori tempat wisata yang lebih dari satu kata, dipisah dengan karakter `underscore` (_). Hal ini dilakukan agar memudahkan saat pemodelan.

## 4.4 Tahap Persiapan
"""

# Membuat variabel preparation yang berisi dataframe fix_wisata
preparation = fix_wisata
preparation

"""Selanjutnya, mengkonversi data series menjadi list. Dalam hal ini, gunakan fungsi `tolist()` dari library numpy."""

# Mengonversi data series ‘Category’ menjadi dalam bentuk list
wisata_category = preparation['Category '].tolist()
 
# Mengonversi data series ‘Name’ menjadi dalam bentuk list
wisata_name = preparation['Name '].tolist()
 
# Mengonversi data series ‘City’ menjadi dalam bentuk list
wisata_city = preparation['City'].tolist()
 
print(len(wisata_category))
print(len(wisata_name))
print(len(wisata_city))

"""Tahap berikutnya, membuat dictionary untuk menentukan pasangan key-value pada data `wisata_category`, `wisata_name`, dan `wisata_city` yang telah disiapkan sebelumnya."""

# Membuat dictionary untuk data ‘wisata_category’, ‘wisata_name’, dan ‘wisata_city’
wisata_new = pd.DataFrame({
    'Category': wisata_category,
    'wisata_name': wisata_name,
    'City': wisata_city
})
wisata_new

"""# **5. Model Development dengan Content Based Filtering**

Sebelumnya, lakukan pengecekan data kembali dan assign dataframe dari tahap Preparation ke dalam variabel data
"""

data = wisata_new
data.sample(5)

"""## 5.1 TF-IDF Vectorizer
Pada tahap ini akan membangun sistem rekomendasi sederhana berdasarkan kategori tempat wisata, dengan menggunakan fungsi `tfidfvectorizer()` dari library `sklearn`.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
 
# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()
 
# Melakukan perhitungan idf pada data kategory
tf.fit(data['Category']) 
 
# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names()

"""Selanjutnya, lakukan fit dan transformasi ke dalam bentuk matriks. """

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(data['Category']) 
 
# Melihat ukuran matrix tfidf
tfidf_matrix.shape

"""Perhatikanlah, hasil matriks berukuran (100, 6). Nilai 100 merupakan ukuran data dan 22 merupakan matrik kategori tempat wisata. 

Untuk menghasilkan vektor tf-idf dalam bentuk matriks, gunakan fungsi `todense()`.
"""

# Mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()
tfidf_matrix.todense()

"""Selanjutnya, mari kita lihat matriks tf-idf untuk beberapa tempat wisata (wisata_name) dan kategori tempat wisata (Category)."""

# Membuat dataframe untuk melihat tf-idf matrix
# Kolom diisi dengan kategori tempat wisata
# Baris diisi dengan nama tempat wisata
 
pd.DataFrame(
    tfidf_matrix.todense(), 
    columns=tf.get_feature_names(),
    index=data.wisata_name
).sample(6, axis=1).sample(10, axis=0)

"""Output matriks tf-idf di atas menunjukkan tempat wisata *Kawi* memiliki kategori Gunung. Hal ini terlihat dari nilai matriks 1.0 pada kategori gunung. Selanjutnya, tempat wisata *Coban Rondo* termasuk dalam kategori air terjun. Sedangkan, tempat wisata *Trowulan* termasuk dalam kategori museum. Demikian seterusnya. 

Sampai di sini, kita telah berhasil mengidentifikasi representasi fitur penting dari setiap kategori tempat wisata dengan fungsi `tfidfvectorizer`. Kita juga telah menghasilkan matriks yang menunjukkan korelasi antara kategori tempat wisata dengan tempat wisata. Selanjutnya, kita akan menghitung derajat kesamaan antara satu tempat wisata dengan tempat wisata lainnya untuk menghasilkan kandidat tempat wisata yang akan direkomendasikan.

## 5.2 Cosine Similarity
Pada tahap sebelumnya, telah dilakukan identifikasi korelasi antara tempat wisata dengan kategorinya. Sekarang, lakukan perhitungan derajat kesamaan (*similarity degree*) antar tempat wisata dengan teknik `cosine similarity`, dengan menggunakan fungsi `cosine_similarity` dari library `sklearn`.
"""

from sklearn.metrics.pairwise import cosine_similarity
 
# Menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix) 
cosine_sim

"""Tahap ini merupakan tahap menghitung cosine similarity dataframe tfidf_matrix yang sudah diperoleh pada tahapan sebelumnya. Kode di atas menghasilkan keluaran berupa matriks kesamaan (similarity) dalam bentuk array. 

Selanjutnya, mari kita lihat matriks kesamaan setiap tempat wisata dengan menampilkan nama tempat wisata dalam 5 sampel kolom (axis = 1) dan 10 sampel baris (axis=0).
"""

# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa nama tempat wisata
cosine_sim_df = pd.DataFrame(cosine_sim, index=data['wisata_name'], columns=data['wisata_name'])
print('Shape:', cosine_sim_df.shape)
 
# Melihat similarity matrix pada setiap tempat wisata
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""Dengan cosine similarity, kita berhasil mengidentifikasi kesamaan antara satu tempat wisata dengan tempat wisata lainnya. Shape (100, 100) merupakan ukuran matriks similarity dari data yang kita miliki. Berdasarkan data yang ada, matriks di atas sebenarnya berukuran 100 tempat wisata x 100 tempat wisata (masing-masing dalam sumbu X dan Y). Artinya, kita mengidentifikasi tingkat kesamaan pada 100 nama tempat wisata. Tapi tentu kita tidak bisa menampilkan semuanya. Oleh karena itu, kita hanya memilih 10 tempat wisata pada baris vertikal dan 5 tempat wisata pada sumbu horizontal seperti pada output di atas. 

Angka 1.0 mengindikasikan bahwa tempat wisata pada kolom X (horizontal) memiliki kesamaan dengan tempat wisata pada baris Y (vertikal). Sebagai contoh, tempat wisata *Siring Kemuning* teridentifikasi sama (similar) dengan tempat wisata *Coro*, *Tambakrejo,* dan *Papuma*. Contoh lain, tempat wisata *Coban Rondo* teridentifikasi mirip dengan tempat wisata *Toroan* dan *Sumber Pitu Pujon*.

# **6. Mendapatkan Rekomendasi Tempat Wisata**

## 6.1 Testing Model
Sebelumnya, kita telah memiliki data similarity (kesamaan) antar tempat wisata. Sekarang saatnya menghasilkan sejumlah tempat wisata yang akan direkomendasikan kepada pengguna. Untuk lebih memahami bagaimana cara kerjanya, lihatlah kembali matriks similarity pada tahap sebelumnya. Sebagai gambaran, simak contoh berikut.

Pengguna X pernah mengunjungi tempat wisata *Coban Rondo*. Kemudian, saat pengguna tersebut berencana untuk mengunjungi tempat wisata lain, sistem akan merekomendasikan tempat wisata *Toroan* atau *Sumber Pitu Pujon*. Nah, rekomendasi kedua tempat wisata ini berdasarkan kesamaan yang dihitung dengan cosine similarity pada tahap sebelumnya. 

Di sini, kita membuat fungsi wisata_recommendations dengan beberapa parameter sebagai berikut:

- **nama_wisata** : Nama tempat wisata (index kemiripan dataframe).
- **similarity_data** : Dataframe mengenai similarity yang telah kita definisikan sebelumnya.
- **items** : Nama dan fitur yang digunakan untuk mendefinisikan kemiripan, dalam hal ini adalah ‘wisata_name’ dan ‘Category’.
- **k** : Banyak rekomendasi yang ingin diberikan.

Keluaran dari sistem rekomendasi ini adalah berupa **top-N recommendation**. Oleh karena itu, kita akan memberikan sejumlah rekomendasi tempat wisata pada pengguna yang diatur dalam parameter k.
"""

def wisata_recommendations(nama_wisata, similarity_data=cosine_sim_df, items=data[['wisata_name', 'Category']], k=5):
    """
    Rekomendasi Tempat Wisata berdasarkan kemiripan dataframe
 
    Parameter:
    ---
    nama_wisata : tipe data string (str)
                Nama Tempat Wisata (index kemiripan dataframe)
    similarity_data : tipe data pd.DataFrame (object)
                      Kesamaan dataframe, simetrik, dengan tempat wisata sebagai 
                      indeks dan kolom
    items : tipe data pd.DataFrame (object)
            Mengandung kedua nama dan fitur lainnya yang digunakan untuk mendefinisikan kemiripan
    k : tipe data integer (int)
        Banyaknya jumlah rekomendasi yang diberikan
    ---
 
 
    Pada index ini, kita mengambil k dengan nilai similarity terbesar 
    pada index matrix yang diberikan (i).
    """
 
 
    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan    
    # Dataframe diubah menjadi numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,nama_wisata].to_numpy().argpartition(
        range(-1, -k, -1))
    
    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    
    # Drop nama_wisata agar nama tempat wisata yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(nama_wisata, errors='ignore')
 
    return pd.DataFrame(closest).merge(items).head(k)

"""Perhatikanlah, dengan menggunakan argpartition, kita mengambil sejumlah nilai k tertinggi dari similarity data (dalam kasus ini: dataframe **cosine_sim_df**). Kemudian, kita mengambil data dari bobot (tingkat kesamaan) tertinggi ke terendah. Data ini dimasukkan ke dalam variabel closest. Berikutnya, kita perlu menghapus nama_wisata yang yang dicari agar tidak muncul dalam daftar rekomendasi. 

Dalam kasus ini, nanti kita akan mencari tempat wisata yang mirip dengan Gunung Bromo, sehingga kita perlu drop nama_wisata Bromo agar tidak muncul dalam daftar rekomendais yang diberikan nanti.  
"""

data[data.wisata_name.eq('Bromo')]

"""Perhatikanlah, Bromo masuk dalam kategori tempat wisata Gunung. Tentu kita berharap rekomendasi yang diberikan adalah tempat wisata dengan kategori yang mirip. 

Nah, sekarang, dapatkan tempat wisata recommendation dengan memanggil fungsi yang telah kita definisikan sebelumnya
"""

# Mendapatkan rekomendasi tempat wisata yang mirip dengan Bromo
wisata_recommendations('Bromo')

"""Sistem memberikan rekomendasi 5 nama tempat wisata dengan kategori Gunung.

## 6.2 Evaluasi Model
Selanjutnya kita akan evaluasi model kita menggunakan metrik **Precision**, dengan cara melihat kesamaan antara kategori tempat wisata yang pernah dikunjungi pengguna dengan kategori tempat wisata yang direkomendasikan sistem.

Dari hasil rekomendasi sistem sebelumnya, diketahui bahwa Bromo termasuk ke dalam kategori Gunung. Dan dari 5 item yang direkomendasikan, semuanya memiliki kategori Gunung (similar).
"""

recommended_film = 5 # jumlah item yang direkomendasikan sistem
relevant_film = 5 # jumlah item rekomendasi yang kategorinya relevan (similar) dengan yang pernah dikunjungi pengguna
precision = relevant_film/recommended_film
print(precision)

""" Dari hasil ini artinya, precision sistem kita sebesar 5/5 atau 100%."""