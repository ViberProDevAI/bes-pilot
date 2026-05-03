# Provider Stub — Yeni Kurum Adapter Şablonu

Bu template, henüz tam test edilmemiş BES kurumları için kullanılır. Kullanıcının kurumu için tam adapter yoksa bu template'i takip et — kullanıcının ekran üzerinden yönlendirip ilerlersin, eSube'nin yapısını "live" keşfedersin.

## Temel akış (her BES eSube'sinde benzer)

Tüm BES kurumları SPK/EGM regülasyonuna uyduğu için akış benzerdir:

1. Login (kullanıcı adı + şifre + SMS — **kullanıcı yapar**)
2. Sözleşme listesi → bir sözleşme seç
3. Fon işlemleri / Fon dağılım değişikliği menüsü
4. Mevcut sepet + radio (mevcut + gelecek / sadece gelecek / sadece mevcut)
5. Fon listesi (THE'nin kendi fonları + BEFAS açılırsa diğer kurucular)
6. Yüzdeleri gir
7. Toplam = 100 doğrula
8. Onay → SMS doğrulama → talep gerçekleşti

## Bilinmeyen UI ile çalışma stratejisi

Eğer bu kurumun adapter'ı yoksa kullanıcıya:

```
{Kurum} eSube'si için tam test edilmiş bir adapter henüz yok. 
Birlikte adım adım keşfedelim:

1. Sen tarayıcıda eSube'ye girince bana söyle
2. Ben her ekranda screenshot alır, ne yapacağımı seninle konuşurum
3. Bittiğinde bu kurumun adapter dosyasını yazarız ki bir sonraki ay 
   otomatik çalışsın
```

Sonra her ekranda şunları yap:

1. **Screenshot al** ve butonları/ menüleri tanımla
2. Kullanıcıya "şuraya tıklayalım mı?" diye sor (özellikle finansal aksiyonlar için)
3. Form alanlarını JS ile incelet (input türleri, IDs, ne yapıyorlar)
4. Dağılım değişikliği ekranına geldiğinde:
   - Fon kodları nasıl listelenmiş?
   - Yüzde girme mekanizması nasıl (slider mı, sayı kutusu mu, dropdown mu)?
   - Toplam kontrol UI'ı nerede?
   - "Onayla" butonu nerede?

## Yeni adapter yazma

Kullanıcıyla bir kez tüm akışı yaptıktan sonra **bu kurumun adapter'ını yaz**:

1. `references/providers/{kurum_kisa_adi}.md` dosyası oluştur
2. `turkiye_hayat.md` formatını kullan — özellikle şu bölümleri kapsa:
   - Login akışı + URL'ler
   - Hesap yapısı (sözleşme listesi, çoklu sözleşme davranışı)
   - Fon dağılım değişikliği akışı (sayfa yapısı, JS snippet'leri)
   - BEFAS akışı (varsa)
   - Yüzde girme + doğrulama (validator davranışları)
   - **Pay fiyatı çekme** — gerçek getiri hesabı için kritik (`current_basket.md`'ye yazılacak)
   - Bilinen tuhaflıklar
   - Hata kurtarma (`error_recovery.md` Senaryolarıyla eşleşme)
3. Test edilmiş JS snippet'leri (yüzde girme, fon işaretleme vs.) yaz
4. Bilinen validator davranışlarını not et (THE'nin TVH/YZD pattern'i gibi kurum-spesifik durumlar)
5. URL'leri, sayfa isimlerini, element ID'lerini kayıt altına al

Bir sonraki ay/kullanıcıda bu adapter direkt çalışacak. Ortak hata kurtarma `references/error_recovery.md`'de — kurum adapter'ı sadece kuruma özel sapmaları (eğer varsa) belgeler.

## Bilinen kurumlar için ipuçları

- **Anadolu Hayat**: anadoluhayat.com.tr → "Online İşlemler" → BES portali
- **Garanti Emeklilik**: garantibbvaemeklilik.com.tr (Garanti BBVA mobil de mümkün)
- **Allianz Yaşam**: allianzyasam.com.tr
- **Agesa**: agesa.com.tr → "Online Şube"
- **HDI Fiba**: hdifibaemeklilik.com.tr
- **NN Hayat**: nnhayat.com.tr (artık AvivaSA'dan ayrı)
- **AvivaSA**: avivasa.com.tr
- **Vakıf Emeklilik**: vakifemeklilik.com.tr

Çoğunda BEFAS açıktır (regülasyon zorunluluğu). BEFAS bilgilendirme onayı her kurumda benzer şekilde işliyor.

## Adapter oluşturulduktan sonra

PR olarak bu repo'ya katkı: yeni adapter dosyası + README'de "test edilmiş kurumlar" listesine ekle.
