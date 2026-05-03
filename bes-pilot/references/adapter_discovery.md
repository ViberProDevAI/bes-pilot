# Adapter Keşfi — Yeni Bir Kurum İçin Yaşayan Öğrenme

Türkiye Hayat dışındaki 17 BES kurumu **stub** olarak işaretli — yapısal akış benzer ama UI'lar farklı, JS selector'leri farklı, validator davranışları farklı. Bu dosya, skill'in bir kullanıcıyla birlikte **bu kurumu canlı keşfederek kalıcı bir adapter üretmesini** anlatır.

## Felsefe

Tek bir kullanıcının ilk seferi 30-60 dakika sürer. Sonraki tüm aylar (ve sonraki tüm kullanıcılar) için **adapter hazır**. Yani 30 dakika harcayan ilk gönüllü, kendisinden sonra geleceklere ücretsiz hediye bırakır. Bu bir topluluk akışı — `CONTRIBUTING.md` PR yolunu açıklar; ama yerel kullanım için de skill kendi `memory/users/{kısa_ad}/` altına özel adapter saklayabilir.

## Ne zaman tetiklenir?

Üç durumda:

1. **Onboarding sırasında**: Kullanıcı stub kurumlardan birini seçtiyse skill önerir
2. **Aylık revizede**: Sözleşme stub kurumda ve adapter henüz yoksa skill önerir
3. **Manuel**: `/bes-kurum-kesfet` komutu — kullanıcı bilerek başlatır

Skill **asla zorlamaz**. Kullanıcı "şimdi vakit yok" derse skill manuel modda çalışır (öneri verir, kullanıcı eSube'de elle uygular). Keşif başka bir zaman yapılabilir.

## Akış

### Adım 0: Onay ve hazırlık

Kullanıcıya net bir teklif:

```
{Kurum} için tam test edilmiş bir adapter yok. İki seçenek var:

A) Birlikte keşfedelim — 30-60 dk, ekran ekran ilerleyeceğiz, 
   sonunda kalıcı adapter oluşturacağız. Sonraki tüm kullanımlar 
   otomatik. (Topluluğa katkı yapma şansın da var: PR olarak 
   gönderirsen bu kurumdaki tüm BES'liler için faydalı olur.)

B) Bu sefer manuel — sepet önerisini sunarım, sen eSube'de elle 
   uygularsın. Adapter sonraki bir oturumda da yapılabilir.

Hangisini istersin?
```

Kullanıcı A seçtiyse:

1. **Tarayıcı kullanılabilirliği kontrol et**: Claude in Chrome MCP yüklü mü? Yoksa kullanıcıdan yüklemesini iste veya manuel screenshots'la ilerle.
2. **Draft dosya oluştur**: `references/providers/{kurum_kisa_adi}_draft.md` (örn. `anadolu_hayat_draft.md`). Şablon: `references/providers/_stub_template.md`'i kopyala, başına şunu ekle:
   ```markdown
   ---
   adapter_durumu: KEŞİF (DRAFT)
   keşif_başlangıcı: {YYYY-MM-DD}
   keşfeden: {kısa_ad}
   ---
   
   > ⚠️ Bu adapter henüz tam test edilmedi. Kullanıcıyla birlikte canlı keşif sürüyor.
   ```
3. **Kullanıcıya beklenti seti**: "Her ekranda ne yaptığımı söyleyeceğim. Sen gördüklerini doğrula, ben her adımı drafte yazacağım."

### Adım 1: Login akışı

```
[Skill]: Şimdi {Kurum}'un sitesine git. Ana sayfada online işlemler/şube 
linkini bulduğunda söyle. URL'ini paylaş.
```

Skill, draft'a yazar:

```markdown
## Login akışı

1. Ana site URL: {kullanıcının paylaştığı URL}
2. Online işlemler linki: {ana sayfanın neresinde, nasıl ulaşılır}
3. Login URL: {Login.aspx benzeri, kullanıcı paylaşır}
4. Login alanları: {Müşteri No / TC Kimlik / E-posta / hangi alan?}
5. SMS doğrulama: {var mı, format ne}
6. Login sonrası açılan sayfa URL'i: {AnaSayfa.aspx benzeri}

⚠️ Kredentialler ve SMS koduna ASLA dokunma. Kullanıcı kendi yazar.
```

> Kullanıcının login bilgilerini sen yazma — sadece akış adımlarını kayda al.

### Adım 2: Hesap yapısı

```
[Skill]: Login oldun. Şu an ekranda ne görüyorsun? Sözleşme listesi var mı,
varsa kaç tane ve nasıl gösteriliyor?
```

Draft'a yazar:

```markdown
## Hesap yapısı

Login sonrası açılan sayfada görünenler:
- {sözleşme listesi formatı: tablo / kartlar / pasta grafik}
- Sözleşme bilgileri: {No, plan adı, mevcut birikim, ...}
- Sözleşmeye nasıl erişilir: {tıklama, satır seçme, ...}

Birden fazla sözleşme varsa: her biri için ayrı revize gerekir mi yoksa toplu mu?
```

### Adım 3: Fon dağılım değişikliği menüsüne erişim

```
[Skill]: Tek bir sözleşmeyi seç (test için kendinin olanı kullanıyoruz).
Fon dağılım değişikliği menüsüne nasıl ulaşıyorsun? Hangi sekmelere bastın?
```

Draft'a yazar:

```markdown
## Fon Dağılım Değişikliği akışına gitme

Kullanıcı yolu:
1. {Üst sekme adı} → {Alt sekme adı} → {Sol menü adı}
2. Sayfa URL'i: {... değişiklik sayfası URL'i}

Direkt URL ile gitmek mümkün mü test edildi: {evet/hayır, deneme sonucu}
```

### Adım 4: Sayfa yapısı

```
[Skill]: Şimdi fon dağılım değişikliği sayfasındasın. Hangi UI elementleri var?
- Bir radio butonu var mı (mevcut/gelecek/her ikisi gibi)?
- Fon listesi nasıl gösteriliyor (tablo, kart)?
- Yüzde girme alanı slider mı, sayı kutusu mu, dropdown mu?
- "Devam eden işlem" uyarısı var mı?
- "Kalan değişiklik hakkın" bilgisi nerede?
```

Draft'a yazar:

```markdown
## Sayfa yapısı

### Yeni Fon Dağılımı Talebim radio
Seçenekler: {liste}
Default: {hangisi}

### Fon listesi tablosu
Sütunlar: {liste}
Yüzde girme widget'ı: {slider tipi / numeric input / dropdown}
Plan limitleri görünür mü: {evet/hayır}

### Kalan hak göstergesi
Konum: {sayfanın neresinde}
Format: {"Kalan Hakkınız: N" veya alternatif}

### Devam eden işlem uyarısı
{varsa nasıl gösteriliyor, yoksa "yok"}
```

### Adım 5: JS selector'leri keşfi (developer tools ile)

> Bu adım kullanıcıdan tarayıcı developer tools (F12) açmasını gerektirir. Eğer kullanıcı teknik değilse bu adımı atla, skill manuel UI tıklamalarıyla çalışır (yavaş ama OK).

```
[Skill]: F12'ye bas, "Console" sekmesine geç. Şu komutu yapıştır ve çıktıyı söyle:

document.querySelectorAll('table tr').length

Sonra bu komutu yapıştır:

document.querySelectorAll('input[type="text"]').length

Sayfa yapısını anlamak için bu sayılar yeterli.
```

İleri seviye keşif için:

```javascript
// Fon kodu sütunu hangisinde?
Array.from(document.querySelectorAll('table tr')).slice(0,3).map(r => 
  Array.from(r.querySelectorAll('td')).map(c => c.innerText.trim().slice(0,20))
);

// Slider widget tipi
document.querySelectorAll('.range, .ion-slider, input[type="range"]').length;

// Form ID'leri
Array.from(document.querySelectorAll('[id*="Fon"], [id*="Dagilim"]')).map(e => e.id);
```

Çıktıları kullanıcı paylaşır, skill draft'a element ID'lerini, sınıf isimlerini, widget tipini yazar.

### Adım 6: BEFAS akışı (varsa)

```
[Skill]: BEFAS linki var mı sayfada? Tıklayınca ne oluyor?
```

Eğer BEFAS açılırsa, Türkiye Hayat akışına benzer bir akış kayda alınır:
- Bilgilendirme modal'ı var mı?
- Kurum çoklu seçim mi, tek tek mi?
- Fon ekleme nasıl yapılıyor?
- Kurum kodları (3 harfli)?

### Adım 7: Yüzde girme — pratik test

> En kritik adım. Kullanıcı **gerçek bir değişiklik yapacak**, ama "Tamam"a basmayacak (test amaçlı).

```
[Skill]: Şimdi 2-3 fonun yüzdesini değiştirmeyi deneyelim — örn. teknoloji 
fonuna %10, borçlanmaya %15. "Tamam"a basma, sadece girip toplam 100'e 
ulaştığını görelim.

İlk fon için yüzde 10 yaz. Sonra ekran ne yaptı? (Slider hareket etti mi, 
toplam göründü mü, validator uyardı mı?)
```

Draft'a yazar:

```markdown
## Yüzde girme — gözlem

Widget tipi: {slider / numeric input / dropdown}
Değer set edildiğinde: {slider hareket eder mi, toplam görünür mü}
Validator davranışı: {yüzde 100'e zorluyor mu, fazla/eksik kabul ediyor mu}
JS ile programatik set mümkün mü: {test sonucu}

Bilinen tuhaflıklar (ilk gözlem):
- {kullanıcının fark ettiği ama beklenmeyen davranışlar}
```

### Adım 8: Doğrulama ve onay

```
[Skill]: Test başarılı oldu — toplam 100'e ulaştı, validator uyarmadı. 
Şimdi gerçek revizeyi yapacaksak fon yüzdelerini istediğimiz gibi 
güncelleyelim ve sen "Tamam"a basacaksın. Hazır mısın?
```

Bu noktada skill normal akıştaki gibi çalışır — yüzdeleri girer, kullanıcı son onayı verir, SMS'i kullanıcı yazar.

### Adım 9: Hata kurtarma sapmaları

```
[Skill]: Bu süreçte hata aldın mı? (Validator yüzde düşürdü mü, oturum 
koptu mu, BEFAS modal açılmadı mı, "Tamam"a bastıktan sonra hata mesajı 
çıktı mı?)
```

Karşılaşılan her hata draft'a yazılır:

```markdown
## Hata kurtarma sapmaları (kuruma özel)

| Senaryo (error_recovery.md) | {Kurum}'da gözlem |
|---|---|
| Senaryo 2 (validator) | {ne oldu, nasıl çözüldü} |
| Senaryo 3 (BEFAS modal) | {gözlem} |
| ... | |

Yeni keşfedilen senaryolar:
- {kuruma özgü, error_recovery.md'de olmayan} 
```

### Adım 10: Pay fiyatı çekme

```
[Skill]: Aylık revizede önceki sepetin gerçek getirisini hesaplamak için 
fon pay fiyatlarına ihtiyacımız var. Bu kurumda fon detay sayfasında pay 
fiyatı görünüyor mu? URL pattern'i nasıl?
```

Draft'a yazar:

```markdown
## Pay fiyatı çekme

eSube'de fon detay sayfası: {URL pattern, örn. /Views/FonBilgileri.aspx?fonkod={KOD}}
Pay fiyatı element ID/sınıfı: {örn. #lblPayFiyati veya .fon-fiyat}
JS ile çekme:
```js
{çalışan kod}
```

Eğer eSube anlık fiyat vermiyorsa: TEFAS'tan al (https://www.tefas.gov.tr/FonAnaSayfa.aspx?FonKod={KOD})
```

## Promosyon: draft → kalıcı adapter

Akış başarıyla tamamlandığında (kullanıcı "Tamam"a bastı, talep düştü, "Talep alındı" mesajı geldi):

```
[Skill]: 🎉 {Kurum} eSube akışı baştan sona çalıştı. Bu deneyimi kalıcı 
adapter olarak kaydedelim mi?

Yes derseniz:
- references/providers/{kurum}_draft.md → references/providers/{kurum}.md
- README.md'deki "Desteklenen kurumlar" tablosu güncellenir: 🟡 → ✅
- Topluluğa katkı için PR yolu önerilir (opsiyonel)

Hayır derseniz draft kalır, bir sonraki kullanımda devam ederiz.
```

Onay alındıysa:

1. Draft dosyayı yeniden adlandır: `mv references/providers/{kurum}_draft.md references/providers/{kurum}.md`
2. Frontmatter'ı güncelle:
   ```markdown
   ---
   adapter_durumu: TEST EDİLMİŞ ✅
   ilk_test_tarihi: {YYYY-MM-DD}
   keşfeden: {anonim — örn. "topluluk katkısı"}
   ---
   ```
3. README'deki kurum tablosunda durum işaretini güncelle
4. Kullanıcıya PR önerisi:
   ```
   Bu adapter'ı topluluğa açık hale getirmek istersen:
   
   cd ~/Projects/bes-pilot
   git checkout -b feat/{kurum}-adapter
   git add references/providers/{kurum}.md README.md
   git commit -m "feat(provider): {Kurum} adapter'ı (test edildi)"
   git push origin feat/{kurum}-adapter
   gh pr create --title "feat(provider): {Kurum} adapter'ı" --body "..."
   ```

## Sonraki kullanımlarda gelişen adapter

Adapter `TEST EDİLMİŞ ✅` olduktan sonra, sonraki revizelerde yeni gözlem olursa skill ekler:

- Yeni hata senaryosu → `## Hata kurtarma sapmaları` bölümüne ekleme
- Yeni validator davranışı → `## Bilinen tuhaflıklar` bölümüne ekleme
- UI değişikliği → ilgili bölüm güncellenir, frontmatter'a "son_doğrulama: {tarih}" eklenir

Bu yüzden adapter zamanla **olgunlaşır**, statik kalmaz.

## Adapter olgunluk seviyeleri

| Seviye | İşaret | Anlam |
|---|---|---|
| 🔴 STUB | `_stub_template.md`'de | Hiç keşfedilmedi, sadece şablon |
| 🟡 KEŞİF | `_draft.md` uzantısı | Aktif keşif sürüyor, tamamlanmadı |
| 🟢 TEST EDİLMİŞ | normal `.md` | Bir kez baştan sona çalıştı |
| ✅ OLGUN | normal `.md`, frontmatter'da `olgunluk: olgun` | 3+ farklı revize, en az 2 farklı kullanıcı tarafından doğrulanmış |

Topluluğa katkı PR'larında olgunluk artırmak için kayıt önemli — README tablosunda kurum işareti olgunluk seviyesini yansıtır.

## Mahremiyet

Keşif sırasında kullanıcının ekranında **sözleşme no, birikim tutarı, ad-soyad** görünebilir. Skill bu bilgileri **draft'a yazmaz** — sadece UI yapısını, akışı, hata davranışlarını kayda alır. PII içeren screenshot'lar varsa kullanıcı paylaşmadan önce mask'lemelidir.

Promosyon sırasında dosya tekrar gözden geçirilir; PII varsa silinir, sonra kalıcı yapılır.

## Eğer keşif yarım kalırsa

Kullanıcı keşif sırasında "yeter, şimdi vakit yok" derse:
1. Draft dosyası `references/providers/{kurum}_draft.md` olarak kalır
2. Skill bir sonraki kullanımda kullanıcıya hatırlatır: "{Kurum} adapter keşfine kaldığımız yerden devam edelim mi? Şu adıma kadar gelmiştik: {son tamamlanan adım}"
3. Kullanıcı "evet" derse kaldığı yerden devam, "hayır" derse manuel mod aktif
