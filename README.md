# :beginner: Communications Middleware

Aplikasi yang dibuat menggunakan protokol XMPP dengan menggunakan gaya arsitektur microservice. Terdiri dari tiga komponen yaitu:
1. Tracker
2. Manager
3. Relay

Tersedia juga aplikasi untuk mencoba middlewarenya, yang tersimpan dalam folder user. Cara aplikasi user berkomunikasi dengan middleware menggunakan stanza, yang terbagi menjadi tiga yaitu, message, presence, dan iq (info/query).

 ## :zap: Cara Penggunaan

**Setup**
1. Pastikan server sudah terinstall Python 3.8+.
2. Buka file `.env` dalam folder manager, relay, atau user, dan ubah konfigurasi IP dari server tempat tracker dijalankan.
3. Install library python yang diperlukan dengan menjalankan `pip install -r requirements.txt`.
4. Jalankan program sesuai dengan perintah dibawah.

**Folder User**
1. Pastikan komputer sudah terinstall Python 3.8+.
2. Jalankan program sesuai dengan perintah dibawah.

**Folder User Bot Joker Node.JS**
1. Pastikan komputer sudah terinstall Node.JS V16.8.0
2. Masuk ke folder "user bot joker Node JS"
3. Install package yang diperlukan dengan menjalankan `npm install`
4. Jalankan program sesuai dengan perintah dibawah.

## :package: Perintah

**Urutan Menyalakan Komponen**
- Jalankan komponen tracker
- Jalankan komponen manager
- Jalankan komponen relay

**Tracker**
- Masuk ke folder tracker, kemudian
- `Python tracker.py` untuk menjalankan komponen tracker

**Manager**
- Masuk ke folder manager, kemudian
- `Python main.py` untuk menjalankan komponen manager

**Relay**
- Masuk ke folder relay, kemudian
- `Python main.py` untuk menjalankan komponen relay

**Background Services**

- Background service akan menggunakan systemd, untuk kalian yang belum tahu cara penggunaannya, bisa dilihat disini ["cara menggunakan systemd pada server"](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267).
- Gunakan `tracker.service` di folder services untuk menjalankan tracker.
- Gunakan `manager.service` di folder services untuk menjalankan manager.
- Gunakan `relay.service` di folder services untuk menjalankan relay.

**User**
- Masuk ke folder user, kemudian
- `Python main.py` untuk menjalankan aplikasi user
- Input pilihan 1 atau 2, untuk registrasi atau login, lakukan dengan benar
- Aplikasi sudah terhubung dengan middleware

**User Bot Joker Node.JS**
- Masuk ke folder "user bot joke node js"
- `node client.js` untuk menjalankan aplikasi user bot joker
- Aplikasi sudah terhubung dengan middleware

<!--## :notebook: File Dokumentasi

- [Entity Relationship Diagram (ERD)](https://dbdiagram.io/d/62622c031072ae0b6acb52f0)
- [Class Diagram](docs/class_diagram_simplified.png)
- [Postman API Documentation](https://documenter.getpostman.com/view/11687432/2s8YerLWtg)
- [Routing Table](docs/routing_table.png) -->

## :wrench: Dokumentasi Stanza Message
<details>
<summary>Mengirimkan Message Melalui Middleware</summary>
- **Komponen Target**: Relay
- **Payload/Stanza**:
```json
{
    "stanza": "message",
    "from": "user_initiator",
    "to": "user_target",
    "lang": "id",
    "body": "value_of_message",
    "time_send": "timestamp_now"
}
```
<!-- - **Response** -->
</details>

## :wrench: Dokumentasi Stanza Presence
<details>
<summary>Inisialisasi Presence</summary>
- **Komponen Target**: Manager
- **Payload/Stanza**:
```json
{
    "stanza": "presence"
}
```
<!-- - **Response** -->
</details>
<details>
<summary>Mendapatkan Directed Presence</summary>
- **Komponen Target**: Manager
- **Payload/Stanza**:
```json
{
    "stanza": "presence",
    "to": "user_target"
}
```
<!-- - **Response** -->
</details>
<details>
<summary>Update Bio pada Middleware</summary>
- **Komponen Target**: Manager
- **Payload/Stanza**:
```json
{
    "stanza": "presence",
    "bio": "value_of_bio"
}
```
<!-- - **Response** -->
</details>
<details>
<summary>Logout dari Sistem</summary>
- **Komponen Target**: Manager
- **Payload/Stanza**:
```json
{
    "stanza": "presence",
    "type": "unavailable"
}
```
<!-- - **Response** -->
</details>

## :wrench: Dokumentasi Stanza IQ (Info/Query)
<details>
<summary>Menambahkan Roster (Contact)</summary>
- **Komponen Target**: Manager
- **Payload/Stanza**:
```json
{
    "stanza": "iq",
    "namespace": "roster",
    "from": "user_initiator",
    "type": "set",
    "query": {
        "item": {
            "jid": "user_target",
            "name": "alias_name_for_user_target",
            "subscription": "to"
        }
    }
}
```
<!-- - **Response** -->
</details>
<details>
<summary>Mendapatkan Daftar Roster (Contact)</summary>
- **Komponen Target**: Manager
- **Payload/Stanza**:
```json
{
    "stanza": "iq",
    "namespace": "roster",
    "from": "user_initiator",
    "type": "get",
    "query": {"items": null}
}
```
<!-- - **Response** -->
</details>
<details>
<summary>Memperbarui Nickname dari Roster (Contact)</summary>
- **Komponen Target**: Manager
- **Payload/Stanza**:
```json
{
    "stanza": "iq",
    "namespace": "roster",
    "from": "user_initiator",
    "type": "set",
    "query": {
        "item": {
            "jid": "user_target",
            "name": "new_nickname_user_target",
            "subscription": "to"
        }
    }
}
```
<!-- - **Response** -->
</details>
<details>
<summary>Menghapus Roster (Contact)</summary>
- **Komponen Target**: Manager
- **Payload/Stanza**:
```json
{
    "stanza": "iq", 
    "namespace": "roster", 
    "from": "user_initiator", 
    "type": "set", 
    "query": {
        "item": {
            "jid": "user_target", 
            "name": "name_user_target", 
            "subscription": "to"
            }
        }, 
    "subscription": "remove"
}
```
<!-- - **Response** -->
</details>

## :file_folder: Struktur Direktori & File

    .
    ├── docs                                                            # Sebagai tempat dokumentasi file seperti skripsi, referensi, manual guide, dll
    |
    ├── services                                                        # Kumpulan konfigurasi background service yang dipakai di systemd/systemctl
    |
    ├── programs                                                        # Kumpulan folder komponen dan utilitasnya
    |   |
    │   ├── manager                                                     # Folder untuk komponen manager
    |   |   |
    │   |   ├── database                                                # Folder tentang basis datanya komponen manager
    |   |   |   |
    |   |   |   ├── dummy                                               # Menyimpan data dalam bentuk dictionary
    |   |   |   |   └── init_data.py                                    # Menyimpan daftar socket komponen terkoneksi pada manager
    |   |   |   |   
    |   |   |   └── sqlite                                              # Menyimpan data dalam bentuk SQLite
    |   |   |       ├── init_db.py                                      # File berisi object database SQLite manager
    |   |   |       ├── component.py                                    # Untuk mengelola database komponen relay yang terkoneksi
    |   |   |       ├── roster.py                                       # Untuk mengelola database daftar roster dari user
    |   |   |       └── user.py                                         # Untuk mengelola database user
    |   |   |   
    │   |   ├── manager_utils                                           # Berisi utilitas/fungsionalitas komponen manager
    |   |   |   ├── import_abs_path.py                                  # Kemampuan untuk meng-import utilitas umum yang berada pada folder utils
    |   |   |   ├── get_time.py                                         # Kemampuan untuk mengelola timestamp
    |   |   |   ├── packet.py                                           # Kemampuan untuk menerima packet pesan dari komponen lainnya
    |   |   |   ├── auth.py                                             # Kemampuan untuk melakukan autentikasi kepada user
    |   |   |   ├── presence.py                                         # Kemampuan untuk mengelola presence user
    |   |   |   └── roster.py                                           # Kemampuan untuk mengelola roster user
    |   |   |
    │   |   ├── main.py                                                 # File utama untuk menjalankan manager
    │   |   ├── .env                                                    # Environment komponen manager
    │   |   └── socketClient.py                                         # Kemampuan manager untuk menjadi klien
    |   |
    │   ├── relay                                                       # Folder untuk komponen relay
    |   |   |
    │   |   ├── database                                                # Folder tentang basis datanya komponen relay
    |   |   |   |   
    |   |   |   ├── sqlite                                              # Menyimpan data dalam bentuk SQLite
    |   |   |   |   ├── init_db.py                                      # File berisi object database SQLite relay
    |   |   |   |   └── messages.py                                     # Untuk mengelola database pesan
    |   |   |   | 
    |   |   |   └── init_data.py                                        # Menyimpan data kebutuhan dasar relay
    |   |   |   
    │   |   ├── relay_utils                                             # Berisi utilitas/fungsionalitas komponen relay
    |   |   |   ├── import_abs_path.py                                  # Kemampuan untuk meng-import utilitas umum yang berada pada folder utils
    |   |   |   ├── message.py                                          # Kemampuan untuk mengelola stanza message
    |   |   |   └── packet.py                                           # Kemampuan untuk menerima packet pesan dari komponen lainnya
    |   |   |
    │   |   ├── main.py                                                 # File utama untuk menjalankan relay
    │   |   ├── .env                                                    # Environment komponen relay
    │   |   └── socketClient.py                                         # Kemampuan relay untuk menjadi klien
<!--|   |
    │   ├── tracker                                                     # Folder untuk kodingan crawling
    |   |   |
    │   |   ├── database                                                # Folder tentang basis datanya komponen manager
    |   |   |   |   
    |   |   |   ├── component.py                                        # Menyimpan data dalam bentuk SQLite
    |   |   |   └── init_db.py                                          # Menyimpan daftar socket komponen terkoneksi pada manager
    |   |   |   
    │   |   ├── tracker_utils                                           # Berisi utilitas/fungsionalitas komponen manager
    |   |   |   ├── get_time.py                                         # Kemampuan untuk mengelola timestamp
    |   |   |   ├── import_abs_path.py                                  # Kemampuan untuk meng-import utilitas umum yang berada pada folder utils
    |   |   |   └── packet.py                                           # Kemampuan untuk menerima packet pesan dari komponen lainnya
    |   |   |
    │   |   └── tracker.py                                              # Fungsi-fungsi pendukung crawling
    |   |
    │   ├── user                                                        # Folder untuk kodingan crawling
    |   |   |
    │   |   ├── database                                                # Folder tentang basis datanya komponen manager
    |   |   |   |   
    |   |   |   ├── dummy                                               # Menyimpan data dalam bentuk SQLite
    |   |   |   |   └── init.py                                         # File berisi object database SQLite manager
    |   |   |   | 
    |   |   |   └── init.py                                             # Menyimpan daftar socket komponen terkoneksi pada manager
    |   |   |   
    │   |   ├── user_utils                                              # Berisi utilitas/fungsionalitas komponen manager
    |   |   |   ├── communicate_with_another_component.py               # Kemampuan untuk meng-import utilitas umum yang berada pada folder utils
    |   |   |   ├── get_time.py                                         # Kemampuan untuk mengelola timestamp
    |   |   |   ├── message.py                                          # Kemampuan untuk meng-import utilitas umum yang berada pada folder utils
    |   |   |   ├── packet.py                                           # Kemampuan untuk menerima packet pesan dari komponen lainnya
    |   |   |   ├── presence.py                                         # Kemampuan untuk meng-import utilitas umum yang berada pada folder utils
    |   |   |   └── roster.py                                           # Kemampuan untuk meng-import utilitas umum yang berada pada folder utils
    |   |   |
    │   |   ├── main.py                                                 # File utama untuk menjalankan manager
    │   |   ├── .env                                                    # Environment komponen manager
    │   |   └── socketClient.py                                         # Fungsi-fungsi pendukung crawling
    |   |
    │   ├── user bot joker node js                                      # Folder untuk kodingan document ranking
    │   |   ├── client.js                                               # File utama untuk menjalankan manager
    │   |   ├── kumpulan_quotes.js                                      # File utama untuk menjalankan manager
    │   |   ├── package.json                                            # File utama untuk menjalankan manager
    │   |   └── package-lock.json                                       # Implementasi dari TF-IDF
    |   |
    │   └── utils                                                       # Folder untuk kodingan crawling
    |       |
    │       ├── kelas                                                   # Folder tentang basis datanya komponen manager
    |       |   |   
    |       |   └── socketServer.py                                     # Menyimpan data dalam bentuk SQLite
    |       |
    │       └── utility                                                 # Folder tentang basis datanya komponen manager
    |           |   
    |           ├── get_time.py                                         # Kemampuan untuk menerima packet pesan dari komponen lainnya
    |           └── testing_import_from_another_folder_in_top_root.py   # Menyimpan data dalam bentuk SQLite
    | -->
    ├── README.md                                                       # File README
    └── requirements.txt                                                # Berisi list library yang diperlukan

## :page_facing_up: Referensi

- [Cara set up background service di systemd](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267)
- [XMPP Core](https://datatracker.ietf.org/doc/html/rfc6120)
- [XMPP Instant Messaging and Presence](https://datatracker.ietf.org/doc/html/rfc6121)
- [The Definitive Guide XMPP](https://kr-labs.com.ua/books/Oreilly-XMPP-The-Definitive-Guide-May-2009.pdf)
