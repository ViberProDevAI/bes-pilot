# Türkiye Hayat ve Emeklilik — eSube Adaptörü (✅ TEST EDİLMİŞ)

URL: https://esube.turkiyehayatemeklilik.com.tr/
Login: https://esube.turkiyehayatemeklilik.com.tr/Views/Login.aspx
Kurumsal site: https://www.turkiyehayatemeklilik.com.tr/

**Bu adapter Mayıs 2026'da gerçek bir kullanıcının hesabında test edilerek çalıştırıldı.**

## Login akışı

1. Ana sitede sağ üstte **"Online İşlemler"** butonuna tıkla
2. Açılan modaldan **"Bireysel"** seç
3. Yeni tab'da Login.aspx açılır
4. Müşteri No / TC Kimlik + Şifre — **kullanıcı kendi girer**
5. SMS doğrulama gelir — **kullanıcı kendi girer**
6. AnaSayfa.aspx'e düşer

⚠️ Kredentialler ve SMS koduna **asla dokunma**. Kullanıcının "girdim" demesini bekle.

## Hesap yapısı

Ana sayfada (BireyselEmeklilik.aspx) sözleşme listesi var:
```
1 (GBB) XXXXXXXXX Gruba Bağlı Bireysel Emeklilik Planı 2
2 (BES) XXXXXXXXX 18 Yaş Altı Kumbara Bireysel Emeklilik Planı
```

Sözleşmeye tıklayınca pasta grafik o sözleşmenin birikim/devlet katkısı tutarını gösterir.

**Birden fazla sözleşme varsa her biri için ayrı revize gerekiyor**. Kullanıcı sözleşmelerin hepsi için aynı sepet mi farklı mı istediğini söylemediyse sor.

## Fon Dağılım Değişikliği akışına gitme

Doğru sözleşme seçili olduğundan emin ol, sonra:

1. Üst sekmeden **"Bireysel Emeklilik"** menüsüne tıkla (yoksa direkt URL ile git: `/Views/BireyselEmeklilik.aspx`)
2. Alt sekmelerden **"İşlemlerim"**
3. Sol menüden **"Fon Dağılım Değişikliği"**
4. Sayfa yüklenir: `/Views/BireyselEmeklilik-Islemlerim-FonDagilimDegisikligi.aspx`

## Sayfa yapısı

### Üst kısım: "Yeni Fon Dağılımı Talebim" radio
3 seçenek:
- (default seçili) Hem mevcut birikim hem gelecek katkılar — **bunu kullan**
- Sadece gelecek katkılar
- Sadece mevcut birikim

Default doğru, dokunma.

### Orta kısım: "Devam eden işlem" uyarısı (varsa)
Eğer son 2-3 iş günü içinde bir değişiklik yaptıysan ekran şunu söyler:
> "Devam eden fon dağılım değişikliği işleminiz bulunmaktadır. Bu işlem, tahmini olarak {tarih} tarihinde tamamlanacaktır."

Bu durumda yeni değişiklik **yapılamaz** — kullanıcıya bildir, beklesin.

### Alt kısım: Fon listesi tablosu

Sütunlar: **Fon Kodu | Fon Adı | Yeni Dağılım Oranı (slider) | Mevcut (%) | Plan Alt Limit | Plan Üst Limit | Fon Valör Süresi**

- **Yeni Dağılım Oranı**: IonRangeSlider widget. JS ile güncellenir.
- **Mevcut (%)**: Read-only, mevcut dağılımı gösterir
- **Plan Limitleri**: 0-1 ondalık (yani 0%-100%). Türkiye Hayat'ta her fon 0-100 arası, kısıt yok.

### En alt: "BEFAS Fonları İçin Tıklayınız" linki + "Tamam" butonu + "Kalan Hakkınız: N"

## BEFAS akışı

Diğer kurucu fonlarına erişim için:

1. **"BEFAS Fonları İçin Tıklayınız"** linkine tıkla
2. **BEFAS Bilgilendirme modalı** açılır:
   - 6 madde uyarı yazısı
   - Checkbox: "BEFAS'a ilişkin bilgilendirmeleri okudum ve anladım"
   - **Kullanıcı izin verirse** checkbox'ı işaretle, "Tamam"a bas
   - İlk seferinde mutlaka kullanıcıya BEFAS'ın trade-off'unu özetle:
     - ✅ Diğer kurucu (Agesa, Garanti, Allianz, HDI Fiba, BNP, vs.) fonlarına erişim
     - ⚠️ Devlet katkısı iade hesaplamasında sadece Türkiye Hayat fonlarından kesilen tutarlar dikkate alınır
     - ⚠️ İleri valörlü fon tercih edilirse nemalandırma yapılmaz
3. **BEFAS Fonları sayfası** açılır: `/Views/BireyselEmeklilik-Islemlerim-Befas-Fonlari.aspx`

### BEFAS sayfasında kurum + fon ekleme

**Kurum seçici** (Kurum Listesi alanı):
- Çoklu seçim multi-select (`<select id="ContentPlaceHolder1_drpFonKurum" multiple>`)
- 14 BES kurumu mevcut, kodları:

| Kod | Kurum |
|---|---|
| AHS | AGESA HAYAT VE EMEKLİLİK A.Ş. |
| HYS | ALLIANZ YAŞAM VE EMEKLİLİK A.Ş. |
| KHM | ALLİANZ HAYAT VE EMEKLİLİK A.Ş. |
| AEM | ANADOLU HAYAT EMEKLİLİK A.Ş. |
| AHY | AXA HAYAT VE EMEKLİLİK A.Ş. |
| ASH | BEREKET EMEKLİLİK VE HAYAT A.Ş. |
| FRE | BNP PARİBAS CARDİF EMEKLİLİK A.Ş. |
| GEM | GARANTİ EMEKLİLİK VE HAYAT A.Ş. |
| FBH | HDI FİBA EMEKLİLİK VE HAYAT A.Ş. |
| KEM | KATILIM EMEKLİLİK VE HAYAT A.Ş. |
| DEN | METLİFE EMEKLİLİK VE HAYAT A.Ş. |
| FEM | QNB SAĞLIK HAYAT SİGORTA VE EMEKLİLİK A.Ş. |
| ANM | VİENNALİFE EMEKLİLİK VE HAYAT A.Ş. |
| IEM | ZURİCH YAŞAM VE EMEKLİLİK A.Ş. |

Manuel tıklama yerine **JavaScript ile direkt option select edip change event tetikle** (daha güvenilir):

```js
const sel = document.getElementById('ContentPlaceHolder1_drpFonKurum');
const wantCodes = ['AHS', 'HYS', 'FRE', 'GEM', 'FBH']; // örnek
Array.from(sel.options).forEach(o => {
  o.selected = wantCodes.includes(o.value);
});
if (window.jQuery) {
  jQuery(sel).trigger('change.select2');
  jQuery(sel).trigger('change');
}
sel.dispatchEvent(new Event('change', {bubbles: true}));
```

Sonra ~3 saniye bekle, postback ile fon listesi yenilensin.

**Fon seçimi** (checkbox'lar):
Her fon için tablo satırında bir checkbox var. Sepetteki fonları tek seferde işaretle:

```js
const targets = ['TVH','ENF','GCN','YZD','FFC']; // örnek
const rows = document.querySelectorAll('table tr');
rows.forEach(row => {
  const cells = row.querySelectorAll('td');
  if (cells.length >= 2) {
    const code = cells[1] ? cells[1].innerText.trim() : '';
    if (targets.includes(code)) {
      const cb = row.querySelector('input[type="checkbox"]');
      if (cb && !cb.checked) cb.click();
    }
  }
});
```

**"Fon Ekle" butonuna tıkla** — ana fon dağılımı sayfasına döner, BEFAS fonları listede görünür.

## Yüzde girme

Yüzde inputları **IonRangeSlider** widget'ı kullanır. Her satırda 3 input var:

1. `<input type="hidden">` — fon kodunu tutar
2. `<input type="text" class="range irs-hidden-input" readonly>` — slider değeri (sync için)
3. `<input type="text" class="inp type-1 range-input numericAndDotOnly">` — kullanıcının yazacağı text alan

3. input'a değer ata + change event tetikle + IonRangeSlider'ı update et:

```js
const basket = {
  'TVH': 13, 'TBJ': 13, 'BZY': 13, 'GCN': 12,
  'YZD': 12, 'FFC': 12, 'TSZ': 12, 'ENF': 13
};
const nativeSetter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype, 'value'
).set;

document.querySelectorAll('table tr').forEach(row => {
  const cells = row.querySelectorAll('td');
  if (cells.length < 4 || !cells[0]) return;
  const code = cells[0].innerText.trim();
  if (code.length !== 3) return;
  
  const writable = Array.from(row.querySelectorAll('input')).find(i => 
    i.type === 'text' && !i.readOnly && i.className.includes('range-input')
  );
  const slider = row.querySelector('input.range.irs-hidden-input');
  if (!writable || !slider) return;
  
  const newVal = basket.hasOwnProperty(code) ? basket[code] : 0;
  
  writable.focus();
  nativeSetter.call(writable, String(newVal));
  writable.dispatchEvent(new Event('input', {bubbles: true}));
  writable.dispatchEvent(new Event('change', {bubbles: true}));
  
  const inst = jQuery(slider).data('ionRangeSlider');
  if (inst) inst.update({from: newVal});
  nativeSetter.call(slider, String(newVal));
  jQuery(slider).trigger('change');
  writable.blur();
});
```

## Doğrulama (kritik)

Her zaman:

1. **Toplam = 100 mu** kontrol et:
```js
let total = 0;
document.querySelectorAll('table tr').forEach(row => {
  const cells = row.querySelectorAll('td');
  if (cells.length < 4 || !cells[0]) return;
  const w = Array.from(row.querySelectorAll('input')).find(i => 
    i.type === 'text' && !i.readOnly && i.className.includes('range-input')
  );
  if (w) total += parseFloat(w.value) || 0;
});
console.log('Toplam:', total);
```

2. **Bilinen sorun: Validator otomatik düşürme** — bazı satırların değerleri ilk yazımda 0'a düşer (özellikle ilk birkaç fon). Toplam 100 değilse **eksik kalan satırları yeniden yaz**, ikinci pas at.

3. **Bilinen sorun: Aynı fon iki satırda** — eğer fon hem mevcut allokasyonda var hem de BEFAS'tan yeni eklendiyse, 2 satıra düşer. Birini sıfırla.

4. **Screenshot ile görsel doğrula** — JS başarılı dese de slider UI güncellenmemiş olabilir. Ekrana bak.

## Tamam → kullanıcıya teslim

Doğrulama tamamlandıktan sonra:

```
✅ Sözleşme {numara} sepeti hazır, toplam %100, [N] fon.
Şimdi sayfanın altındaki **"Tamam"** butonuna sen bas.
Onay/SMS ekranı gelirse onayla. İşlem 2-7 iş günü içinde gerçekleşir.
```

**Kullanıcı "Tamam"a bastıktan sonra**:
- SMS doğrulama isterse kullanıcı yapar
- Sayfa "Talep alındı" mesajı gösterir
- O sözleşme için kalan değişiklik hakkı 1 azalmış olur

Kalan hakkı `Kalan Hakkınız : N` text'inden okuyabilirsin (regex: `/Kalan Hakk[ıi]n[ıi]z\s*:\s*\d+/`).

## Birden fazla sözleşme

Birinci sözleşmeyi onayladıktan sonra:
1. Ana sayfaya geri dön (`/Views/BireyselEmeklilik.aspx`)
2. İkinci sözleşmeye tıkla (pasta grafik o sözleşmeyi göstermeli)
3. İşlemler → Fon Dağılım Değişikliği → akışı tekrarla
4. ⚠️ Bazen sözleşme seçimi geçmiyor — sayfa yenile veya ana sayfaya dön

Eğer bir sözleşme onayı sırasında **otomatik logout** olursan (oturum sona ererse), kullanıcının tekrar girmesini iste.

## Bilinen tuhaflıklar (THE-spesifik)

- 18 yaş altı kumbara hesabında bazı katılım fonları (AGB - Büyüme Katılım Değişken) sadece o plan'da var
- Bazı fonlar BEFAS'a eklenince hem THE listesinde 0% hem BEFAS'tan eklenen 12% olarak 2 satır olabilir
- Validator bazen TVH/YZD gibi fonları ilk pas'ta düşürüyor; ikinci pas attığında düzeliyor
- Modal'lar bazen scroll dışında kaldığı için "Tamam" butonu görünmez — scroll yap
- Pasta grafik load timing: Yüksek katılım sayısında pasta grafik 5+ saniye yüklenebilir, kullanıcı sözleşmeye tıkladıktan sonra hesabın açıldığını grafiğin yüklenmesinden anla

## Hata kurtarma (genel kurallar)

Bu adapter'ı kullanırken oluşabilecek hatalar için **tek otoriter playbook** `references/error_recovery.md`. THE-spesifik notlar:

| Senaryo (error_recovery.md) | THE'de tipik tezahür |
|---|---|
| Senaryo 1 (oturum timeout) | 20 dakika hareketsizlik → otomatik logout, Login.aspx'e atar |
| Senaryo 2 (validator) | TVH ve YZD ilk pas'ta düşer, ikinci pas çözer (yukarıda detay) |
| Senaryo 3 (BEFAS modal) | Bilgilendirme modal'ı bazen scroll dışında — pencere boyutu küçükse scroll up |
| Senaryo 5 (kalan hak 0) | "Kalan Hakkınız: 0" satırı sayfa altında kırmızı görünür |
| Senaryo 6 (çift satır) | THE listede 0%, BEFAS satırında hedef yüzde — eski 0 satırı dokunma, yeni satıra yaz |
| Senaryo 9 ("Tamam" hata) | "İşlem alınamadı" üst banda yeşil/kırmızı bilgi kutusu olarak çıkar |

## Pay fiyatı çekme (gerçekleşmiş getiri için)

Aylık revize sırasında her fonun **talep tarihindeki pay fiyatını** kayda almak gerekiyor (`current_basket.md` doldurulurken). Türkiye Hayat'ta:

1. **Fon Bilgileri** sayfası: `/Views/BireyselEmeklilik-FonBilgileri.aspx?fonkod={KOD}`
2. Sayfada "Pay Fiyatı" bölümünde günlük pay fiyatı tablosu var
3. JS ile son fiyatı çekmek:

```js
const priceCell = document.querySelector('#ContentPlaceHolder1_lblPayFiyati');
const price = priceCell ? parseFloat(priceCell.innerText.replace(',', '.')) : null;
console.log('Pay fiyatı:', price);
```

4. Eğer eSube anlık fiyat vermiyorsa (BEFAS fonları için bazen) TEFAS'tan al:
   `https://www.tefas.gov.tr/FonAnaSayfa.aspx?FonKod={KOD}`

## Bir sonraki adım

Yüzdeler girildikten sonra:
1. Her fonun talep tarihindeki pay fiyatını çek ve `current_basket.md`'ye yaz
2. Kullanıcıya teslim et
3. "Tamam"a basmasını bekle
4. SMS doğrulama tamamlandıktan sonra "Talep alındı" ekranını gör
5. history yaz, current_basket.md'yi finalize et

Hata oluşursa: `references/error_recovery.md`'deki ilgili senaryoyu uygula, sessiz kurtarma yapma.
