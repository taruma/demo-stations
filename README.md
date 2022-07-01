# RAINFALL STATION EXPLORER (fiako-stations)

![image](./_readme/fiakodev-demo-stations-thumbnail.png)

**Rainfall Stations Explorer** atau `fiako-stations` adalah aplikasi web atau dashboard yang dapat digunakan untuk mengeksplorasi data hujan harian yang tersedia di database. Dari aplikasi ini dapat memperoleh informasi kelengkapan data dan akusisi data hujan harian dengan mudah dan cepat.

## FITUR APLIKASI

Berikut daftar fitur aplikasi ini:

<div align="center">
<h3>Memudahkan eksplorasi data hujan harian yang dimiliki</h3>
<img src="./_readme/fkstations-ft-01-loop.gif" width="250px">
<br>
<span align="center">Navigasi dan Interaksi Peta</span>
</div>

<div align="center">
<h3>Mengetahui informasi stasiun terdekat terhadap titik lokasi tinjauan</h3>
<img src="./_readme/fkstations-ft-2-1-loop.gif" width="auto">
<br>
<span align="center">Navigasi dan Interaksi Peta</span>
</div>

### Mengetahui informasi stasiun terdekat terhadap titik lokasi tinjauan.

![image](./_readme/fkstations-ft-2-1-loop.gif)

![image](./_readme/fkstations-ft-2-2-loop.gif)

### Melihat secara sekilas kelengkapan data dengan heatmap.

### Memilih stasiun dan periode yang akan digunakan di analisis.

### Visualisasi & Download data hujan harian dengan periode yang telah dipilih.



## KEKURANGAN

Berikut daftar kekurangan atau _known issues_ aplikasi ini:

- Penentuan data stasiun hujan masih berdasarkan radius dari titik tinjauan. Lebih tepatnya harusnya menggunakan DAS dari outlet/titik tinjauan. 
- Proses pembuatan database harus dilakukan secara _case-by-case_. 

## TATA CARA PENGGUNAAN / TUTORIAL

Tutorial bisa di lihat pada dokumen [TUTORIAL.md](./docs/TUTORIAL.md).

## DOKUMENTASI

Berikut daftar dokumentasi yang tersedia terkait proyek ini:

- Dokumen Struktur Proyek. [Link](./docs/project_structure.md).
- Dokumen Panduan Membuat Database. [Link](./docs/create_database.md).
- Dokumen Memperbarui situs/proyek. [Link](./docs/update_project.md).
- Dokumen Tutorial/Penggunaan aplikasi. [Link](./docs/TUTORIAL.md).

## LISENSI

[MIT LICENSE](./LICENSE)

Copyright (c) 2022 PT. FIAKO ENJINIRING INDONESIA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

----

Dataset untuk demo merupakan data acak. Lokasi stasiun hujan merupakan titik sembarang. Nama stasiun hujan dibangkitkan menggunakan [Name Generator](https://www.name-generator.org.uk/).
