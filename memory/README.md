# Memory — BES Pilot Belleği

Her kullanıcının BES verisi `memory/users/{kısa_ad}/` altında saklanır. Bu klasör skill'in "kalıcı belleği"dir.

## Yapı

```
memory/
├── README.md (bu dosya)
├── _template/             ← yeni kullanıcı için kopyala (Şema sürümü 2)
│   ├── profile.md             # doğum tarihi + override geçmişi + sözleşme detayları
│   ├── current_basket.md      # talep tarihi pay fiyatları + önceki sepet getirisi
│   └── history/
│       └── _example.md        # gerçek getiri + benchmark karşılaştırması
└── users/
    └── {kısa_ad}/        ← her kullanıcı için ayrı klasör
        ├── profile.md
        ├── current_basket.md
        └── history/
            ├── {YYYY-MM}.md     # aylık revize
            ├── {YYYY-MM}.md
            ├── {YYYY}-yillik.md # yıl sonu özet (compound + tema dağılımı)
            └── ...
```

## Şema sürümü 2 (Mayıs 2026)

Sürüm 1'den farkları:
- **Doğum tarihi** tutuluyor, "yaş" değil — yaş otomatik hesaplanır, eşik geçişleri (40, 55) zamanında yakalanır
- **Talep tarihi pay fiyatları** her sepete kayıtlı — gerçekleşmiş getiri hesabı için kritik
- **Önceki sepetin gerçekleşmiş getirisi** her revizede güncellenir (BIST 100 + TÜFE benchmark)
- **Override geçmişi** profile.md'de — yaş eşik öneri kullanıcı kararları kaydedilir, tekrar tekrar sorulmaz
- **Sözleşme açılış tarihi** — fon gider iadesi (BES Yönetmeliği Madde 22/A) zamanlaması için
- **Yıllık takvim** — Genelge 2026/1 ile 12 hak/yıl, Ocak 1'de sıfırlama

Sürüm 1 → 2 geçişi: kullanıcıyla doğum tarihi sor (mevcut yaş kayıttan silinmeli), eski sepetler için pay fiyatları geriye doğru toplanamayabilir — bir sonraki revizeden itibaren gerçek getiri ölçümü başlar.

## Kullanıcı kısa adı

`{ad}-{soyad ilk harfi}` formatı tercih edilir, küçük harf, Türkçe karakter yok:
- `{Ad} {Soyad}` → `{ad}-{s}` (örn: ad-soyad → `ad-s`)
- Aynı isimde başka kullanıcı varsa numaralandır: `{ad-s}`, `{ad-s}-2`

## Yeni kullanıcı oluşturma

```bash
cp -r memory/_template memory/users/{yeni-kısa-ad}
```

Sonra `profile.md`'yi `references/onboarding.md`'deki 5 soruya göre doldur.

## Çoklu kullanıcı

Skill aynı bilgisayarda birden fazla kişiye hizmet edebilir (örn. eş, çocuk, ebeveyn). Her birinin kendi klasörü olur. Skill açıldığında "kim için çalışıyoruz?" sorusu sor (eğer birden fazla user dosyası varsa).

## Privacy

Bu klasör finansal bilgi içerir. **GitHub'a pushlama!** `.gitignore` zaten `memory/users/` dizinini hariç tutuyor.

`memory/_template/` ise public — sadece şablon, gerçek veri yok.
