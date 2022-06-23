# PANDUAN MEMPERBARUI APLIKASI/PROYEK

Panduan ini digunakan untuk memperbarui database yang ada di proyek ini.Pastikan format HDF5 untuk data harian mengikuti [panduan pembuatan database](./create_database.md).

1. Taruh database berupa HDF5 (`.h5`) di dalam folder `./data/rainfall/`.
2. Jalankan _script_ `run_completeness.py` untuk membuat database kelengkapan data seluruh database yang tersedia di `./data/rainfall/`.
3. Jalankan _script_ `run_metadata.py` untuk membuat metadata keseluruhan data hujan (`./data/rainfall/`) dan data kelengkapan (`./data/completeness/`).
4. Commit git, dan jangan lupa _push_ ke heroku untuk pembaruan data. Jika dijalankan lokal, bisa langsung menjalankan `app.py`. 
