# Modul Verifikasi SheerID ChatGPT Militer

## Gambaran Umum

Dokumen ini merangkum bagaimana alur verifikasi SheerID untuk program militer ChatGPT bekerja. Validasi militer sedikit berbeda dibanding verifikasi guru/mahasiswa karena SheerID meminta status militer diverifikasi terlebih dahulu sebelum formulir identitas pribadi dapat dikirim.

## Alur Permintaan

### Langkah 1 – Tetapkan status militer (`collectMilitaryStatus`)

Langkah ini menandai status calon pengguna sebagai veteran/aktif sehingga SheerID menampilkan formulir yang sesuai.

**Permintaan**

- **URL**: `https://services.sheerid.com/rest/v2/verification/{verificationId}/step/collectMilitaryStatus`
- **Metode**: `POST`
- **Body**:

```json
{
    "status": "VETERAN"
}
```

**Respons Contoh**

```json
{
    "verificationId": "{verification_id}",
    "currentStep": "collectInactiveMilitaryPersonalInfo",
    "errorIds": [],
    "segment": "military",
    "subSegment": "veteran",
    "locale": "en-US",
    "country": null,
    "created": 1766539517800,
    "updated": 1766540141435,
    "submissionUrl": "https://services.sheerid.com/rest/v2/verification/{verification_id}/step/collectInactiveMilitaryPersonalInfo",
    "instantMatchAttempts": 0
}
```

**Catatan**

- `submissionUrl` adalah endpoint yang harus dipakai pada langkah berikutnya.
- `currentStep` akan berubah menjadi `collectInactiveMilitaryPersonalInfo` jika status berhasil diperbarui.

---

### Langkah 2 – Kirimkan informasi pribadi (`collectInactiveMilitaryPersonalInfo`)

Setelah menerima `submissionUrl`, kirim data profil lengkap melalui endpoint tersebut.

**Permintaan**

- **URL**: nilai `submissionUrl` dari langkah 1 (biasanya `https://services.sheerid.com/rest/v2/verification/{verificationId}/step/collectInactiveMilitaryPersonalInfo`)
- **Metode**: `POST`
- **Body**:

```json
{
    "firstName": "name",
    "lastName": "name",
    "birthDate": "1939-12-01",
    "email": "your mail",
    "phoneNumber": "",
    "organization": {
        "id": 4070,
        "name": "Army"
    },
    "dischargeDate": "2025-05-29",
    "locale": "en-US",
    "country": "US",
    "metadata": {
        "marketConsentValue": false,
        "refererUrl": "",
        "verificationId": "",
        "flags": "{\"doc-upload-considerations\":\"default\",\"doc-upload-may24\":\"default\",\"doc-upload-redesign-use-legacy-message-keys\":false,\"docUpload-assertion-checklist\":\"default\",\"include-cvec-field-france-student\":\"not-labeled-optional\",\"org-search-overlay\":\"default\",\"org-selected-display\":\"default\"}",
        "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the <a target=\"_blank\" rel=\"noopener noreferrer\" class=\"sid-privacy-policy sid-link\" href=\"https://openai.com/policies/privacy-policy/\">privacy policy</a> of the business from which I am seeking a discount, and I understand that my personal information will be shared with SheerID as a processor/third-party service provider in order for SheerID to confirm my eligibility for a special offer. Contact OpenAI Support for further assistance at support@openai.com"
    }
}
```

**Penjelasan Field**

- `firstName` / `lastName`: nama depan dan belakang.
- `birthDate` / `dischargeDate`: format `YYYY-MM-DD`.
- `organization`: pilih ID cabang militer yang relevan (lihat tabel di bawah).
- `email` dan `phoneNumber`: kontak pengguna (nomor telepon dapat dikosongkan).
- `metadata`: tetap gunakan nilai yang diminta SheerID, khususnya `submissionOptIn`.

---

## Referensi Organisasi Militer

| ID       | Cabang        |
|----------|---------------|
| `4070`   | Army          |
| `4073`   | Air Force     |
| `4072`   | Navy          |
| `4071`   | Marine Corps  |
| `4074`   | Coast Guard   |
| `4544268`| Space Force   |

Semua entri di atas bertipe `MILITARY` dan memiliki koordinat default yang sama pada data SheerID.

---

## Tips Implementasi

1. Simpan `submissionUrl` dari respons pertama dan gunakan kembali agar tidak perlu menebak endpoint berikutnya.
2. Pastikan nilai `organization.id` dan `organization.name` saling cocok.
3. Validasi format tanggal sebelum mengirim sehingga SheerID tidak menolak request.
4. Metadata harus tetap dikirim apa adanya; hanya ubah nilai yang benar-benar diperlukan seperti `refererUrl` atau `verificationId`.

---

## Checklist Validasi

- [ ] Panggilan `collectMilitaryStatus` berhasil dan mengembalikan `submissionUrl`.
- [ ] Data `collectInactiveMilitaryPersonalInfo` dikirim menggunakan `submissionUrl` terbaru.
- [ ] ID organisasi sesuai cabang yang diinginkan.
- [ ] Semua tanggal menggunakan format `YYYY-MM-DD`.
- [ ] Metadata menyertakan kalimat `submissionOptIn` yang dikonfirmasi.
- [ ] Jalur verifikasi baru (`/verify6` atau serupa) menyimpan respons SheerID agar dapat diteruskan ke pengguna bot.
