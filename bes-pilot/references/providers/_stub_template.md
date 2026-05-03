# Provider Stub — Yeni Kurum Adapter İskeleti

Bu dosya, henüz tam test edilmemiş BES kurumlarının canlı keşif sürecinde **draft adapter'ın başlangıç noktası** olarak kullanılır. Skill, kullanıcının kurumuyla ilk kez karşılaştığında bu iskeleti `references/providers/{kurum_kisa_adi}_draft.md` adıyla kopyalar ve kullanıcıyla birlikte ekran-ekran doldurur.

> **Not**: Tam keşif sürecinin detayı `references/adapter_discovery.md`'de. Bu dosya iskeletin kendisidir; süreç o dosyadadır.

## Skill, stub kuruma rastlayınca ne yapar?

`references/adapter_discovery.md`'i takip eder. Özet:

1. Kullanıcıya **iki seçenek** sunar:
   - **A) Birlikte keşfedelim** (30-60 dk, ilk seferde, sonraki tüm kullanımlar otomatik)
   - **B) Bu sefer manuel** (skill öneri verir, sen eSube'de elle uygularsın)

2. Kullanıcı A seçtiyse:
   - Bu dosyayı `_draft.md` uzantısıyla kopyalar
   - Frontmatter'ı doldurur (keşif başlangıç tarihi, durum: KEŞİF)
   - Adım adım ilerler, her ekranda kullanıcıyla birlikte UI'yı tanır, drafte yazar
   - Akış sonunda kalıcı `.md` adapter olarak kaydeder
   - README'deki kurum tablosunu günceller (🟡 → ✅)
   - Opsiyonel: topluluğa PR önerir

3. Kullanıcı B seçtiyse:
   - Skill normal akışta devam eder ama eSube'de gezme/tıklama yapmaz
   - Sepet önerisini sunar, kullanıcı eSube'de elle uygular
   - Bir sonraki ay tekrar A önerilir

## Şablon (kullanıcı keşifte bunu doldurur)

```markdown
---
adapter_durumu: KEŞİF (DRAFT) | TEST EDİLMİŞ ✅ | OLGUN
keşif_başlangıcı: {YYYY-MM-DD}
ilk_test_tarihi: {YYYY-MM-DD}
son_doğrulama: {YYYY-MM-DD}
---

# {Kurum Tam Adı} — eSube Adaptörü

Ana site: {URL}
Login: {URL}
Kurumsal site: {URL}

## Login akışı

1. Ana sitede {nereden} → "{link adı}" butonuna tıkla
2. {modal/yeni tab} → "Bireysel" seç
3. Login.aspx (veya benzeri) açılır
4. Müşteri No / TC Kimlik / E-posta — **kullanıcı kendi girer**
5. Şifre — **kullanıcı kendi girer**
6. SMS doğrulama — **kullanıcı kendi girer**
7. Login sonrası açılan sayfa: {URL}

⚠️ Kredentialler ve SMS koduna **asla dokunma**.

## Hesap yapısı

Login sonrası ekranda görünenler:
- Sözleşme listesi formatı: {tablo / kartlar / pasta grafik}
- Sözleşme bilgileri: {alan listesi}
- Sözleşmeye erişim: {nasıl tıklanır}

Birden fazla sözleşme: {her biri ayrı revize / toplu işlem}

## Fon Dağılım Değişikliği akışına gitme

1. {Üst sekme} → {Alt sekme} → {Sol menü}
2. Sayfa URL'i: {değişiklik sayfası URL}

Direkt URL erişimi: {evet/hayır}

## Sayfa yapısı

### Yeni Fon Dağılımı Talebim radio
Seçenekler:
- (default) {opsiyon 1}
- {opsiyon 2}
- {opsiyon 3}

### Devam eden işlem uyarısı
{varsa nasıl gösteriliyor / yoksa "yok"}

### Fon listesi tablosu
Sütunlar: {Kod | Ad | Yeni % | Mevcut % | ...}
Yüzde widget tipi: {slider / numeric input / dropdown / IonRangeSlider}
Plan limitleri: {0-100 / kısıtlı / vb.}

### Kalan hak göstergesi
"Kalan Hakkınız: N" benzeri metin nerede: {konum}

## BEFAS akışı

{Kurum BEFAS desteklemiyorsa "BEFAS yok" yaz, gerisini atla.}

1. "{BEFAS link adı}" linkine tıkla
2. {Bilgilendirme modalı varsa: 6 madde uyarı + checkbox}
3. {Kurum seçici: tek seçim / çoklu seçim, dropdown / checkbox}
4. {Fon seçimi: checkbox / "Ekle" butonu}

### Kurum kodları (BEFAS sayfasında görünenler)

| Kod | Kurum |
|---|---|
| {3 harfli kod} | {Kurum tam adı} |
| ... | ... |

## Yüzde girme

Widget tipi: {detay}
JS ile programatik set:

```js
// Bu kuruma özel test edilmiş kod buraya
// Türkiye Hayat ile aynı pattern (IonRangeSlider) çalışmıyor olabilir
```

## Doğrulama (kritik)

1. Toplam = 100 kontrolü:
```js
// Toplam hesaplama JS'i
```

2. Bilinen sorunlar (validator davranışı):
- {örn: bazı fonlar ilk pas'ta düşürülüyor mu}
- {örn: aynı fon iki satırda görünüyor mu}

## Pay fiyatı çekme (gerçek getiri için)

eSube'de fon detay sayfası: {URL pattern}
Pay fiyatı element: {selector}
JS ile çekme:
```js
{kod}
```

Yedek: TEFAS (https://www.tefas.gov.tr/FonAnaSayfa.aspx?FonKod={KOD})

## Hata kurtarma sapmaları

`references/error_recovery.md`'deki ortak senaryolarla eşleşme:

| Senaryo | {Kurum}'da gözlem |
|---|---|
| 1 (oturum timeout) | {ne kadar süre sonra, ne yapıyor} |
| 2 (validator) | {pas davranışı} |
| 3 (BEFAS modal) | {açılma sorunu var mı} |
| 5 (kalan hak 0) | {nasıl gösteriliyor} |
| 9 ("Tamam" hata) | {hata mesajı formatı} |

Yeni keşfedilen kuruma özel senaryolar:
- {liste}

## Birden fazla sözleşme

Birinci sözleşmeyi onayladıktan sonra:
1. {Ana sayfaya nasıl dönülür}
2. {İkinci sözleşmeye nasıl geçilir}
3. {Akış tekrar başa döner mi yoksa devam eder mi}

## Bilinen tuhaflıklar

(keşif sırasında karşılaşılanlar buraya)

## Bir sonraki adım

Yüzdeler girildikten sonra:
1. Pay fiyatlarını eSube fon detayından/TEFAS'tan al
2. Kullanıcıya teslim et, "Tamam"a basmasını bekle
3. SMS doğrulama tamamlandıktan sonra "Talep alındı" ekranını gör
4. history yaz, current_basket.md'yi finalize et

Hata oluşursa: `references/error_recovery.md` + bu dosyadaki kuruma özel sapmalar.
```

## Adapter olgunluk yolculuğu

Skill, kullanım sayısına göre adapter'ı işaretler:

```
🔴 STUB (yok)
   ↓ kullanıcı + skill ilk keşif başlatır
🟡 KEŞİF (_draft.md, frontmatter: KEŞİF)
   ↓ baştan sona başarılı revize tamamlanır
🟢 TEST EDİLMİŞ (.md, frontmatter: TEST EDİLMİŞ)
   ↓ 3+ farklı revize, 2+ kullanıcı doğrulaması
✅ OLGUN (.md, frontmatter: OLGUN)
```

Her seviye atlama PR + commit ile kayda geçer (CONTRIBUTING.md akışı).

## Bilinen kurumlar — başlangıç ipuçları

Aşağıdaki listede her kurumun **olası** giriş noktaları var. Keşif sırasında bunlar başlangıç noktası olarak kullanılabilir, gerçek URL'ler değişmiş olabilir:

- **Anadolu Hayat**: anadoluhayat.com.tr → "Online İşlemler" → BES portali
- **Garanti Emeklilik**: garantibbvaemeklilik.com.tr (Garanti BBVA Mobil de bir seçenek)
- **Allianz Yaşam**: allianzyasam.com.tr
- **Allianz Hayat**: allianzhayat.com.tr
- **Agesa**: agesa.com.tr → "Online Şube"
- **HDI Fiba**: hdifibaemeklilik.com.tr
- **NN Hayat**: nnhayat.com.tr (artık AvivaSA'dan ayrı)
- **AvivaSA**: avivasa.com.tr
- **Vakıf Emeklilik**: vakifemeklilik.com.tr
- **AXA Hayat**: axahayatemeklilik.com.tr
- **BNP Paribas Cardif**: bnpparibascardif.com.tr
- **Bereket Emeklilik**: bereketemeklilik.com.tr
- **Katılım Emeklilik**: katilimemeklilik.com.tr
- **MetLife**: metlife.com.tr
- **QNB Sağlık & Hayat**: qnbhayat.com.tr
- **Vienna Life**: viennalife.com.tr
- **Zurich Yaşam**: zurich.com.tr/emeklilik

Çoğu BEFAS açıktır (regülasyon zorunluluğu — Genelge 2026/1). BEFAS bilgilendirme onayı her kurumda benzer şekilde işliyor (6 maddelik bilgilendirme + checkbox).

## Mahremiyet kuralı

Keşif sürecinde kullanıcının ekranında **sözleşme no, ad-soyad, birikim tutarı** görünür. Skill bunları **draft'a yazmaz** — sadece UI yapısı, akış, JS davranışı kayda alınır. Promosyon (kalıcı `.md`'ye dönüştürme) sırasında dosya gözden geçirilir, kişisel veri olmadığından emin olunur.

PR'a giderken `CONTRIBUTING.md`'deki PII kontrol listesi tekrar uygulanır.
