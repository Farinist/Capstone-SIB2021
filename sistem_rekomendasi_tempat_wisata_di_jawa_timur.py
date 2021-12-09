# -*- coding: utf-8 -*-
"""Sistem Rekomendasi Tempat Wisata di Jawa Timur.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AcaNTqp7z4laUxb0b4V5ACE8MGdb6WT6

# **Sistem Rekomendasi**: Rekomendasi Tempat Wisata di Jawa Timur dengan Content-based Filtering
---
##### Oleh : Samuel Partogi Pakpahan dan Farin Istighfarizky
##### Capstone Project - Studi Independen Bersertifikat x Dicoding

# **Pendahuluan**

Pada proyek ini akan dibuat sistem rekomendasi tempat wisata di Jawa Timur menggunakan *content-based filtering*. Untuk memudahkan navigasi gunakan menu *Table of Contents* di kanan atas Google Colaboratory.

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

wisata.head()

rating.head()

rating.describe()

"""# **3. Data Preprocessing**

## Menggabungkan Data Tempat Wisata dengan Data Rating
"""



"""# **4. Persiapan Data** ***(Data Preparation)*** **dan Visualisasi Data**"""

