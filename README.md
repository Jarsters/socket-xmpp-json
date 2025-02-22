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

- **Response**: Null

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
- **Response**: Null
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
- **Response**:
```json
{
  "stanza": "presence",
  "from": "user_target",
  "username": "user_target",
  "bio": "bio_user_target",
  "online": "status_user_target",
  "updated_at": "last_update_user_target",
  "directed_entity": true,
  "to": "user_initiator"
}
```
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
- **Response**: 
```json
{
  "stanza": "presence",
  "from": "user_initiator",
  "username": "user_initiator",
  "bio": "new_bio_user_initiator",
  "online": "status_user_initiator",
  "updated_at": "last_update_user_initiator",
  "to": "user"
}
```
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
- **Response**:
```json
{
  "stanza": "presence",
  "from": "user_initiator",
  "type": "unavailable",
  "to": "user"
}
```
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
- **Response 1**:
``` json
{
  "stanza": "presence",
  "from": "user_target",
  "to": "user_initiator",
  "type": "subscribed",
  "item": {
    "jid": "user_target",
    "name": "alias_name_for_user_target",
    "subscription": "to"
  }
}
```
- **Response 2**:
``` json
{
  "stanza": "presence",
  "from": "user_target",
  "username": "user_target",
  "bio": "bio_user_target",
  "online": "status_user_target",
  "updated_at": "last_updated_user_target",
  "to": "user_initiator"
}
```
- **Response 3**:
``` json
{
  "stanza": "iq",
  "namespace": "roster",
  "type": "result",
  "to": "user_initiator"
}
```
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
- **Response**:
``` json
{
  "stanza": "iq",
  "namespace": "roster",
  "type": "result",
  "query": {
    "items": [
      {
        "jid": "roster_1",
        "name": "alias_name_roster_1",
        "subscription": "type_subscribe between them"
      }
    ]
  },
  "to": "user_initiator"
}
```
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
            "name": "alias_name_for_user_target",
            "subscription": "to"
        }
    }
}
```
- **Response 1**:
``` json
{
  "stanza": "presence",
  "from": "user_target",
  "to": "user_initiator",
  "type": "subscribed",
  "item": {
    "jid": "user_target",
    "name": "alias_new_name_for_user_target",
    "subscription": "to"
  }
}
```
- **Response 2**:
``` json
{
  "stanza": "presence",
  "from": "user_target",
  "username": "user_target",
  "bio": "bio_user_target",
  "online": "status_user_target",
  "updated_at": "last_updated_user_target",
  "to": "user_initiator"
}
```
- **Response 3**:
``` json
{
  "stanza": "iq",
  "namespace": "roster",
  "type": "result",
  "to": "user_initiator"
}
```
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
- **Response 1**:
```json
{
  "stanza": "presence",
  "from": "user_target",
  "to": "user_initiator",
  "type": "unsubscribed"
}
```
- **Response 2**:
```json
{
  "stanza": "iq",
  "namespace": "roster",
  "type": "result",
  "subscription": "remove",
  "to": "user_initiator"
}
```
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
    |   |
    │   ├── tracker                                                     # Folder untuk komponen tracker
    |   |   |
    │   |   ├── database                                                # Folder tentang basis datanya komponen tracker
    |   |   |   |   
    |   |   |   ├── component.py                                        # Menyimpan data komponen dalam bentuk SQLite
    |   |   |   └── init_db.py                                          # File berisi object database SQLite tracker
    |   |   |   
    │   |   ├── tracker_utils                                           # Berisi utilitas/fungsionalitas komponen tracker
    |   |   |   ├── get_time.py                                         # Kemampuan untuk mengelola timestamp
    |   |   |   ├── import_abs_path.py                                  # Kemampuan untuk meng-import utilitas umum yang berada pada folder utils
    |   |   |   └── packet.py                                           # Kemampuan untuk menerima packet pesan dari komponen lainnya
    |   |   |
    │   |   └── tracker.py                                              # File utama untuk menjalankan tracker
    |   |
    │   ├── user                                                        # Folder untuk komponen aplikasi user penguji
    |   |   |
    │   |   ├── database                                                # Folder tentang basis datanya komponen user
    |   |   |   └── init.py                                             # Menyimpan data kebutuhan dasar aplikasi user
    |   |   |   
    │   |   ├── user_utils                                              # Berisi utilitas/fungsionalitas komponen aplikasi user
    |   |   |   ├── communicate_with_another_component.py               # Kemampuan untuk menerima pesan dari komponen relay atau manager, dan melakukan pengolahan pesan
    |   |   |   ├── get_time.py                                         # Kemampuan untuk mengelola timestamp
    |   |   |   ├── message.py                                          # Kemampuan untuk melakukan pengiriman stanza message kepada komponen relay
    |   |   |   ├── packet.py                                           # Kemampuan untuk menerima packet pesan dari komponen lainnya
    |   |   |   ├── presence.py                                         # Kemampuan untuk pengelolaan kegiatan yang berkaitan stanza presence
    |   |   |   └── roster.py                                           # Kemampuan untuk pengelolaan kegiatan yang berkaitan stanza iq, namespace "roster"
    |   |   |
    │   |   ├── main.py                                                 # File utama untuk menjalankan aplikasi user
    │   |   ├── .env                                                    # Environment komponen manager
    │   |   └── socketClient.py                                         # Kemampuan aplikasi user untuk menjadi klien
    |   |
    │   ├── user bot joker node js                                      # Folder untuk komponen aplikasi user bot
    │   |   ├── client.js                                               # File utama untuk menjalankan aplikasi user bot
    │   |   ├── kumpulan_quotes.js                                      # File kumpulan quotes yang akan digunakan pada aplikasi user bot
    │   |   ├── package.json                                            # File JSON yang berisi catatan deskripsi aplikasi
    │   |   └── package-lock.json                                       # File JSON yang berisi catatan package yang dipakai pada aplikasi user bot
    |   |
    │   └── utils                                                       # Folder untuk fungsionalitas umum yang dapat digunakan oleh komponen tracker, manager, dan relay.
    |       |
    │       ├── kelas                                                   # Folder fungsionalitas dalam bentuk Class
    |       |   |   
    |       |   └── socketServer.py                                     # Kemampuan untuk menjadikan komponen pengguna menjadi server
    |       |
    │       └── utility                                                 # Folder fungsionalitas dalam bentuk fungsi biasa
    |           |   
    |           └── get_time.py                                         # Kemampuan untuk menjadikan komponen mampu mengolah timestamp\
    |
    ├── README.md                                                       # File README
    └── requirements.txt                                                # Berisi list library yang diperlukan untuk program python

## :page_facing_up: Referensi

- [Cara set up background service di systemd](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267)
- [XMPP Core](https://datatracker.ietf.org/doc/html/rfc6120)
- [XMPP Instant Messaging and Presence](https://datatracker.ietf.org/doc/html/rfc6121)
- [The Definitive Guide XMPP](https://kr-labs.com.ua/books/Oreilly-XMPP-The-Definitive-Guide-May-2009.pdf)
