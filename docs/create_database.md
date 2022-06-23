# PANDUAN PEMBUATAN DATABASE

Pembuatan database untuk aplikasi ini diharuskan menggunakan __python__ dan __pandas__. Meski HDF5 bisa dibuat dengan ketentuan tersendiri dan aplikasi lain, aplikasi ini hanya dapat membaca tabel yang dibuat oleh `pandas`.


## Struktur HDF5

Pada setiap file HDF5 harus memiliki dua grup yaitu `metadata` dan `stations` dengan fungsi sebagai berikut:

- `/metadata/`: berisikan informasi metadata yang digunakan sebagai acuan pemerolehan `key` setiap stasiun, informasi file, dan informasi metadata original yang diperoleh dari pemerolehan file mentah data.
- `/stations/`: berisikan `key` setiap stasiun yang berisi tabel `pandas`.

### Metadata (`/metadata/`)

Pada metadata setidaknya harus memiliki `key` berikut:

- `/metadata/file`: berisikan informasi terkait file seperti nama file, sumber, dlsbnya. Key ini __harus berupa `pandas.Series`__. Objek `pd.Series` dibuat menggunakan _dictionary_ dengan _key_ wajib:

    - `filename`: (`str`) nama file.
    - `title`: (`str`) judul file. Informasi ini digunakan untuk nama dataset.
    - (opsional) `[key]`: `[value]`. bisa ditambahkan informasi lainnya, tapi yang wajib ada adalah key `filename` dan `title`. 

Contoh pembuatan metadata_file
```python
dict_file = {'filename': 'nama_file.h5', 'title': 'Dataset Pribadi', 'source':'Personal'}
metadata_file = pd.Series(dict_file)
```

- `/metadata/stations`: berisikan informasi daftar stasiun di dalam database. Key ini __harus berupa `pandas.DataFrame`__. `pandas.DataFrame` ini wajib memiliki nama kolom sebagai berikut:

    - `id` (index): id stasiun. ID ini mohon dimodifikasi dari original agar menghindari kesamaan id dengan stasiun lain dengan dataset yang berbeda. ID ini juga harus bersifat unik untuk setiap stasiun. ID harus tidak mengandung karakter selain angka dan abjad. Gunakan regex `[^a-zA-Z0-9]+` untuk menyesuaikan ID Stasiun.
    - `station_name`: (`str`) nama stasiun.
    - `latitude`: (`float`) lintang derajat/latitude.
    - `longitude`: (`float`) bujur derajat/longitude.
    - `key`: (`str`) lokasi _key_ data stasiun. Disarankan key stations diberi prefix `sta`. Contoh: Untuk ID `hk_82931`, maka key berupa `/stations/stahk_82931`. 

- `/metadata/original`: berisikan informasi mengenai stasiun yang diperoleh langsung/asli dari eksternal. Key ini __harus berupa `pandas.DataFrame`__. Tidak ada ketentuan untuk key ini karena tidak dibaca di aplikasi. Key ini harap dilampirkan untuk memudahkan memperoleh informasi terkait stasiun. Disarankan menggunakan ID stasiun yang sama dengan `/metadata/stations/` sebagai index. 

### Stations (`/stations/`)

Jumlah key didalam grup ini ditentukan dengan jumlah stasiun yang ada di `/metadata/`. Grup ini tidak diakses langsung dari aplikasi, akan tetapi agar memudahkan penamaan dan penyeragaman dataset, digunakan grup `/stations/` sebagai grup data hujan harian setiap stasiun. Penamaan key __harus__ sesuai dengan kolom `key` di `/metadata/stations`. Direkomendasikan menamai key setiap stasiun dengan format `sta{id}`. Contoh: untuk stasiun ber-id `hk_125423` memiliki key `stahk_125423` atau lengkapnya `/stations/stahk_125423`. 