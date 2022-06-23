# RAINFALL STATION EXPLORER (fiako-stations)

Rainfall Stations Explorer (fiako-stations) merupakan portal untuk memperoleh data hujan dari pos/stasiun hujan yang tersedia di database. Aplikasi web ini juga dapat digunakan untuk menentukan stasiun mana saja yang terdekat dengan lokasi titik tinjauan (lokasi proyek, outlet, dll). Output aplikasi ini adalah data hujan harian dalam bentuk _CSV (Comma Seperated Value)_. Tujuan aplikasi ini hanya untuk mensentralisasikan dataset dan pemerolehannya dengan mudah, untuk analisis selanjutnya akan dikembangkan di aplikasi yang terpisah. 

Situs resmi aplikasi ini adalah [demo-stations.dev.fiako.engineering](http://demo-stations.dev.fiako.engineering).

## TATA CARA PENGGUNAAN / TUTORIAL

Tutorial bisa di lihat pada dokumen [TUTORIAL.md](./docs/TUTORIAL.md).

## FITUR

Berikut daftar fitur aplikasi ini:

- Melihat database yang tersedia dan yang dimiliki.
- Melihat stasiun terdekat dari titik tinjauan.
- Melihat secara sekilas mengenai kelengkapan data yang tersedia di database.
- Memudahkan untuk mengeksplorasi data dan mengambil keputusan dalam ketentuan penggunaan data dari stasiun mana saja yang akan digunakan.
- Mensentralisasikan data yang telah digunakan untuk kepentingan proyek selanjutnya atau _preliminary analysis/research_.
- Mempersingkat pekerjaan untuk pemerolehan data dari kumpulan data yang telah dimiliki dari proyek sebelumnya. 

## KEKURANGAN

Berikut daftar kekurangan atau _known issues_ aplikasi ini:

- Penentuan data stasiun hujan masih berdasarkan radius dari titik tinjauan. Lebih tepatnya harusnya menggunakan DAS dari outlet/titik tinjauan. 
- Proses pembuatan database harus dilakukan secara _case-by-case_. 

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
