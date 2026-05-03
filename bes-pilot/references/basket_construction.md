# Sepet Kurma — Risk Profili × Piyasa Verisi → Final Sepet

Bu adım profil + piyasa özetini alıp **uygulanabilir bir sepet** üretir.

## Girdiler

1. Kullanıcının risk profili: defansif / dengeli / agresif (`risk_profile.md`'den)
2. Bu ayın piyasa özeti (`fund_research.md`'den)
3. Kullanıcının BES kurumu ve BEFAS açık mı (`profile.md` ve provider adapter'dan)
4. Geçen ay sepeti (`current_basket.md`'den) — stabilite için
5. Kalan değişiklik hakkı (eSube'den, `Kalan Hakkınız: N` text'inden)
6. **Önceki sepetin gerçekleşmiş getirisi** (`current_basket.md`'deki "Önceki sepetin gerçekleşmiş getirisi" bölümünden)

## Algoritma

### 1. Temel iskeleti yükle

`risk_profile.md`'den profile karşılık gelen allokasyon yüzdelerini al.

### 2. Konjonktürel tilt uygula

Mevcut piyasa özetine göre allokasyonu **±5-15%** kaydır:

| Durum | Tilt | Eşik gerekçesi |
|---|---|---|
| Belirgin tema lider (top 10'un 7+ fonu tek kategoride) | O kategoriye **+10%**, defansif kategorilerden -10% kes | %70 konsantrasyon = belirgin sinyal, gürültü değil |
| Trend doğrulanmış (hafta=ay yönü) | Tilt'i koru | Hafta-ay aynı → kalıcı, geçici dalga değil |
| Trend belirsiz (hafta ay'a aykırı) | Tilt yapma, iskelete sadık kal | Reversal sinyali var, momentum güvenilmez |
| Counter-momentum açık (en kötü kategori bir bandı altta) | O kategoriye **+5%** koy, mean-reversion bahsi | Asimetrik bahis: küçük pozisyon, dönerse büyük getiri |
| Makro şok var | Defansife **+10%** geçici geçiş (volatilite yüksek) | Belirsizlik yüksek, koruma maliyeti düşük |

> Tilt yüzdeleri (±5%, ±10%, ±15%) **çıplak gözlem ve alışılmış aktif yönetim büyüklükleri**. Klasik aktif yönetim "stratejik allokasyondan ±%5-10" sapma kabul edilebilir kabul edilir; daha büyük sapmalar "taktik aşırılık" sayılır. Defansif profilde tilt **±%5 ile sınırlı** çünkü defansif kullanıcının "ben sektör bahsi yapmam" tercihine saygı.

**Defansif profil için**: Konjonktürel tilt'i sınırla — max ±5%. Defansif kullanıcı sektör bahsi yapamaz.

### 3. Fon seçimi (kategori → spesifik kod)

Her kategori için:

a. **BEFAS açıksa**: Tüm Türkiye BES kurucularından son hafta+ay top performerlarını sırala, ilk 1-3'ünü seç
b. **BEFAS kapalıysa**: Sadece kullanıcının kendi kurumunun fon listesinden o kategorinin lideri

**Çoklu fon kuralı** (tek kategori içinde):
- Ağırlık < %15 → 1 fon yeter
- Ağırlık %15-30 → 2 fon (farklı kurucu)
- Ağırlık > %30 → 3 fon (3 farklı kurucu, yönetici risk diversifikasyonu)

> Çoklu fon eşikleri (%15, %30) **yönetici-bazlı tek nokta arıza** mantığına dayanır. Aynı kategoride tek bir fonun aniden zayıflaması (yönetici değişikliği, fon kapanması, gizli yapısal değişim) kullanıcıyı etkiler. %30+ ağırlıkta tek bir fon → ölçek riski. 3 fon (3 kurucu) bu riski dağıtır.

### 4. Stabilite cezası

Geçen ay sepetiyle karşılaştır:
- Aynı tema lider devam ediyor → mümkünse aynı fonları koru, sadece ağırlıkları ayarla
- Bir fon eklemek/çıkarmak ufak fayda sağlıyorsa (< %2 ek getiri beklentisi) **yapma** — fon değişiklik hakkını koru
- Eğer toplam değişiklik < %15'lik bir reshuffle ise **revize gerekli mi** sorgula. Pas geçmek değerli olabilir.

> %15 örtüşmeme eşiği = "değişiklik anlamlı bahse dönüştü mü" sorusu. Daha düşük örtüşmeme yıl içi 12 hakkın tükenme hızını artırır (Genelge 2026/1, Madde 8/Y). Yıl boyu agresif aktiflik = takvim yılının ortasında hak kalmaması = piyasa şoku anında müdahale edememek. Marjinal değişiklikleri eleyerek hak budgetini sona doğru rezerve etmek değerlidir.

### 5. Performans geri besleme (yeni adım)

`current_basket.md`'deki "Önceki sepetin gerçekleşmiş getirisi" bölümünü oku. Şunları sorgula:

- **Önceki sepet benchmark'tan (BIST 100) ne kadar saptı?**
  - Çok altıysa (-3% ve fazlası): Önceki kararın mantığını gözden geçir. Tema yanlış tahmin mi edildi? Kullanıcıya açık ol.
  - Üstüyse (+3% ve fazlası): Strateji çalışıyor — değişikliği konservatif tut, çalışan şeyi bozma.
- **Reel getiri pozitif mi?** TÜFE'yi yenebildi mi?
- **Geçtiğimiz aydaki gerekçe (history dosyası) bu sonuçla tutarlı mı?** "Teknoloji rallisi devam edecek" dediysen ve teknoloji düştüyse, bu ay teknoloji bahsini doğrulamak için ek kanıt iste.

Bu adım skill'in **kendini öğrenmesi**dir — mantık eskidikçe pas geçmez, vurguladığı tema yanlış çıkarsa söyler.

### 6. Kullanıcıya öneriyi sun

Her zaman bu formatı kullan:

```markdown
## Bu ayın sepeti — {YYYY-MM}

**Profil**: Dengeli (puan +1, son hesaplama 2026-04-01)
**Bu ayın teması**: Teknoloji rallisi devam (4. ay üst üste)
**Geçen aya göre değişiklik**: Düşük (%92 örtüşme), 1 fon değiştirildi

### Önceki ay performansı (geri besleme)
- Önceki sepet getirisi: %3.45 (33 gün)
- BIST 100 aynı aralık: %2.83
- TÜFE Nisan: %1.92
- **Reel getiri**: %+1.53 ✅ (TÜFE'yi yendi)
- **BIST'e karşı**: %+0.62 ✅ (benchmark üstü)

### Bu ayın önerisi
| # | Fon | Kurucu | Yeni Ağırlık | Geçen Ay | Δ |
|---|---|---|---|---|---|
| 1 | TVH — Teknoloji ŞTİ. Hisse | Agesa | 13% | 13% | = |
| 2 | TBJ — Teknoloji Hisse | THE | 13% | 13% | = |
| ... | | | | | |

**Toplam**: 100%
**Kullanılacak değişiklik hakkı**: 1 (kalan: 8/12)
**Bir sonraki revize**: 2026-06-01 (otomatik)
```

### 7. Yatırımcıya değişiklik gerekli mi karar ver

Eğer önerilen sepet ile mevcut sepet **%85+ örtüşüyorsa** kullanıcıya seçenek sun:

```
Bu ay belirgin değişiklik gerekmiyor. 2 seçenek:
A) Pas geç — fon değişiklik hakkını koru, sepet aynı kalsın (önerilir)
B) Marjinal tweak — 2-3 fon ağırlığı ufak değişti, uygulayalım
```

Eğer örtüşme **< %85** ise direkt revize öner ve eSube'ye geçeceğiz.

## Pratik örnekler

### Örnek 1: Dengeli profil, teknoloji teması

```
İskelet:
- Borçlanma 25%, Altın 10%, Hisse-pazar 20%, Hisse-tek 30%, Karma 10%, P.piyasa 5%

Tilt: +10% Hisse-tek (lider tema), -5% Altın, -5% Borçlanma

Final allokasyon:
- Borçlanma 20%, Altın 5%, Hisse-pazar 20%, Hisse-tek 40%, Karma 10%, P.piyasa 5%

Sadeleştirilmiş 8-fon sepet:
- TVH 13, TBJ 13, GCN 12, YZD 12, FFC 10, ENF 10 (sektör çeş.), VES 20, VGA 10
```

### Örnek 2: Agresif profil, teknoloji teması

```
İskelet:
- Hisse-tek 50%, Hisse-pazar 20%, Karma 10%, Borçlanma 10%, Altın 5%, Sektör-rotasyon 5%

Tilt: Tema zaten lehimize, +5% daha (hisse-tek 55%) ama 3+ kurucudan

Final fon dağılımı (8 fon):
- TVH 13%, TBJ 13%, BZY 13%, GCN 12%, YZD 12%, FFC 12% (6 teknoloji ≈ %75)
- ENF 13% (enerji rotasyonu)
- TSZ 12% (taşınmaz rotasyonu)
- 0% borçlanma/altın (agresif "her şey hisse")
```

### Örnek 3: Defansif profil, teknoloji teması

```
İskelet:
- Borçlanma 50%, Altın 15%, P.piyasa 10%, Hisse-pazar 15%, Hisse-tek 5%, Karma 5%

Tilt: Defansif kullanıcı sektör tilt yapamaz. Sadece +2% Hisse-tek konjonktürel olarak makul.

Final:
- VES (Borçlanma) 30%, ZHG (Kamu Borçlanma) 20%
- VGA (Altın Katılım) 10%, EAE (Agesa Altın) 5%
- VEL (Para Piyasası) 10%
- VEH (Hisse Senedi) 15%
- TBJ (Teknoloji) 5% + FFC 2% = 7%
- HHY (Karma) 3%
```

## Sepet onaylandıktan sonra

`references/providers/{kurum}.md`'i oku ve eSube'de uygula. Browser otomasyonu adımları orada.

`memory/users/{kısa_ad}/current_basket.md`'yi güncelle:
- "Talep tarihi" + "Gerçekleşme tarihi" doldur
- Her fon için "Talep tarihi pay fiyatı" yaz (TEFAS veya eSube fon detayından)
- "Önceki sepetin gerçekleşmiş getirisi" bölümünü hesapla ve yaz (yeni revize başlamadan önceki sepetin nasıl performe ettiği)

Pay fiyatlarını eklemeden geçme — bir sonraki revizede gerçek getiri hesabı bu fiyatlara bağlı.

Bir de `history/{YYYY-MM}.md`'ye o ayın özetini yaz (gerekçe, karar, performans geri beslemesi dahil).
