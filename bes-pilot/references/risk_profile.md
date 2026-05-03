# Risk Profili → Temel Allokasyon

Risk profilinden çıkan **temel allokasyon** sepetin iskeletidir. Sonra `basket_construction.md` bu iskelete momentum ve fon-spesifik seçimleri ekler.

## Sayıların kaynağı (şeffaflık)

Bu dosyadaki yüzdeler **BES kurucu kurumlarının kamu emeklilik fon dağılım önerileri** + **2-Hisse-Senedi-1-Hayat klasik yaşam-döngüsü çerçevesi** + **Türkiye'de 2024-2026 enflasyon konjonktürü** üçgeninden derlenmiştir. Bunlar **kalibre edilmiş, ama klinik backtest'le doğrulanmamış**. Aylık revize sürecinde (`monthly_review.md`) gerçekleşmiş getiriyle benchmark karşılaştırılır → eğer profil tutarlı şekilde benchmark'ın altındaysa eşikler revize edilmeli.

İddia → İtiraz → Cevap:
- **İddia**: "Defansif profilde %50 borçlanma, %15 altın iyi bir başlangıç."
- **İtiraz**: "Ya enflasyon %50 ve TL bonds reel kayıp veriyorsa? Bu konjonktürde defansif aslında saldırgan değil mi?"
- **Cevap**: Türkiye 2022-2025 boyunca yüksek enflasyon, yüksek nominal faizle birlikte yaşadı — bu konjonktürde TL bonds nominal getiriyi sağladı ama reel kayıpla kapanan dönemler de oldu. Defansif profil = "nominal sermaye koruma, reel iddialı değilim" tercihidir. Reel koruma isteyen kullanıcı için DENGELİ daha uygun.

## Üç profil — temel allokasyon

### DEFANSİF

```
Borçlanma araçları (TL bonds)        50%
Kıymetli madenler (altın)            15%
Para piyasası                         10%
Hisse - geniş pazar (BIST 30, broad) 15%
Hisse - sektör/teknoloji              5%
Karma/Değişken                         5%
```

**Mantık**: Sermaye koruma birinci öncelik. %25 hisse maruziyeti = kontrollü risk + uzun vadeli getiri katılımı. Altın enflasyon hedge'i + USD korelasyonu (TR konjonktüründe USDTRY ile altın TL fiyatı pozitif korele).

### DENGELİ

```
Borçlanma araçları                    25%
Kıymetli madenler                     10%
Hisse - geniş pazar                   20%
Hisse - sektör/teknoloji              30%
Karma/Değişken                        10%
Para piyasası                          5%
```

**Mantık**: Risk-adjusted büyümeye odaklanma. %50 hisse + %35 sabit getiri + %15 esnek. Sektör tilt'i (teknoloji ya da konjonktürel olarak güncel lider) momentum kazanma için.

### AGRESİF

```
Hisse - sektör/teknoloji              50%
Hisse - geniş pazar                   20%
Karma/Değişken                        10%
Borçlanma araçları                    10%
Kıymetli madenler                      5%
Hisse - sektörel rotasyon (enerji,
  taşınmaz, sürdürülebilirlik)         5%
```

**Mantık**: Maximum büyüme. %75 hisse, sadece %15 koruma. Sektör konsantrasyonu yüksek — momentum trendine binme stratejisi. Beklenen volatilite yüksek (yıllık standart sapma > %30) → kullanıcının kayıp toleransı C cevabıyla doğrulanmış olmalı, aksi halde override.

## Yaş eşikleri ve gerekçesi

| Profil | Tipik yaş üst sınırı | Gerekçe |
|---|---|---|
| AGRESİF | < 40 | 25+ yıl vade volatiliteyi dümdüz eder; tek bir resesyon kalan vadenin %4'ü |
| DENGELİ | 40-55 | 10-25 yıl vade — düşüşten sonra toparlanma süresi var ama "bir krizin ortasında çıkmak zorunda kalmak" riski belirir |
| DEFANSİF | > 55 | < 10 yıl vade — sequence-of-returns risk artar, emeklilikte düşüşten zarar yazmak iyileştirilemez |

> Eşikler **kabul görmüş yaşam-döngüsü emeklilik planlama** çerçevesine dayanır (target-date fonların standardı: yaş arttıkça hisse oranı düşer, bonds artar — "100 - yaş = hisse %" gibi). Ama bunlar **deterministik kurallar değil**, kullanıcı override edebilir. Skill her eşik geçişinde **bir kez** öneri yapar, cevap profile.md'ye yazılır, ileriki revizelerde tekrar sormaz (kullanıcının kararı kaydedildi).

### Yaş override örnekleri (kullanıcının haklı olduğu durumlar)

- **41 yaş, 24 yıl vade**: 65'te emeklilik istiyor → vade hala uzun → AGRESİF kalabilir
- **38 yaş, 7 yıl vade**: 45'te erken emeklilik istiyor → vade kısa → DENGELİ daha uygun
- **57 yaş ama yüksek refah seviyesi, BES portföyü toplam servetin %5'i**: DENGELİ kalabilir, kayıp toleransı yüksek

Bu yüzden yaş tek başına otomatik geçişe yetmez — vade ve kullanıcı tercihi de hesaba katılır.

## Kategori → fon kategorisi haritası

Fon kategorileri TEFAS/BEFAS'taki standart kategori isimleri:

| Allokasyon | TEFAS Kategorisi |
|---|---|
| Borçlanma araçları | "Borçlanma Araçları EYF", "Kamu Borçlanma Araçları EYF", "Kamu Dış Borçlanma Araçları EYF" |
| Kıymetli madenler | "Altın EYF", "Altın Katılım EYF", "Kıymetli Madenler EYF", "Kıymetli Madenler Katılım EYF" |
| Para piyasası | "Para Piyasası EYF", "Standart EYF", "Katılım Standart EYF" |
| Hisse - geniş pazar | "Hisse Senedi EYF", "BIST-30 Dışı Şirketler Hisse Senedi EYF", "Endeks EYF" |
| Hisse - sektör/teknoloji | "Teknoloji Sektörü Hisse Senedi EYF", "Teknoloji Sektörü Değişken EYF", "Teknoloji Sektörü Yabancı Değişken EYF", "Teknoloji Fon Sepeti EYF" |
| Hisse - sektörel rotasyon | "Enerji Sektörü Değişken EYF", "Taşınmaz ve İnşaat Sektörü Değişken EYF", "Sürdürülebilirlik Hisse Senedi EYF", "Sağlık Sektörü EYF" |
| Karma/Değişken | "Karma EYF", "Değişken EYF", "Dengeli Değişken EYF", "Dinamik Değişken EYF" |

## Önemli notlar

1. **Bu yüzdeler iskelet, son sepet değil**. Konjonktür her ay değişir, fon-spesifik seçimler `basket_construction.md`'de yapılır.

2. **18 yaş altı kumbara hesapları için özel**: Çocuğun emekliliğe vadesi 50+ yıl, bu yüzden teknik olarak agresife uygun. Ama veliye ait BES'lerle aynı kişide olduğu için bazen daha defansif tutmak istenir. **Onboarding'de açıkça sor**.

3. **Override kuralı kesin**: Onboarding'deki "kayıp tepkisi A" cevabı varsa AGRESİF asla seçilemez (bkz. onboarding.md). Bu kuralı bozma. Seçim mekanizması: önce override taraması, sonra puan eşiği uygulaması.

4. **Profil değişiklikleri kayda alınır**: Kullanıcı ileride profili değiştirirse (yaş eşiği, manuel override, kayıp toleransı revizyon) profile.md'deki "Risk profili" bölümünü güncelle, eski puanı silme — git history zaten tutulmuyor (memory/users/ gitignore'da), ama profile.md içinde "Profil son hesaplama" alanını güncelle.

## Fon kategorisi içinde fon seçimi

Bir kategori için **hangi fon (kod)** seçileceği `basket_construction.md`'de:
- Son 1 hafta + 1 ay getiriye göre kategori liderini bul
- Kullanıcının BES kurumu hangi fonları ulaşılabilir veriyor (BEFAS açıksa hepsi, kapalıysa sadece kendi kurumu)
- Tek fon değil 2-3 farklı kurucudan seç (kurucu bazlı çeşitlendirme)

Bu adıma `basket_construction.md`'den devam et.
