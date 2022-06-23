# PROJECT STRUCTURE

## Tree

Berikut struktur folder di proyek ini:
```
[RAINFALL-STATION-EXPLORER / fiako-rse]
|   .gitignore
|   app.py
|   app_config.yml
|   environment-dev.yml
|   Procfile
|   pyconfig.py
|   pyfigure.py
|   pyfunc.py
|   pylayout.py
|   pylayoutfunc.py
|   pytemplate.py
|   README.md
|   requirements.txt
|   run_completeness.py
|   run_metadata.py
|
+---.vscode
|       settings.json
|
+---data
|   +---completeness
|   |       ... (generated from run_completeness.py)
|   |
|   +---metadata
|   |       ... (generated from run_metadata.py)
|   |
|   \---rainfall
|           data_hujan_data_A.h5
|           data_hujan_data_B.h5
|           data_hujan_data_C.h5
|
\---docs
        TUTORIAL.md
        ...
```

Berikut file/folder yang perlu diperhatikan:

## Root Folder (`.`)

- `app.py`: merupakan file utama aplikasi proyek. Semua fungsi selain _callback_ diatur/ditulis diluar file ini agar memudahkan pengembangan lanjutan. File ini bergantung juga ke beberapa file antara lain:

    - `pyconfig.py`: file ini hanya bertugas membuat _object_ yang berisikan konfigurasi aplikasi yang tersedia di berkas `app_config.yml`.
    - `pyfigure.py`: file ini berisikan fungsi untuk membuat grafik yang digunakan dalam proyek dengan hasil akhir (_return_) berupa `plotly.graph_objects.Figure`.
    - `pyfunc.py`: file ini berisikan fungsi yang digunakan untuk memproses pengolahan data. File ini digunakan sebagai tempat untuk menyimpan fungsi yang keluarannya selain berupa `plotly.graph_objects` atau komponen dash.
    - `pylayout.py`: file ini berisikan objek yang digunakan di dalam `app.Layout(...)` untuk fungsi yang akan digunakan didalam layout akan disimpan di file `pylayoutfunc.py`.
    - `pylayoutfunc.py`: sama halnya dengan `pyfigure.py`, file ini berisikan untuk membuat layout (berupa komponen dash (html/dcc/dbc)) yang digunakan di `pylayout.py`.
    - `pytemplate.py`: file ini berisikan objek untuk template yang digunakan grafik di `plotly`.

- `run_completeness.py`: Script ini digunakan untuk memproduksi/menghasilkan database untuk kelengkapan data (completeness). hasil script ini disimpan di `./data/completeness/` dengan masing-masing nama file yang tersedia di `./data/rainfall/`.
- `run_metadata.py`: Script ini menggabungkan metadata yang tersedia di folder `./data/completeness/` dan `./data/rainfall/`. Script ini dijalankan setelah `run_completeness.py`. 
- `Procfile`: file yang dibutuhkan untuk pengaturan di heroku.

## Database / Dataset (`./data/`)

Terdapat tiga folder di dalam folder database:
- `rainfall/`: merupakan folder utama menyimpan data hujan **harian** dalam bentuk HDF5. Untuk format lihat dokumentasi dalam pembuatan database.
- `completeness/`: merupakan folder yang berupa hasil `run_completeness.py` untuk memproduksikan dataset kelengkapan data (completeness).
- `metadata/`: merupakan folder yang berisikan metadata hasil kompilasi dari seluruh data yang tersedia di `rainfall/` dan `completeness/`

## Dokumentasi (`./docs/`)

Dokumentasi berupa:
- [TUTORIAL](./TUTORIAL.md): Cara penggunaan aplikasi.
- [Project Structure](project_structure.md): Struktur Proyek.
- [Panduan Memperbarui Proyek](update_project.md): Panduan Memperbarui Proyek/Aplikasi.
- [Panduan Pembuatan Database](create_database.md): Panduan membuat database HDF5 (`.h5`).
