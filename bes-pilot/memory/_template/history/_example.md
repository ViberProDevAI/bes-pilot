# {YYYY-MM} Revizesi — TEMPLATE / SENTETIK ÖRNEK

> ⚠️ Bu dosya **gerçek bir kişiye ait değildir**. Aşağıdaki tüm sayılar (tarihler, fon kodları, getiri yüzdeleri, pay fiyatları) **şablonun nasıl doldurulacağını gösteren sentetik veridir**. Yeni bir kullanıcı için `memory/users/{kısa_ad}/history/{YYYY-MM}.md` oluştururken bu yapıyı kopyala, içindeki sayıları kullanıcının gerçek verisiyle değiştir.

**Tarih**: {YYYY-MM-DD}
**Karar**: Köklü revize uygulandı (mevcut karma → momentum sepet)
**Kullanılan hak**: bu revizeyle 4/12 (kalan: 8)

## Önceki sepetin gerçekleşmiş getirisi

> Bu kayıt 2026-04-01 ile 2026-05-04 arasında (33 gün, 24 iş günü) — yani Nisan revizesi geçerli olduğu süre.

| Kod | Fon | Ağırlık | Pay fiyatı 2026-04-01 | Pay fiyatı 2026-05-04 | Getiri | Katkı |
|---|---|---|---|---|---|---|
| AGB | Büyüme Katılım | 50% | 0.045623 | 0.043891 | -3.80% | -1.90% |
| HHY | Karma | 20% | 0.156234 | 0.158012 | +1.14% | +0.23% |
| FFC | Tek. Değişken | 15% | 0.234518 | 0.252307 | +7.59% | +1.14% |
| VEH | Hisse Senedi | 9% | 0.098712 | 0.101245 | +2.57% | +0.23% |
| CFA | Altın | 6% | 0.187234 | 0.182156 | -2.71% | -0.16% |

- **Sepet ağırlıklı getirisi**: -0.46%
- **BIST 100 (01.04 → 04.05)**: +2.83%  ← kaynak: TCMB EVDS / Tradingview
- **TÜFE (Nisan)**: +1.92%  ← kaynak: TÜİK
- **Reel getiri**: -0.46% − 1.92% = **-2.38%** (kullanıcı reel zarardaydı)
- **Benchmark farkı (BIST'e karşı)**: -0.46% − 2.83% = **-3.29%** (underperform)

### Çıkarım
Önceki "AGB ağırlıklı karma" sepet ay boyunca underperform etti. Hem reel kayıp, hem benchmark altı. Bu da köklü revize gerekçesinin verilerle desteklenmesi.

## Bu ayın piyasa özeti (yeni karar girdisi)

- **Lider tema**: Teknoloji (1 hafta top 10'un 7'si tek, 1 ay top 10'un 9'u tek)
- **En kötü kategori**: Kıymetli madenler (-1% hafta, -2.5% ay) — counter-momentum fırsatı kayda değer ama tek başına yetersiz
- **Trend**: Doğrulanmış (hafta = ay yönü aynı)
- **Makro**: TCMB faiz 42.5 sabit, USDTRY 35.40 (geçen aydan +0.8%)
- **Regülasyon değişikliği**: Yok (Genelge 2026/1 yürürlükte, ek değişiklik aranmadı)

## Karar gerekçesi

- Mevcut karma sepet yıl başından beri underperform, son ay reel zarar (-2.38%)
- Kullanıcı agresif istedi (override: yok, hak skoru +5)
- Teknoloji rallisi 4. ay üst üste — momentum güçlü, trend hafta=ay
- Stabilite cezası uygulanmadı: önceki sepet ile yeni sepet örtüşmesi <%15 (köklü değişim açıkça gerekli)

## Yeni sepet

| Kod | Fon | Kurucu | % | Geçen Ay | Δ |
|---|---|---|---|---|---|
| TVH | Teknoloji ŞTİ. Hisse | Agesa | 13 | 0 | +13 |
| TBJ | Teknoloji Hisse | THE | 13 | 0 | +13 |
| BZY | Teknoloji Değişken | BNP | 13 | 0 | +13 |
| ENF | Enerji Sektörü | Agesa | 13 | 0 | +13 |
| GCN | Yeni Teknoloji | Garanti | 12 | 0 | +12 |
| YZD | Teknoloji Fon Sepeti | Allianz Yaşam | 12 | 0 | +12 |
| FFC | Teknoloji Değişken | HDI Fiba | 12 | 15 | -3 |
| TSZ | Taşınmaz/İnşaat | Agesa | 12 | 0 | +12 |
| AGB | Büyüme Katılım | THE | 0 | 50 | -50 |
| HHY | Karma | THE | 0 | 20 | -20 |
| VEH | Hisse Senedi | THE | 0 | 9 | -9 |
| CFA | Altın | (THE) | 0 | 6 | -6 |

## eSube sürecinde olanlar

- BEFAS açıldı (5 farklı kurucu fonuna erişim)
- Validator TVH ve YZD'yi ilk pas'ta düşürdü, ikinci pas'ta düzeltildi (bilinen tuhaflık)
- FFC THE listesinde 2 satır göründü, biri sıfırlandı
- "Tamam" 2026-05-04 14:23'te kullanıcı tarafından basıldı
- SMS doğrulama 14:24'te tamamlandı
- Talep alındı mesajı 14:25'te gözüktü, beklenen gerçekleşme: 2026-05-09

## Bir sonraki revizede izlenecek

- Eylül'e doğru tatil sonrası rotasyon olabilir
- Eğer USDTRY 38+ olursa altın counter-bahsi düşünülebilir
- Eğer teknoloji 2 hafta üst üste yataysa momentum bittiği işareti
- 2026-06-01 tetikleme: önceki ayın gerçek getirisini hesaplayıp buraya tekrar yaz
