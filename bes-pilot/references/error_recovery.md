# eSube Hata Kurtarma — Genel Playbook

eSube otomasyonunda yapısal başarısızlık modları sınırlı sayıda. Bu playbook her birini ele alır: sebep, tespit, kurtarma adımları, tırmandırma. Provider-spesifik adımlar `references/providers/{kurum}.md`'de.

## Felsefe

**Sessiz kurtarma yasak**. Her başarısızlık kullanıcıya görünür olmalı, log'a yazılmalı, history dosyasına geçmeli. Sebep:
- Kullanıcı her zaman ne olduğunu bilmeli (güven)
- Aynı hata tekrar ederse paterni bulabilelim (bakım)
- Skill'i geliştirenler hangi hataların yaygın olduğunu görsün (kalite döngüsü)

**Kullanıcı tarafında düzeltilebilir vs. düzeltilemez ayrımı**:
- Düzeltilebilir (kullanıcı yapar): tekrar login, sayfa yenile, popup kapatma, beklemek
- Düzeltilemez (kurum yapar): site bakımda, hesap bloklu, sözleşme dondurulmuş — bu durumda skill kullanıcıya açıkla, beklemeyi öner, history'ye yaz

## Senaryo 1: Oturum zaman aşımı (timeout)

**Belirti**: Tipik olarak 15-30 dakika hareketsizlik sonrası. Sayfa otomatik login'e atar veya "Oturumunuz sona erdi" mesajı gösterir.

**Tespit**:
- Sayfa URL'si `/Login.aspx` veya benzeri auth sayfasına döndü
- Body'de "oturumunuz sona erdi", "session expired", "tekrar giriş yapın" benzeri metin
- API çağrıları 401/302 dönüyor

**Kurtarma**:

```
1. Mevcut state'i kaydet:
   - Hangi sözleşmedeydik?
   - Hangi adımdaydık? (BEFAS açma, fon ekleme, yüzde girme, doğrulama, "Tamam" bekliyor)
   - Yüzdeler local'de saklı mı? (varsa)
   
2. Kullanıcıya bildir:
   "Oturum kapandı. Sen tekrar login olunca kaldığım yerden devam ederim:
    - Sözleşme: GBB XXXXXXXXX
    - Adım: BEFAS fon yüzdeleri girilmiş ama henüz Tamam'a basılmamıştı
    - Yüzdeler: TVH 13, TBJ 13, ..."
    
3. Kullanıcı tekrar login olduktan sonra:
   - Doğru sözleşmeyi seç
   - Fon Dağılım Değişikliği sayfasına git
   - "Devam eden işlem var" uyarısını kontrol et (önceki yarım girişimde bir talep verilmiş olabilir)
   - Yoksa: yüzdeleri tekrar gir, doğrula, "Tamam"a kullanıcı bassın
   - Varsa: yeni değişiklik yapılamaz, kullanıcıya bekle de
```

**Önleme**: 10 dakikadan uzun sürecek otomasyonlarda her 5 dakikada bir sayfa yenile veya bir tıklama yap (heartbeat). Cowork mode'da kullanıcı arada başka iş yapıyorsa sayfa hareketsiz kalabilir.

## Senaryo 2: Validator yüzdeleri tutturmaz (Türkiye Hayat'ta yaygın)

**Belirti**: JS ile yüzdeleri girdikten sonra toplam 100 değil. Bazı satırlar 0'a düşmüş, bazıları beklenen değerden farklı.

**Tespit**: 
```js
let total = 0;
document.querySelectorAll('table tr').forEach(row => {
  // ... toplam hesapla
});
console.log('Toplam:', total);
// Eğer total !== 100 → validator devreye girdi
```

**Kurtarma — kademeli pas**:

```
İlk pas: Tüm yüzdeleri tek seferde gir
↓
Toplam kontrol et
↓ (≠ 100)
İkinci pas: SADECE 0'a düşmüş veya yanlış olan satırları yeniden gir
↓
Toplam kontrol et
↓ (≠ 100)
Üçüncü pas (nadir): Tek tek satır satır, her birinde event tetikle, beklemek için 200ms ara
↓
Toplam kontrol et
↓ (hala ≠ 100)
Manuel devir: Kullanıcıya açıkla, 
"Validator otomatik girişi tutturmuyor (3 pas denedim). 
 Şu anda toplam: 97%. Eksik fon: TVH (girmesi gereken 13, girdi 10).
 TVH satırını sen elle 13 yapar mısın?"
```

**Tipik nedenler**:
- Türkiye Hayat: bazı fonlar (özellikle TVH, YZD) ilk pas'ta düşürülür
- Sayfa AJAX postback'i bekliyor — değer set etmeden önce postback bitmemiş
- IonRangeSlider widget update event'i kabul etmiyor

**Önleme**: Provider adapter'ında bilinen sorunlu fonlar listesi tut, onları sona bırak veya iki kez gir.

## Senaryo 3: BEFAS modal'ı açılmıyor / popup blokere takılıyor

**Belirti**: "BEFAS Fonları İçin Tıklayınız" linkine basıldı ama modal görünmüyor. Konsol'da JS hatası olabilir.

**Tespit**:
- Tıkladıktan 3-5 saniye sonra ekranda yeni element yok
- Console'da hata: undefined function, jQuery missing, popup blocked

**Kurtarma**:
```
1. Sayfa yenile, tekrar dene
2. Tarayıcı popup blokerini kontrol et — kullanıcıya sor
3. Direkt URL ile geç (provider adapter'ında doğru URL'i biliyorsan):
   /Views/BireyselEmeklilik-Islemlerim-Befas-Fonlari.aspx
4. Hala olmuyorsa: BEFAS'ı atla, sadece kendi kurumun fonlarından sepet kur
   "BEFAS açılamadı (modal sorunu). Bu ay kendi kurumun fonlarından sepet 
    kuralım, getiri biraz düşer ama uygulanabilir."
```

## Senaryo 4: Sözleşme dondurulmuş / atıl

**Belirti**: Sözleşmeye tıkladığında "Bu sözleşme aktif değil" veya "Katkı payı ödenmemiş" tarzı uyarı.

**Tespit**:
- Sözleşme listesinde sözleşme görünüyor ama detay açılmıyor
- "Pasif sözleşme" / "Atıl sözleşme" / "İşlem yapılamaz" mesajı

**Kurtarma**:
```
1. Kullanıcıya açıkla:
   "Sözleşme {No} aktif değil. Aşağıdakilerden biri olabilir:
    - Katkı payı ödemesi son 6+ ayda yok
    - Sözleşme transfer/birleştirme süreci
    - Müşteri talebiyle dondurulmuş
   Bu sözleşmede fon değişikliği yapamayız."

2. Çoklu sözleşme varsa: diğer sözleşmelere geç, onları yönet
3. Tek sözleşme varsa: kullanıcıya kurum çağrı merkeziyle iletişime geçmesini öner
4. profile.md'de bu sözleşmeyi "atıl: YYYY-MM-DD itibarıyla" olarak işaretle
```

## Senaryo 5: Kalan değişiklik hakkı 0

**Belirti**: Sayfada "Kalan Hakkınız: 0" görünüyor. Yüzde değişikliği yapılsa da "Tamam"a basınca hata.

**Tespit**:
- `Kalan Hakkınız: 0` text'i (regex: `/Kalan Hakk[ıi]n[ıi]z\s*:\s*0/`)
- "Tamam"a basınca "Yıllık fon değişiklik hakkınız doldu" mesajı

**Kurtarma**:
```
Bu durum normalde önlenebilir — skill yıl içi haritayı tutuyorsa 12'ye 
yaklaştığında kullanıcıya "kalan haklarını dikkatli kullan" diye uyarmalı.

Yine de sıfıra düştüyse:
1. Kullanıcıya açıkla:
   "Yıllık 12 fon değişiklik hakkın doldu (Genelge 2026/1 Madde 8/Y). 
    Bir sonraki sıfırlama: {bir sonraki 1 Ocak}. 
    Şu anki sepetinle devam edeceğiz."
    
2. Aylık takvimi 1 Ocak'a göre kur — Ocak 1 sonrası yeni hak
3. Bu durumda manuel `/bes-revize` çağrılarında uyar:
   "Hak yok, bu ay sepet değişikliği yapamayız."
4. profile.md "Yıllık takvim" bölümünü güncelle: "12/12 dolu, sıfırlama: 2027-01-01"
```

## Senaryo 6: Aynı fon iki satırda (BEFAS sonrası)

**Belirti**: Fon listesinde aynı fon kodu iki kez görünüyor. Bir kez kendi kurum fonu olarak (mevcut allokasyonda), bir kez BEFAS'tan eklendiği için.

**Tespit**: 
```js
const codes = [];
document.querySelectorAll('table tr td:first-child').forEach(td => {
  const code = td.innerText.trim();
  if (code.length === 3) codes.push(code);
});
const dupes = codes.filter((c, i) => codes.indexOf(c) !== i);
console.log('Tekrarlayan:', dupes);
```

**Kurtarma**:
```
1. Hangi satır "kullanılacak" karar ver:
   - Genelde BEFAS'tan gelen satır kullanılır (taze, daha güncel meta)
   - Diğer satırı 0'a düşür
2. Yüzde girerken sadece bir satıra hedef yüzdeyi ata
3. Toplam doğrulamada her iki satırı da gör — eski satır 0 mı, yeni satır hedef mi?
```

## Senaryo 7: Kurum sitesi bakımda

**Belirti**: HTTP 503, "Bakım çalışması", veya site yavaşlığı (timeout).

**Tespit**:
- Login sayfası açılmıyor veya çok yavaş (>30 sn)
- HTTP error 5xx
- Site içeriği "Bakım çalışmaları nedeniyle..."

**Kurtarma**:
```
1. Kullanıcıya açıkla:
   "{Kurum} eSube şu anda erişilebilir değil. 1-2 saat sonra tekrar deneyelim mi?"

2. Skill, scheduled task'ı tekrar tetiklemek için 4 saat sonrasına 
   bir hatırlatma çalıştırabilir (scheduled-tasks MCP varsa).

3. Eğer 24 saat içinde site açılmazsa: kullanıcıya uyarı, 
   "Site uzun süre kapalı. Manuel olarak EGM'ye danış veya sosyal medyada bakım anonsu kontrol et."

4. history dosyasında not düş: bu ayın revizesi gecikti, sebep: site bakımda
```

## Senaryo 8: SMS doğrulama gelmiyor

**Belirti**: Kullanıcı "Tamam"a bastı, SMS bekleniyor ama gelmiyor (5+ dakika).

**Tespit**: Skill bu durumu doğrudan bilemez (kullanıcının telefonuna erişimi yok). Kullanıcının "SMS gelmedi" demesi.

**Kurtarma**:
```
Kullanıcıya öneriler:
1. "Tekrar gönder" linkine bas (varsa)
2. SPAM'ı kontrol et
3. Kurum çağrı merkezini ara, kayıtlı telefon numarasını doğrula
4. eSube'den tek seferlik OTP yerine mobil uygulama doğrulamasını dene (varsa)

Bu durumda talep eSube'de yarıda kalır. Genelde kurum 30 dk sonra 
otomatik olarak iptal eder. Sonraki gün sıfırdan tekrar dene.
```

## Senaryo 9: "Tamam"a basıldı ama hata mesajı

**Belirti**: Kullanıcı "Tamam"a bastıktan sonra ekran "İşlem alınamadı" veya benzer hata gösteriyor.

**Olası nedenler**:
- Yüzde toplamı 100 değil (validator pas'ında düzgün çalışmamış)
- Sözleşme durumu son anda değişti (atıl, beklemede)
- Backend doğrulaması başarısız (eksik bilgi, format hatası)

**Kurtarma**:
```
1. Hata mesajını oku ve kullanıcıyla paylaş (şeffaf ol)
2. Sayfayı yenile, durumu kontrol et — talep gerçekten alınmamış mı?
3. eSube'de "İşlem geçmişi" varsa son talep durumunu kontrol et
4. Eğer talep hiç düşmediyse: yüzdeleri tekrar gir, baştan dene
5. Eğer talep düştüyse ama "kabul edilmedi" durumdaysa: 
   - Kullanıcıdan kurum çağrı merkezini aramasını iste
   - Bir sonraki gün sıfırdan tekrar dene
```

## Tüm senaryolar için ortak kurallar

1. **Hatayı history'ye yaz**: Hangi senaryo, ne zaman, kullanıcı tarafında ne yaptı, çözüm ne oldu
2. **Yarım kalmış işlemi takip et**: "Tamam"a basılmamış bir değişiklik kayıtlara `current_basket.md`'ye **YAZILMAMALIDIR** — ancak gerçekleşme onayından sonra yazılır
3. **Yıl içi pattern göz önünde tut**: Aynı kullanıcıda aynı hata 2+ kere olduysa profile.md'ye "Bilinen sorunlar" notu düş, ileri revize öncesinde kontrol et
4. **Kullanıcıyı yorma**: Her hatada baştan sorma — özellikle kullanıcı bilgisi (sözleşme no, profil) bilinen şeyler. "Sözleşme {bilinen no} için tekrar deniyorum" de, kullanıcının yeni veri girmesini gerektirme

## Yeni hata türü ortaya çıkarsa

Bu playbook'ta olmayan bir durumla karşılaşırsan:
1. Kullanıcıyla konuş, ne olduğunu net anla
2. Çözüm bulduktan sonra **bu dosyaya yeni senaryo ekle** (Senaryo 10, 11, ...)
3. history dosyasına detaylı yaz: HTML hata mesajı, console log, ekran görüntüsü açıklaması
4. Bir sonraki kullanıcıda aynı hata olduğunda playbook hazır olsun
