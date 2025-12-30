Tautan YouTube sedikit berbeda, misalnya:
https://offers.sheerid.com/youtube/student/?yrdup=https%3A%2F%2Fwww.youtube.com%2F%3Fsld%3Dxxxxxxxxxxxxxxxytpid=premium&ytsku=premium&yrsp=https%3A%2F%2Fwww.youtube.com%2Fpremium%2FstudxxxxxxxxxxxxQQBRgO&euid=230493635&locale=en-US&oid=AI97cxxxxxxxxxxxxxxxxxxxxxNT06Nb5kDzo384b8cAu

Tautan tersebut tidak langsung menampilkan `programId` dan `verificationId`, jadi Anda harus mengambilnya dari log jaringan.

1. Buka DevTools browser → tab Network.
2. Cari permintaan ke `https://services.sheerid.com/rest/v2/verification/`.
3. Ambil `programId` dari payload dan `verificationId` dari respons.
4. Rakit tautan manual:

```
https://services.sheerid.com/verify/xxx/?verificationId=yyyy
```

`xxx` adalah `programId`, `yyyy` adalah `verificationId`.
