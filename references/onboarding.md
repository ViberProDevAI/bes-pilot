# Onboarding — 5 Soruda Profil Çıkarımı

Yeni kullanıcı için 5 soruluk hızlı profil. Hedef: kullanıcıyı 2 dakikada tanı, defansif/dengeli/agresif risk profilinden birine yerleştir, BES kurumu/sözleşme bilgilerini al.

## Temel ilke: Doğum tarihi, "yaş" değil

Kullanıcının **doğum tarihini** sor, "kaç yaşındasın" değil. Sebep: skill yıllarca aynı kullanıcı için çalışacak. "Yaş: 32" ifadesi 1 yıl sonra paslı olur, kullanıcı manuel "yaşım değişti" demeli. Doğum tarihinden yaş her revizede otomatik hesaplanır → yaş eşik geçişleri (40, 55) zamanında yakalanır.

Aynı mantık aylık katkı ve birikim için de geçerli: tarih damgası tut, çürümeyi say.

## Soru sırası ve mantığı

AskUserQuestion tool'u varsa onu kullan, daha temiz UX. Yoksa düz sohbetle sor — ama hepsini tek mesajda boğma; 1-2 soru sor, cevap al, devam et.

### Soru 1 — Doğum tarihi + Hedef Emeklilik Yaşı (Vade)

```
Doğum tarihin nedir (gün/ay/yıl)? BES'i emeklilikte kaç yaşında bozdurmayı düşünüyorsun?
```

**Neden önemli**: Vade = uzun mu kısa mı? Vade uzunsa volatilite tolere edilebilir (agresife eğilim), kısaysa korunmacı sermaye gerek.

**Hesaplama**:
- Bugünün tarihi - doğum tarihi = mevcut yaş (yıl)
- Hedef emeklilik yaşı - mevcut yaş = vade (yıl)

**Çıkarım kuralları (vade)**:
- Vade ≥ 20 yıl → "uzun" (agresife eğilim)
- 10-20 yıl arası → "orta"
- < 10 yıl → "kısa" (defansife eğilim)

**Hedef emeklilik tarihini de türet ve profile.md'ye yaz** — kullanıcının fikir değiştirmesi mümkün, ama 1 yıllık takvim için ihtiyaç var.

### Soru 2 — Aylık Düzenli Katkı + Mevcut Birikim Tutarı

```
Aylık ne kadar BES'e koyuyorsun? Şu ana kadar BES'te yaklaşık ne kadar birikmiş (devlet katkısı dahil)?
```

**Neden önemli**: Birikim tutarı = risk için "elini ne kadar yakacak". Aylık katkı = ortalamayla maliyetlendirme avantajı (DCA).

**Çıkarım kuralları**:
- Aylık katkı ≥ aylık net gelirin %10'u → DCA güçlü, agresif daha tolere edilebilir
- Birikim tutarı kullanıcının yıllık geliri kadarsa veya fazlaysa → "ciddi para", riske dikkat
- Birikim tutarı küçükse (< 50K TL) → "alıştırma", agresif tolere edilebilir

**Tarih damgası**: profile.md'de "Aylık katkı son güncelleme: 2026-05-03" şeklinde tut. Kullanıcı 6 ay sonra "gelirim arttı" demese de, skill aylık revizede "9 aydır katkı tutarı doğrulanmadı, hala doğru mu?" diye yumuşakça sorabilir.

### Soru 3 — Kayıp Toleransı (psikolojik)

```
Diyelim ki BES portföyün tek bir ayda %15 düştü, gazete manşetlerinde "kriz" yazıyor. İlk tepkin ne olur?
A) Hemen panikle satışa çık, daha defansife geç (kaybı durdur)
B) Bekle, ama uykum kaçar; 1-2 ay sonra hala düşükse değiştiririm
C) Düşüşte yeni para koyarım, fırsat bilirim
```

**Çıkarım kuralları**:
- A → defansife eğilim, **agresif override yasak** (bkz. risk_profile.md)
- B → orta/dengeli
- C → agresife eğilim

Bu, **risk algısı** sorusu — yaş ve vade ne olursa olsun, kullanıcı C cevabını veremiyorsa agresif sepet yapmak hatadır (uyku kaçırırsa zaten erken bozdurur, en kötü sonuç).

### Soru 4 — Hedef ve Beklenti

```
BES'ten beklentin ne? (Bir tanesini seç)
A) Sadece devlet katkısını alıp enflasyon kadar koruyayım yeter
B) Reel olarak (enflasyon üstü) makul bir getiri (yıllık enflasyon + %5-10)
C) Agresif büyüme — emekli olduğumda iyi para olsun, oynaklığa razıyım
```

**Çıkarım kuralları**:
- A → defansif
- B → dengeli
- C → agresif

### Soru 5 — Hangi BES kurumunda(lar)? Kaç sözleşme?

```
Hangi BES kurumundasın? (Türkiye Hayat / Anadolu Hayat / Garanti / Allianz / Agesa / HDI Fiba / NN / AvivaSA / Vakıf / diğer)
Kaç tane aktif sözleşmen var? Sözleşmelerini açtığın yılı hatırlıyor musun?
```

**Neden önemli**: 
- Doğru `references/providers/{kurum}.md` adapter'ını yüklemek için
- Birden fazla sözleşme varsa her birini ayrı yöneteceğiz
- Sözleşme açılış yılı, **fon gider iadesi** zamanlaması için kritik (6. yıldan itibaren başlar — Genelge 2026/1, BES Yönetmeliği Madde 22/A)

**Bonus soru** (kullanıcıya bağlı): Sözleşmelerden biri 18 yaş altı kumbara mı? (varsa ona ekstra dikkat → agresif olsa bile kullanıcı onayı şart)

## Risk Profili Hesabı

5 sorunun cevaplarına göre puan ver:

| Soru | A cevabı puan | B cevabı puan | C cevabı puan |
|---|---|---|---|
| 1 (vade) | < 10 yıl: -2 | 10-20: 0 | ≥ 20: +2 |
| 2 (DCA gücü) | Düşük: -1 | Orta: 0 | Yüksek: +1 |
| 3 (kayıp tepkisi) | A: -3 | B: 0 | C: +3 |
| 4 (hedef) | A: -2 | B: 0 | C: +2 |

**Toplam puan**:
- ≤ -3 → **DEFANSİF**
- -2 ile +2 arası → **DENGELİ**
- ≥ +3 → **AGRESİF**

⚠️ **Override kuralı (sert)**: Soru 3'te A diyen kullanıcı asla AGRESİF sepete yönlendirilmez, başka cevaplar ne olursa olsun. Çünkü kayıp toleransı düşükse bağımsız değişken bu — kullanıcı paniklerse zaten erken bozdurur.

> Eşik puanları (-3, +3) **stilize**: davranış finansı literatüründe risk anketleri benzer kalıpta puan verir, ama bizim eşiklerimiz **klinik veriyle kalibre edilmedi**. Aylık revizede kullanıcı "sepet bana fazla agresif geliyor" derse eşikleri kullanıcı bazlı tilt et — bu profile.md'deki "Override geçmişi" tablosuna geçer.

## Profili kaydet

`memory/users/{kısa_ad}/profile.md`'ye yaz. `memory/_template/profile.md`'i kopyala başlangıç noktası olarak. Tüm `{...}` placeholder'larını kullanıcı cevaplarıyla doldur:

```markdown
# {Tam Ad} — BES Profili

**Son güncelleme**: {YYYY-MM-DD}
**Şema sürümü**: 2

## Demografi
- **Doğum tarihi**: {YYYY-MM-DD}
- Hedef emeklilik yaşı: {N}
- Hedef emeklilik tarihi: {YYYY-MM-DD}  ← doğum tarihi + hedef yaştan türetilir

## Finansal
- Aylık katkı (TL): {N}
- Aylık katkı son güncelleme: {YYYY-MM-DD}
- Mevcut toplam birikim (devlet katkısı dahil, TL): {N}
- Birikim son güncelleme: {YYYY-MM-DD}
- DCA gücü: {düşük | orta | yüksek}

## Risk profili
- Soru 1 puanı: {-2 | 0 | +2} (vade {N} yıl)
- Soru 2 puanı: {-1 | 0 | +1}
- Soru 3 cevabı + puan: {A: -3 | B: 0 | C: +3}
- Soru 4 cevabı + puan: {A: -2 | B: 0 | C: +2}
- **Toplam puan**: {SUM} → **{DEFANSİF | DENGELİ | AGRESİF}**
- Kayıp toleransı override aktif mi: {evet | hayır}
- Profil son hesaplama: {YYYY-MM-DD}

## BES sözleşmeleri
| # | Sözleşme No | Kurum | Plan adı | Kim için | Açılış tarihi | BEFAS aktif | Notlar |
|---|---|---|---|---|---|---|---|
| 1 | {XXXXXXXXX} | {Kurum} | {Plan} | {kendi/eş/çocuk/...} | {YYYY-MM-DD} | {evet/hayır} | {opsiyonel} |
| 2 | ... | | | | | | |

## Yıllık takvim
- Hak yılı (en eski sözleşme): {YYYY-MM-DD} → her sözleşme yıldönümünde fon gider iadesi (6. yıl ve sonrası)
- Fon değişiklik hakkı: 12/yıl (Genelge 2026/1; takvim yılı bazlı, 1 Ocak'ta sıfırlanır)
- Bir sonraki revize: {YYYY-MM-DD}
- Yıl içi kullanılan hak: 0/12

## Otomatik sürükleme — yaş eşik haritası
[template'den aynen — risk_profile.md'deki yaş tablosu]

## Kullanıcı override geçmişi
(boş — henüz kayıt yok)

## Notlar
- {kullanıcının özel istek/durumlarını buraya not düş — örn. "çocuk hesabında uzun vade, agresif tolere ediliyor" gibi}
```

> Üstteki blokta `{Tam Ad}`, `{YYYY-MM-DD}`, `{N}`, `{XXXXXXXXX}` gibi süslü-parantezli alanlar **şablon yer tutucularıdır** — gerçek kullanıcı verisini onları değiştirerek yazarsın. Dosya hiçbir aşamada başka birinin verisini içermemeli.

## Sonraki adım

Profil yazıldıktan sonra `references/risk_profile.md` → temel allokasyon → `references/fund_research.md` → güncel piyasa → `references/basket_construction.md` → final sepet.
