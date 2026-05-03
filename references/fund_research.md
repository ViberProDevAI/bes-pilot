# Fon Araştırma — Veri Toplama (yedekli zincir)

Sepet kurulurken/revize edilirken **güncel piyasa verisi** gerekiyor. Bu referans nereden ne çekeceğini söyler **ve birinci kaynak kırılırsa devreye girecek yedekleri** tarif eder. Tek nokta arıza yok.

## Veri kaynağı zinciri — sıralı dene, ilki çalışana kadar git

```
┌─────────────────────────────────────┐
│ 1. CNBCe haftalık derleme (öncelik) │
│    → bulamazsan/kıırıksa ↓          │
├─────────────────────────────────────┤
│ 2. besfongetirileri.com (aylık)     │
│    → AJAX hata varsa ↓              │
├─────────────────────────────────────┤
│ 3. fintables.com (yedek, büyük HTML)│
│    → siteler kapanır/bot block ↓    │
├─────────────────────────────────────┤
│ 4. TEFAS resmi (rate limit dikkat)  │
│    → o da çalışmazsa ↓              │
├─────────────────────────────────────┤
│ 5. Manuel kullanıcı veri girişi     │
│    "Bu ay otomatik veri çekilemedi, │
│     besfongetirileri.com'u açıp      │
│     top 5 fonu söyler misin?"       │
└─────────────────────────────────────┘
```

**Kural**: En az **2 kaynaktan** veri al ve karşılaştır. Tek kaynaktan veri yeterli değil — ne CNBCe, ne fintables yanlış parse'lanabilir, ne de tek bir gün rakamı temsili olur.

## Birincil kaynak: CNBCe haftalık derlemesi

CNBCe her hafta sonu "En çok kazandıran ve kaybettiren fonlar" yazısı yayınlar. **En güvenilir haftalık snapshot.**

URL kalıbı: `https://www.cnbce.com/borsa/en-cok-kazandiran-ve-kaybettiren-fonlar-{TARIH}-h{ID}`

WebSearch ile bul:
```
"haftanın en çok kazandıran emeklilik fonları" {AY} {YIL}
```

İçeriğinden çıkarman gereken:
- En çok kazandıran emeklilik fonu top 10 (fon adı + % getiri)
- En çok kaybettiren top 10 (counter-momentum fırsatları için)
- Haftalık ortalama varsa not et

**CNBCe çalışmadıysa** (HTML değişti, yazı bulunamadı, parse başarısız):
- Hata mesajı: "CNBCe haftalık yazısı bulunamadı/parse edilemedi"
- Otomatik olarak Kaynak 2'ye geç

## Yedek kaynak 2: besfongetirileri.com

Sayfa: https://www.besfongetirileri.com/

Sekme'ler: Hafta / Ay / 2 Ay / 3 Ay / 6 Ay / YBB / Yıl. **Hafta sekmesi AJAX ile yüklenir** — düz fetch'le sadece "Ay" görünür.

Akış:
1. Aylık tabloyu fetch et (bu güvenilir)
2. Haftalık için Claude in Chrome veya WebFetch + manuel JS değerlendirme
3. Aylık veri yeterliyse haftalık atla, "haftalık veri bulunamadı, aylıkla devam" notu düş

**besfongetirileri.com çalışmadıysa** (rate limit, bot block, site bakımda):
- Hata mesajı: "besfongetirileri.com erişilemedi"
- Otomatik olarak Kaynak 3'e geç

## Yedek kaynak 3: fintables.com

Sayfa: https://fintables.com/fonlar/emeklilik-fonlari/getiri

Fetch sırasında dosya çok büyük olur (>300K char). Subagent'a ver, satır kırılmış halde okutma:

```
Subagent prompt: "Bu dosyada Türkiye BES fonlarının haftalık getirileri var. 
En yüksek 1 haftalık getiri sıralamasını çıkar. Python ile 80K karakterlik 
dilimlerde aç (read()[A:B])..."
```

## Yedek kaynak 4: TEFAS resmi (son çare otomatik)

URL: https://www.tefas.gov.tr/FonKarsilastirma.aspx

TEFAS resmi platform — günlük güncellenir, **fon pay fiyatları için tek otoriter kaynak**. Ama listeleme arayüzü ağır, scrape için zor. Bu kaynak özellikle **gerçekleşmiş getiri hesabı** için kritik (current_basket.md'deki "Talep tarihi pay fiyatı" alanı buradan doğrulanır).

## Son çare: Manuel kullanıcı veri girişi

4 kaynak da çalışmadıysa kullanıcıya açıkla:

```
Bu ay otomatik veri kaynaklarından getiri verilerini çekemedim:
- CNBCe: HTML pattern eşleşmedi
- besfongetirileri.com: Bağlantı zaman aşımı
- fintables.com: 403 (bot engeli)
- TEFAS: Rate limit

Birlikte veri toplayalım. Lütfen besfongetirileri.com'u tarayıcıda 
aç ve "Hafta" sekmesindeki ilk 10 fonu söyle (kod + getiri %).
```

Bu durum nadir ama olduğunda kullanıcı sürecin neden takıldığını anlamalı, sessiz başarısızlık olmamalı.

## Veri toplarken cevaplaman gereken sorular

Sepet kurmadan önce şu **6 soruya cevap bul**:

1. **Son 1 haftanın lider fon kategorisi nedir?** (teknoloji / altın / borçlanma / hisse / vb.)
2. **Top 10 haftalık kazandıran fonlardan kaçı tek bir kategoriden?** (konsantrasyon ölçütü — eğer 8+'i tek kategoriden ise momentum güçlü)
3. **Son 1 ay trendi haftayla aynı yönde mi?** (eğer hafta = ay yönü → trend doğrulanmış; ters → reversal var)
4. **En çok kaybettiren kategori hangisi?** (counter-momentum / mean-reversion fırsatı için)
5. **Makro şok var mı?** (TCMB faiz değişimi, USDTRY hareketi, jeopolitik) — WebSearch ile son 7 günün haberlerini tara
6. **Devlet katkısı kuralı veya BES regülasyonu değişikliği var mı?** (Genelge 2026/1 Temmuz 2026'da yürürlüğe girdi — yıl içi nadiren olur, ama olursa haberi al)

## Top performerlardan fon kodlarını çıkarma

CNBCe yazısı veya başka kaynak fon adını verir, fon kodu (3 harf) genelde verilmez. Adı kod'a çevirmek için:

- besfongetirileri.com fon arama
- fintables.com fon listesi
- TEFAS fon arama: https://www.tefas.gov.tr/FonAnaSayfa.aspx?FonKod={KOD}
- Veya BES kurumu eSube'sindeki fon listesi (zaten browser'da açıksa)

## Bilinen yaygın momentum fonları (referans tablo — DOĞRULANMASI GEREKEN)

> ⚠️ Bu liste **2026 başı itibarıyla** derlenmiştir. Kod ve fon ismi eşleştirmesi her ay TEFAS'tan **çapraz doğrulanmalı** — fonlar isim değiştirebilir, fon birleşmesi olabilir, yeni kodlar açılır. Aylık revizede top performer'ları **daima sıfırdan araştır**, bu listeyi sadece "bu kodu görürsen aşağı yukarı budur" diye referans olarak kullan.

| Tema | Kod | Fon Adı | Kurucu |
|---|---|---|---|
| Teknoloji yabancı | AVR | Teknoloji Sektörü Yabancı Değişken EYF | Agesa |
| Teknoloji lokal hisse | TVH | Teknoloji ŞTİ. Hisse Senedi EYF | Agesa |
| Teknoloji lokal hisse | TBJ | Teknoloji Sektörü Hisse Senedi EYF | Türkiye Hayat |
| Teknoloji yeni nesil | GCN | Yeni Teknolojiler Hisse Senedi EYF | Garanti |
| Teknoloji fon sepeti | YZD | Teknoloji Fon Sepeti EYF | Allianz Yaşam |
| Teknoloji değişken | FFC | Teknoloji Sektörü Değişken EYF | HDI Fiba |
| Teknoloji değişken | BZY | Teknoloji Sektörü Değişken EYF | BNP Paribas Cardif |
| Teknoloji fon sepeti | MEV | Teknoloji Fon Sepeti EYF | MetLife |
| Teknoloji hisse | BHT | Teknoloji Sektörü Hisse Senedi EYF | Anadolu Hayat |
| Enerji | ENF | Enerji Sektörü Değişken EYF | Agesa |
| Taşınmaz/İnşaat | TSZ | Taşınmaz ve İnş. Sek. Değiş. EYF | Agesa |
| Sürdürülebilirlik | ZHB | Sürdürülebilirlik Hisse Senedi EYF | Türkiye Hayat |
| Altın | VGA | Altın Katılım EYF | Türkiye Hayat |
| Altın | EAE | Altın EYF | Agesa |
| Altın | GEV | Altın Katılım EYF | Agesa |
| Borçlanma TL | VES | Borçlanma Araçları EYF | Türkiye Hayat |
| Borçlanma kamu | ZHG | Kamu Borçlanma Araçları EYF | Türkiye Hayat |
| Para piyasası | VEL | Para Piyasası EYF | Türkiye Hayat |

## Sepet sürekliliği için: Geçmiş verisi

Yıl boyu aynı kullanıcıyla çalışıyoruz. `memory/users/{kısa_ad}/history/` altındaki son 3 ayı oku — geçmişteki sepet bileşimleri, ne işe yaradı, ne yaramadı. Aşırı dönüş (her ay tüm sepeti değiştirme) kullanıcıyı yorar ve fon değişiklik hakkını harcar. **Stabilite avantajdır**:

- Eğer geçen ay ile aynı tema lider → sepeti büyük ölçüde aynı tut, sadece fon-spesifik tweaks yap
- Eğer tema değişti → daha köklü revize gerekli

## Pay fiyatı verisi — gerçekleşmiş getiri için kritik

Aylık revize sırasında **önceki sepetin gerçek getirisi** hesaplanmalı (current_basket.md'deki "Önceki sepetin gerçekleşmiş getirisi" bölümü için). Fon pay fiyatı kaynakları:

1. **TEFAS** (otoriter): `https://www.tefas.gov.tr/FonKarsilastirma.aspx?fonkod={KOD1},{KOD2}` — tarih aralığıyla sorgu
2. **eSube fon detayı** (kullanıcının kurumu): "Fon Bilgileri" sayfasında günlük pay fiyatı listesi
3. **besfongetirileri.com**: Her fonun detay sayfasında tarihe göre pay fiyatı

İki tarih için pay fiyatı çekmen gerekiyor: **önceki revize tarihi** ve **bu revize tarihi**. Aralarındaki fark = ham getiri.

> Eğer pay fiyatı eski tarihler için bulunamıyorsa: `current_basket.md`'deki kayıtlı "Talep tarihi pay fiyatı"nı kullan. Bu yüzden pay fiyatlarını sepet uygulanırken not etmek **vazgeçilmez** — ileri tarih için nadiren geri dönebilirsin.

## Çıktı formatı (sepet kuruluş için input)

`basket_construction.md`'i çağırırken bu özeti ver:

```markdown
## Bu ayın piyasa özeti — {YYYY-MM}

**Veri kaynakları kullanıldı**: CNBCe + besfongetirileri (her ikisinde lider tema teyit edildi)
**Lider tema**: Teknoloji (haftalık 7/10 fon, aylık 9/10 fon teknoloji)
**Trend doğrulanmış mı**: Evet (hafta = ay yönü aynı, momentum güçlü)
**En kötü kategori**: Kıymetli madenler (-1% hafta) — counter-momentum fırsatı?
**Makro şok**: Yok / TCMB faizi sabit / USDTRY 35.40 (geçen aydan +0.8%)

**Top 10 haftalık BES fonu**:
1. AVR — Agesa Tek. Yabancı +5.19%
2. BZY — BNP Cardif Tek. +3.55%
...

**Aylık konsensüs lider**:
- FFC (HDI Fiba) +21.86% / 1 ay
- AVR (Agesa) +23.77% / 1 ay
```

## Veri yokluğu durumunda akış

Eğer 4 kaynaktan da yeterli veri toplayamadıysan:

1. Kullanıcıya **şeffaf ol**: "Bu ay otomatik veri yetersiz, 2 seçenek var"
2. **Seçenek A**: Pas geç, sepeti değiştirme — bilgisiz karar değişikliğinden, bilgili pas üstündür
3. **Seçenek B**: Manuel veri girişi — kullanıcı 1-2 kaynak açıp özet verir, skill devam eder

Sessiz tahmin yapma. "Veri yok ama sepet öneriyorum" senaryosu yasak.
