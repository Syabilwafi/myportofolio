# Portofolio Pribadi - Tugas Individu PBP

Nama : Syabil Wafi Ahdi

NPM : 2506657371

Kelas : PBP B

## Setup

---

### Prerequisites
- Python 3.12+
- Git
- Any IDE

### Installation
- Clone repository ini pada terminal
```bash
git clone https://github.com/Syabilwafi/myportofolio.git
```

- Buat environment virtual 
```bash
python -m venv env
```

- Aktifkan environment virtual
```bash
env/bin/activate 
```

- Install dependencies pada `requirements.txt` 
```bash
pip install -r requirements.txt
```

- Jalankan Django's check dan migrasi database
```bash
python manage.py check
python manage.py migrate
```

- Jalankan server development
```bash
python manage.py runserver
```
## Tugas 1

---

1. Saya menggunakan elemen semantik seperti `<nav>`, `<header>`, `<main>`, dan `<section>` untuk memisahkan bagian-bagian utama halaman web. Dengan elemen semantik ini, 
penggunaan CSS dapat lebih mudah diterapkan karena bagian bagian tersebut sudah terpisah.
2. Tantangan yang saya hadapi dalam membuat website yang *responsive* adalah bagaimana cara mengatur tata letak elemen elemen tanpa mengubah konsep awal yang sudah di design 
pada tampilan desktop. Dengan menggunakan media query, saya dapat mengatur tata letak elemen elemen dengan lebih fleksibel dan responsif.
3. Untuk mengembangkan lebih lanjut website *static* ini, saya ingin menambakan fitur fitur interaktif pada elemen yng sudah ada agar dapat terlihat lebih menarik.

### Penggunaan AI
Saya menggunakan AI untuk membuat tampilan CRT untuk overlay pada keseluruhan website. Konsep dan design yang digunakan untuk mendesign website ini murni dari kreativitas yang sudah saya
kembangkan sejak lama.

Untuk memastikan website dapat terlihat baik di seluruh device, saya menggunakan AI untuk mengatur media query pada layar lebih kecil.

## Tugas 2

---

1. Saat membuka halaman baru pada website portofolio, request HTTP dari browser akan pertama kali masuk ke `urls.py` project yang berperan sebagai pintu masuk utama yang 
mengrouting ke file url spesifik milik portofolio. Setelah itu akan diarahkan ke `urls.py` aplikasi yang memetakan URL lebih spesifik fungsi atau kelas View yang sesuai. 
Setelah itu, fungsi pada `views.py` akan dipanggil dan mentukan data apa yang dibutuhkan dari model untuk dikirim ke template. Pada `models.py` merepresentasikan struktur 
dari basis data yang sudah dibuat. Model bertugas mengambil, menyimpan, dan memanipulasi data. Setelah itu, olev View akan dikirimkan ke template berupa file `.html` yang 
nantinya akan di render data data yang sudah diambil ke dalam tampilan.

2. Menyimpan data portofolio langsung di dalam template dapat membuat kode menjadi kaku. Saat terdapat data yang perlu diubah atau ditambah, tampilan tidak dapat secara 
otomatis berubah karena data yang ditampilkan langsung ditulis di template. Oleh karena itu, data portofolio lebih baik disimpan di dalam model dan dikirimkan ke template 
melalui fungsi View. Hal ini memungkinkan tampilan website dapat secara otomatis berubah sesuai dengan perubahan data tanpa perlu mengubah kode template secara manual.

3. `makemigrations` menyiapkan catatan perubahannya dalam bentuk file Python, sedangkan `migrate` menerapkan rancangan tersebut ke database fisik. Contoh yang saya gunakan 
adalah perubahan struktur tabel pada model `Project` dengan menghilangkan kolom `thumbnail`.

### Penggunaan AI
AI digunakan untuk memudahkan implementasi dari desain sistem ke dalam kode HTML dengan memberikan tampilan UI dari Figma ke dalam Gemini. Kode yang dihasilkan oleh AI sudah 
di review, verifikasi, dan disesuaikan dengan kebutuhan proyek. Pilihan struktur kode, skema database, dan logika bisnis sudah saya definisikan di awal pengembangan bagian ini.

AI lebih digunakan untuk mengubah tampilan `blog.html` menjadi responsive dengan menambahkan query selector untuk menyesuaikan tampilan pada berbagai ukuran layar dari 
kode yang sudah ditulis sendiri.

## Tugas 3

---

1. Menggunakan `ModelForm` pada Django jauh lebih efisien dibandingkan membuat form HTML secara manual karena `ModelForm` secara otomatis menghasilkan field form berdasarkan struktur kolom yang sudah kita definisikan pada model. Selain menerapkan prinsip *Don't Repeat Yourself* (DRY), `ModelForm` juga secara otomatis menangani validasi data, seperti mengecek tipe data, batas karakter, hingga aturan *unique*, serta memudahkan proses menyimpan data ke basis data hanya dengan memanggil method `.save()`. Sementara itu, penambahan `{% csrf_token %}` diwajibkan untuk melindungi aplikasi dari serangan *Cross-Site Request Forgery* (CSRF). Tag ini menghasilkan token rahasia unik pada form yang akan diverifikasi oleh Django saat form dikirimkan, sehingga *request* tanpa token yang valid akan langsung ditolak demi keamanan data pengguna.

2. JSON lebih disukai daripada XML dalam pengembangan aplikasi web modern karena ukurannya yang jauh lebih ringkas tanpa keberadaan tag penutup, sehingga menghemat *bandwidth* dan mempercepat proses transfer data di jaringan. Selain itu, karena JSON merupakan struktur data *native* JavaScript, proses *parsing* data di tingkat *browser* maupun kerangka kerja frontend modern dapat berjalan jauh lebih cepat tanpa perlu melalui pemrosesan DOM XML yang rumit. Format berbasis *key-value pair* pada JSON juga jauh lebih rapi dan mudah dibaca oleh pengembang dibandingkan dengan hierarki dokumen XML yang dipenuhi oleh tag-tag pembuka dan penutup.

3. Alur pengembalian data portofolio dalam bentuk JSON dimulai saat klien mengirimkan *request* HTTP GET ke URL *endpoint* yang dituju. Fungsi *view* pada `views.py` kemudian akan memproses *request* tersebut dengan mengambil data dari basis data menggunakan QuerySet. Data QuerySet yang didapat lalu diubah bentuknya melalui proses serialisasi menggunakan fungsi serialisator Django. Setelah data terkonversi ke dalam format JSON, data tersebut dibungkus ke dalam `HttpResponse` dengan *content-type* `application/json` untuk dikirimkan kembali ke klien. Proses serialisasi ini wajib dilakukan karena objek model Django merupakan objek Python internal yang tidak bisa dikirimkan langsung melalui protokol HTTP maupun dipahami oleh bahasa pemograman lain di sisi frontend, sehingga serialisasi bertugas menerjemahkan objek Python yang kompleks menjadi format teks terstruktur yang siap dikonsumsi oleh sistem luar.
