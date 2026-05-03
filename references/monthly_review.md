# Aylık Revize Akışı

Her ayın 1'inde scheduled task tarafından otomatik tetiklenir, ya da kullanıcı `/bes-revize` komutuyla manuel başlatır. Bu akışın amacı: kullanıcıyı yormadan, fon değişiklik hakkını boşa harcatmadan, piyasa değiştiyse sepeti uyumla — değişmediyse pas geç. Ek olarak, **önceki sepetin gerçek getirisini ölç ve kayda al** — strateji çalışıyor mu çalışmıyor mu hep bilinsin.

## Akış (sırayla)

### Adım 1: Belleği aç ve durumu çıkar

```
1. memory/users/{kısa_ad}/profile.md → mevcut profil
2. memory/users/{kısa_ad}/current_basket.md → mevcut sepet + talep tarihi pay fiyatları
3. memory/users/{kısa_ad}/history/{son 3 ay} → trend
```

Bu üç dosyayı oku ve özet çıkar:
- "Kullanıcımız, dengeli profilde, Mayıs sepeti %75 teknoloji ağırlıklıydı, Şubat-Nisan boyunca tema teknoloji."

### Adım 2: Yaş kontrolü (otomatik)

Profile.md'deki **doğum tarihinden** mevcut yaşı hesapla. Eşik geçişlerini kontrol et:

| Mevcut profil | Yaş | Eşik geçilmiş mi |
|---|---|---|
| AGRESİF | 40 oldu | Evet → DENGELİ öner |
| DENGELİ | 55 oldu | Evet → DEFANSİF öner |
| (her seviye) | Vade < 10 yıl | Evet → DEFANSİF öner |

**Eşik öneri kuralı**:
1. Profile.md'de "Override geçmişi" tablosunda zaten bu eşik için **kullanıcı kararı varsa** → tekrar sorma, mevcut profile uy
2. Yoksa kullanıcıya öner, cevabı kayda al, override tablosunu güncelle

Örnek:
```
[Skill]: Bu yıl 40 yaşına girdin. Genel öneri: agresif → dengeli geçiş 
(emekliliğe vade 24 yıl, hala uzun ama sequence-of-returns risk oluşmaya 
başlıyor). 3 seçenek:
A) Dengeli'ye geç (sektör tilt 30%, hisse %50)
B) Agresif kal (vadem hala çok uzun)
C) Karma — agresifin yumuşak bir versiyonunu dene (hisse-tek 40%, dengeli'ye doğru çekilmiş)

Hangisi?
```

Cevap profile.md'deki "Kullanıcı override geçmişi"ne yazılır. Bir sonraki yıl 41 olduğunda tekrar sorulmaz.

### Adım 3: Önceki sepetin gerçekleşmiş getirisini hesapla

> **Bu adım, skill'in kendini ölçmesinin tek yoludur.** Atlamak yasak.

3a. **Tarih aralığını belirle**: `current_basket.md`'deki "Talep tarihi" → bugün

3b. **Her fon için pay fiyatı çek**:
- Kayıtlı `Talep tarihi pay fiyatı` (current_basket.md'de yazılı)
- Bugünün pay fiyatı (TEFAS, eSube fon detayı, veya besfongetirileri.com fon detay)

3c. **Ham getiri hesapla**:
```
fon_getiri = (yeni_pay_fiyatı / önceki_pay_fiyatı - 1) × 100
```

3d. **Ağırlıklı sepet getirisi**:
```
sepet_getiri = Σ (fon_ağırlığı × fon_getirisi)
```

3e. **Benchmark'lar**:
- BIST 100 (aynı tarih aralığı) — TCMB EVDS (https://evds2.tcmb.gov.tr/) veya tradingview
- TÜFE (aynı ay) — TÜİK (https://www.tuik.gov.tr/)

3f. **Reel getiri**:
```
reel_getiri = sepet_getiri - tüfe_yüzde
benchmark_farkı = sepet_getiri - bist_yüzde
```

3g. **Sonuçları current_basket.md'deki "Önceki sepetin gerçekleşmiş getirisi" bölümüne yaz** + history dosyasına da kopyala.

#### Eğer pay fiyatı bulunamazsa

Sözleşme yeniyse (ilk revize) önceki getiri yok, atla. Ama eski revizede pay fiyatı kaydedilmemişse:

- TEFAS'tan tarih aralıklı sorgu yap: `https://www.tefas.gov.tr/FonKarsilastirma.aspx?fonkod={KOD}` (tarih seçimi UI'dan)
- eSube fon detay sayfasından geçmiş günlük pay fiyatları
- Bulamazsan: kullanıcıya açık ol, "önceki getiri hesaplanamadı" diye not düş, history'ye yaz, gelecek revizede tekrar topla

### Adım 4: Bu ayın piyasa verisini topla

`references/fund_research.md`'i oku ve takip et. Yedekli zinciri kullan (CNBCe → besfongetirileri → fintables → TEFAS → manuel). **6 sorunun** cevabını çıkar:

1. Lider tema?
2. Konsantrasyon?
3. Trend doğrulanmış mı?
4. Counter-momentum fırsatı?
5. Makro şok?
6. Regülasyon değişikliği?

Bu özeti yaz, history dosyasına eklenecek.

### Adım 5: Karşılaştır — değişiklik gerekli mi?

| Durum | Karar |
|---|---|
| Tema aynı, fon liderleri aynı, önceki sepet benchmark üstü | **Pas geç** — fon hakkını koru, çalışan sepeti bozma |
| Tema aynı, fon liderleri değişti (örn. AVR yerine TVH lider oldu) | **Marjinal revize** — sadece o fonu değiştir |
| Tema değişti (teknoloji → enerji vb.) | **Köklü revize** — tilt'i kaydır |
| Önceki sepet benchmark altı 2 ay üst üste | **Mantığı sorgula** — kullanıcıya sun, "stratejide hata var, profili gözden geçirelim mi?" |
| Makro şok var | **Defansife geçici geçiş** + sonraki ay tekrar değerlendir |
| Counter-momentum güçlü (en kötü kategori 3+ ay üst üste düştü) | **%5-10 mean-reversion bahsi** ekle |
| Yaş eşiği geçti, kullanıcı henüz override etmemiş | Risk profili güncelle, **temel allokasyon yenile** |

> Önceki sepet performansını dikkate alma neden önemli: skill, "teknoloji rallisi" diyerek 3 ay üst üste underperform'lu öneri verirse, 4. ay aynı tema bahsiyle gelmesi inandırıcı değil. Performans, kararın bir girdisidir, sadece sonuç kaydı değil.

### Adım 6: Yeni sepeti hesapla (gerekiyorsa)

`references/basket_construction.md`'i takip et. **Stabilite cezası** uygula — gereksiz değişikliklerden kaçın.

### Adım 7: Kullanıcıya öneriyle gel

Şu formatta sun (önceki performans dahil):

```markdown
## Aylık BES Revizesi — {YYYY-MM}

**Önceki sepet**: {tarih}'te uygulandı, profil: {profil}, tema: {tema}

### Önceki ayın performansı
| Metrik | Değer | Yorum |
|---|---|---|
| Sepet ağırlıklı getiri | %{X.XX} | (33 günlük) |
| BIST 100 (aynı aralık) | %{Y.YY} | benchmark |
| TÜFE | %{Z.ZZ} | enflasyon |
| **Reel getiri** | %{X-Z} | TÜFE üstü mü? ✅/❌ |
| **Benchmark farkı** | %{X-Y} | BIST üstü mü? ✅/❌ |

**Yorum**: {1-2 cümle — strateji çalıştı/çalışmadı, sebepler}

### Bu ayın piyasa özeti
{1-2 cümle, fund_research.md çıktısı}

### Önerilen aksiyon: {DEĞİŞİKLİK GEREK / MARJİNAL TWEAK / PAS GEÇ}

[Eğer DEĞİŞİKLİK GEREK]:
| Fon | Eski % | Yeni % | Δ |
|---|---|---|---|
| TVH | 13 | 15 | +2 |
| ENF | 10 | 0 | -10 (enerji teması zayıfladı) |
| YZD | 12 | 13 | +1 |
| BHT | 0 | 9 | +9 (yeni) |

**Gerekçe**: {2-3 cümle}

**Kullanılacak hak**: 1 (kalan: 8/12 yıl içi)

[Eğer PAS GEÇ]:
Bu ay marjinal değişiklik anlamlı değil. Mevcut sepeti koruyalım. 
Bir sonraki revize: {bir sonraki ay 1'i}
Önceki ayın getirisi yine de kayda alındı (history dosyasında).
```

### Adım 8: Onay → eSube'ye gir → uygula

Kullanıcı onayladıysa:
1. `references/providers/{kurum}.md`'i oku
2. eSube'ye gir, fon dağılım değişikliği ekranına git
3. BEFAS gerekiyorsa kurumları/fonları ekle
4. Yüzdeleri JS ile gir, toplam 100'ü doğrula
5. **Her fonun talep tarihi pay fiyatını** eSube fon detayından veya TEFAS'tan oku ve not et — `current_basket.md`'ye yazılacak (gelecek revize bunu kullanacak)
6. **Kullanıcı "Tamam"a bassın**

Akış sırasında hata oluşursa (timeout, validator failure, oturum kopması): `references/error_recovery.md`'i oku, oradaki playbook'tan ilgili senaryoyu uygula.

### Adım 9: History yaz + current_basket güncelle

`memory/users/{kısa_ad}/history/{YYYY-MM}.md`'i `_template/history/_example.md` formatında yaz:
- Önceki sepetin gerçekleşmiş getirisi tablosu
- Bu ayın piyasa özeti
- Karar gerekçesi
- Yeni sepet
- eSube sürecinde olanlar (validator hataları, retry'lar, "Tamam" zamanı)
- Bir sonraki revizede izlenecekler

`current_basket.md`'yi güncelle:
- Yeni fon listesi + ağırlıklar + talep tarihi pay fiyatları
- "Kullanılan hak" sayacı arttı
- "Bir sonraki revize" tarihi
- "Önceki sepetin gerçekleşmiş getirisi" bölümü dolu (Adım 3'te yazıldı)

## Pas geçilen ayları da kayda geç

Eğer "pas geçildi" diyorsan, **history dosyası gene yaz** ama içinde "değişiklik yapılmadı, gerekçesi: ..." diye not düş + önceki sepetin gerçek getirisini gene hesapla. Trendi takip etmek için kümülatif kayıt önemli — performans verisi zincirinde delik olmasın.

## Otomatik tetikleme + insan onayı

Scheduled task çalıştığında her zaman kullanıcının onayını bekle — sen kendi başına eSube'ye girip değişiklik yapmazsın. Tetikleme dediği şey: "Hey kullanıcı, bu ayın özeti ve önerim hazır, onaylar mısın?" mesajı atmak. Kullanıcı online olunca açar, onaylarsa devam edersin.

Cowork mode'da bu mesaj direkt sohbette belirir; kullanıcı görmek için sohbeti açtığında devralırsın. Mesajda asla yatırım kararı tek başına alınmış olmamalı — her zaman bir öneri + onay isteme.

## Yıllık özel akış

Her **Ocak ilk revizesinde** (yeni takvim yılı, fon değişiklik hakkı 12'ye sıfırlandı):
- Önceki yılın özetini çıkar (`commands/bes-yillik`'i tetikle veya `references/annual_review.md`'i oku)
- Geçen yıl kaç hak harcanmış, hangi temalar çalışmış, toplam getiri nedir, vergisel notlar
- Bu özet kullanıcıya tek sefer gösterilir, sonra normal aylık akışa devam edilir

## Adım atlamak yasak

Bu akışta her adımın gerekçesi var:
- Adım 2 atlandığında kullanıcı yaşı geçmiş bir profile yıllarca takılı kalır
- Adım 3 atlandığında strateji ölçülemez, "şans mı strateji mi" sorusu cevapsız
- Adım 5'teki "önceki sepet 2 ay üst üste underperform" kuralı atlandığında skill yanlış stratejide ısrar eder

Atlanması gereken adım yok — kısa kestiğin yerden ekstra iş çıkar.
