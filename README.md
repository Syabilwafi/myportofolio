# Portofolio Pribadi - Tugas Individu PBP

Website portofolio pribadi berbasis Django yang menampilkan profil, pengalaman, proyek, dan blog. Data proyek dan pengalaman dikelola melalui API Django REST Framework; frontend memakai `fetch()` untuk pencarian dan perubahan data tanpa reload.

Nama : Syabil Wafi Ahdi

NPM : 2506657371

Kelas : PBP B

## Setup

---

### Prerequisites
- Python 3.12 atau lebih baru
- Git
- IDE pilihan

### Installation
- Clone repository ini pada terminal
```bash
git clone https://github.com/Syabilwafi/myportofolio.git
```

- Buat environment virtual 
```bash
python -m venv env
```

- Aktifkan environment virtual (Linux/macOS)
```bash
source env/bin/activate
```

- Aktifkan environment virtual (Windows PowerShell)
```powershell
env\Scripts\Activate.ps1
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

### API

Semua endpoint portofolio tersedia di bawah `/api/v1/` dan menggunakan session authentication.

| Resource | Endpoint | Method |
| --- | --- | --- |
| Experiences | `/api/v1/experiences/` | `GET`, `POST` |
| Experience detail | `/api/v1/experiences/<uuid>/` | `GET`, `PUT`, `PATCH`, `DELETE` |
| Projects | `/api/v1/projects/` | `GET`, `POST` |
| Project detail | `/api/v1/projects/<uuid>/` | `GET`, `PUT`, `PATCH`, `DELETE` |
| Project star | `/api/v1/projects/<uuid>/star/` | `POST` (toggle) |

List endpoint menerima parameter pencarian `?q=...`. Membuat data memerlukan pemilik portofolio; Editor dapat memperbarui data; pengunjung hanya dapat membaca. Star memerlukan pengguna yang sudah login. Request yang mengubah data melalui session perlu menyertakan token CSRF.

Jalankan pemeriksaan dan test suite dengan:

```bash
python manage.py check
python manage.py test
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


## Tugas 5

---

1. Debouncing adalah sebuah teknik yang digunakan untuk membatasi seberapa sering suatu fungsi dapat dieksekusi. Sebuah event terjadi berulang kali dalam interval waktu yang sangat singkat, debouncing memastikan bahwa fungsi handler baru akan dijalankan setelah pengguna berhenti memicu event tersebut selama rentang delay tertentu.

2. Panggilan `fetch()` digunakan untuk melakukan permintaan jaringan secara *asynchronus*. Eksekusi `fetch()` tidak langsung mengembalikan data hasil respons dari server, melainkan mengembalikan sebuah objek `Promise`. Penggunaan kata kunci await di depan fungsi `fetch()` berfungsi untuk menghentikan sementara eksekusi baris kode selanjutnya di dalam fungsi async, sampai objek `Promise` tersebut diselesaikan atau ditolak. Melalui mekanisme ini, alur kode asinkron dapat ditulis dan dibaca dengan gaya penyusunan yang runtut layaknya kode *synchronus*, sehingga mempermudah pengelolaan data respons. Jika kita tidak menyertakan await saat memanggil fetch(), alur eksekusi JavaScript akan langsung melompat ke baris kode berikutnya tanpa menunggu permintaan jaringan selesai diproses oleh server.

3. Cross-Site Scripting (XSS) adalah salah satu jenis serangan keamanan web di mana penyerang berhasil menyisipkan kode berbahaya ke dalam konten atau basis data aplikasi web. Ketika pengguna lain mengunjungi atau memuat halaman yang mengandung skrip berbahaya tersebut, browser pengguna akan mengeksekusi skrip tersebut secara otomatis. Kerentanan terhadap serangan XSS sangat dipengaruhi oleh bagaimana cara aplikasi menyajikan atau merender data ke dalam struktur HTML DOM.

## Tugas 6

---

1. REST (Representational State Transfer) adalah gaya arsitektur API berbasis sumber daya yang menggunakan semantik HTTP secara konsisten. Mengembalikan JSON saja belum cukup untuk membuat API menjadi RESTful. API juga perlu menggunakan URI resource yang jelas, method HTTP sesuai operasi, dan status respons yang tepat. `PUT` mengirim representasi lengkap resource untuk diperbarui, sedangkan `PATCH` mengirim perubahan sebagian. Pada proyek ini aksi star memiliki endpoint `POST` tersendiri karena operasinya adalah toggle, bukan pembaruan field resource melalui `PATCH`.

2. Serializer pada Django REST Framework (DRF) berperan sebagai penerjemah dua arah antara objek kompleks Django (seperti Model atau QuerySet) dengan format data terstruktur seperti JSON (*serialization*), serta memvalidasi masukan data JSON pengguna sebelum disimpan ke basis data (*deserialization*). Keuntungannya dibandingkan merakit dictionary secara manual menggunakan `JsonResponse` adalah tersedianya validasi data otomatis, penerapan prinsip *Don't Repeat Yourself* (DRY) yang membuat kode lebih ringkas, kemudahan integrasi skema tabel melalui `ModelSerializer`, serta penanganan otomatis untuk relasi data yang kompleks.

3. Autentikasi (*authentication*) adalah proses verifikasi **identitas** pengguna (memastikan siapa pengguna tersebut, contohnya proses *login*), sedangkan otorisasi (*authorization*) adalah proses verifikasi **hak akses** pengguna (memastikan apa saja tindakan yang boleh dilakukan oleh pengguna tersebut). Hak akses wajib diperiksa menggunakan *permission class* di sisi server karena pengamanan di sisi frontend (seperti menyembunyikan tombol di template HTML) sangat mudah dimanipulasi oleh pengguna melalui *developer tools* atau pengiriman HTTP request langsung (seperti cURL atau Postman) ke endpoint API.

4. Permintaan yang mengubah data tetap memerlukan token CSRF saat memakai `SessionAuthentication` karena metode ini mengandalkan cookie sesi (`sessionid`) yang otomatis dikirim browser ke domain target. Tanpa pemeriksaan CSRF, situs pihak ketiga dapat mencoba memanfaatkan sesi pengguna untuk mengirim aksi tanpa persetujuannya. Pengujian `force_authenticate` tidak membuktikan perlindungan CSRF karena metode itu melewati pemeriksaan session dan CSRF. Karena itu, proyek juga menguji request session menggunakan `APIClient(enforce_csrf_checks=True)` dan `.login()`.

### Penggunaan AI

AI digunakan sebagai alat bantu untuk mengembangkan dan memeriksa fitur API portofolio. Bantuan yang digunakan mencakup implementasi endpoint daftar, detail, dan star untuk proyek serta pengalaman; penerapan autentikasi sesi, izin berdasarkan peran, validasi serializer, dan pencarian melalui parameter query. AI juga membantu menghubungkan halaman Projects dan Experiences ke API menggunakan `fetch()` tanpa memuat ulang halaman, termasuk penanganan CSRF, pesan kesalahan melalui toast, serta rendering teks secara aman.

AI turut membantu menyusun dan memperbaiki pengujian API untuk izin tiap peran, validasi, star, dan CSRF, serta menyesuaikan tata letak responsif dan tampilan kolom pencarian agar sesuai dengan tema website. Perubahan yang dihasilkan disesuaikan dengan struktur proyek dan diuji menggunakan test suite Django.

Untuk sesi pengerjaan ini, AI yang digunakan adalah OpenAI Codex di IDE. Strategi prompt yang digunakan adalah memberikan rubrik atau kebutuhan fitur secara eksplisit, meminta pemeriksaan file yang sudah ada, lalu mengarahkan perbaikan berdasarkan temuan, hasil test, dan screenshot UI. Bagian yang dibantu mencakup endpoint API, permission, integrasi JavaScript, test, dokumentasi reflektif, dan CSS responsif. Saya memeriksa hasil terhadap struktur aplikasi, memperbaiki test yang memakai URL lama, menyesuaikan penjelasan `PUT`/`PATCH` dengan perilaku endpoint, dan menambahkan test untuk skenario yang terlewat.

Ringkasan log prompting:

- Meminta implementasi permission portfolio owner/Editor/read-only dan endpoint pengalaman dengan serializer.
- Meminta API function-based dengan session authentication, pencarian `q`, status HTTP yang sesuai, dan registrasi di `/api/v1/`.
- Meminta integrasi halaman Projects dan Experiences melalui `fetch()`, termasuk CSRF, toast, dan operasi tanpa reload.
- Meminta pengujian peran, validasi, star, CSRF, lalu audit bug dan perbaikan responsivitas berdasarkan screenshot.

AI dapat salah memahami konteks atau menghasilkan perubahan yang belum sesuai dengan implementasi aktual. Karena itu, saran AI tidak dianggap benar tanpa pemeriksaan; perubahan API diverifikasi dengan test suite, sedangkan tampilan tetap perlu diperiksa di browser pada ukuran layar yang berbeda. Ringkasan interaksi AI pada tugas ini: (1) implementasi dan integrasi API pengalaman/proyek, (2) penambahan test role, validasi, star, dan CSRF, (3) audit dan perbaikan test serta dokumentasi, dan (4) iterasi tampilan search berdasarkan screenshot. Prompt lengkap tersedia pada riwayat percakapan Codex untuk sesi pengerjaan ini.

