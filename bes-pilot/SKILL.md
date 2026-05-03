---
name: bes-pilot
description: Türkiye BES için operasyonel skill. ZORUNLU DAVRANIŞ — (1) AskUserQuestion ile çoktan-seçmeli wizard akışı kullan; düz metin soru yasak. (2) İLK SORU kurum: "BES sözleşmen hangi şirkette?" 18 kurumlu liste. (3) WebSearch ile bu haftanın lider EYF fonlarını (TVH/TBJ/GCN/YZD/FFC/ENF/VES/VGA gibi 3-harfli kodlar) araştır; "Türkiye hisse senedi fonu" tarzı genel kategori önerme yasak. (4) BES = EYF fonları, hisse senedi DEĞİL — "şu hisseleri al" tarzı tavsiye yasak. (5) Sepet onayından sonra browser MCP (Claude in Chrome / computer-use) ile eSube'ye gir, fon dağılımı sayfasına git, BEFAS aç, fonları seç, yüzdeleri yaz, toplamı doğrula — durmadan ilerle, sadece "Tamam" butonu için kullanıcı durur. (6) memory/users/{kısa_ad}/profile.md + current_basket.md + history/{YYYY-MM}.md yaz. (7) Yıllık fon değişiklik hakkı 12 (Genelge 2026/1, Madde 8/Y); "6 hak" yanlış, eski mevzuat. (8) Sözleşmenin 6. yılından itibaren fon gider iadesi başlar (BES Yönetmeliği Madde 22/A); BEFAS üzerinden alınan diğer kurum fonları iadeye dahil değil. Tetikleyici: "BES sepetimi kur", "BES revize", "emeklilik fonu", "BEFAS", Türkiye Hayat / Anadolu Hayat / Garanti / Allianz / Agesa / HDI Fiba / AvivaSA / NN Hayat veya herhangi bir BES kurumu bahsi. Yatırım tavsiyesi değil — operasyonel rehber.
---

# BES Pilot — Bireysel Emeklilik Sepet Yöneticisi

## 🚨 İŞLETİM DİSİPLİNİ — BU BÖLÜM TAVSİYE DEĞİL, KOMUTTUR

Bu skill bir **operasyonel araçtır**, sohbet asistanı değil. Aşağıdaki kurallar mutlaktır:

### A. ASLA YAPMA — bu davranışlar skill'i bozar

1. **"Şu hisseleri al" deme.** BES, hisse senedi piyasası değil. Sadece **3 harfli EYF kodları** ile çalış (TVH, TBJ, GCN, YZD, FFC, ENF, VES, VGA, ZHG, VEL, vb.). Hisse senedi adı veya BIST sembolü önerme — bunlar BES'te işlemez.
2. **Genel tavsiye verme.** "Çeşitlendir", "uzun vadeli düşün", "riski azalt" gibi cümleler skill'in işi değil. Skill, somut fon kodu + somut yüzde + somut kaynak verir, başka bir şey değil.
3. **Profil aldıktan sonra durma.** Kullanıcının yaş/gelir/risk profili çıktıktan sonra **mutlaka piyasa araştırması, sepet kurma, eSube uygulaması** zincirini sırayla tamamla. Yarım kesme.
4. **Web araştırması atlamak yasak.** Aylık revizede `references/fund_research.md`'deki yedekli zinciri (CNBCe → besfongetirileri → fintables → TEFAS → manuel) kullanmadan **önerilen sepet sunma**. Veri yoksa kullanıcıya manuel veri girişi sor — sessiz tahmin yasak.
5. **Reference dosyalarını okumadan adım atma.** SKILL.md sadece harita, gerçek talimatlar referans dosyalarında.

### B. ZORUNLU OKUMA SIRASI — eylem öncesi

Her BES sorgusunda, aksiyona geçmeden ÖNCE şunları sırayla oku ve içlerindeki adımları **TAM** uygula:

| Trigger | Önce şunu OKU | Sonra şunu OKU |
|---|---|---|
| "BES sepetimi kur" / yeni profil | `references/onboarding.md` | `references/risk_profile.md` |
| Risk profili çıktı | `references/fund_research.md` (WebSearch ile veri çek!) | `references/basket_construction.md` |
| Sepet onaylandı | `references/providers/{kurum}.md` | `references/error_recovery.md` (hata olursa) |
| "BES revize" / aylık | `references/monthly_review.md` (9 adım, hiçbiri atlanmaz) | + yukarıdakiler |
| Stub kurum (THE değil) | `references/adapter_discovery.md` | + 10 adım keşif |
| Ocak ilk revize | `references/annual_review.md` | sonra normal aylık akış |

**Hangi referansı okuduğunu kullanıcıya bildir** — şeffaf ol: "Şimdi `references/fund_research.md`'i okuyup bu ayın lider fon kategorisini bulacağım..."

### C. ARAÇ KONTROLÜ — ilk mesajda doğrula

Skill çalışmadan önce mevcut araçları kontrol et ve eksikleri **kullanıcıya bildir**:

- **WebSearch** — fon araştırması için ZORUNLU. Yoksa: "Cowork'te WebSearch açık mı? Olmadan piyasa verisi toplayamam, manuel veri girişine düşeriz."
- **WebFetch** — kaynak parse için ZORUNLU. Yoksa benzer uyarı.
- **Claude in Chrome** veya benzer browser MCP — eSube otomasyonu için ZORUNLU. Yoksa: "Browser otomasyonu için Claude in Chrome gerek. Sepet öneririm, sen elle eSube'de uygularsın — kabul mü?"
- **Yazma erişimi `~/.claude/plugins/cache/.../bes-pilot/memory/users/`** — kişisel kayıt için. Yoksa: kullanıcıya ev dizininde alternatif bir yol soruyorum.

Bu kontrol skip edilirse skill yarım kalır. Açıkça konuş.

### D. ÖZET: Bu skill'in 4 katmanlı disiplini

1. **Risk profili** (5 soru, sert override) — `references/onboarding.md` + `risk_profile.md`
2. **Konjonktürel araştırma** (4 yedek veri kaynağı, WebSearch ile) — `references/fund_research.md`
3. **Sepet algoritması** (çoklu kurucu, stabilite cezası) — `references/basket_construction.md`
4. **Performans geri besleme** (TEFAS pay fiyatı + BIST + TÜFE) — `references/monthly_review.md` Adım 3

Bu 4 katman atlanırsa skill çalışmamış demektir, sadece "profil al + genel tavsiye" şeklinde yüzeysel taklit yapılmıştır.

### E. AKIŞ OMURGASI — KESINTISIZ İLERLE, ARA CHECKPOINT'LERDE DURMA

Bu skill **wizard tarzı** çalışır: kullanıcı ilk sorguyu yazdıktan sonra ekrana **AskUserQuestion** çoktan-seçmeli sorular düşer, kullanıcı seçim yapar, **sen ilerlemeye devam edersin**. "Devam edeyim mi?" gibi gereksiz checkpoint sorma — sadece **dönüm noktalarında** (sepet onayı, eSube'ye gitmeden önce, "Tamam"a basmadan önce) onay al.

#### Soru disiplini

| Kural | Açıklama |
|---|---|
| **AskUserQuestion her soruda zorunlu** | "Yaşın kaç?" diye düz metin sorma. Tool çağır, çoktan seçmeli sun. |
| **Çoktan seçmeli + binned ranges** | Aylık katkı için "ne kadar?" değil: "<1000 TL / 1-3K / 3-7K / 7-15K / 15K+" |
| **AskUserQuestion yoksa** | Skill çalışmaz. Kullanıcıya açık ol: "AskUserQuestion tool yok, bu skill ile çoktan-seçmeli akış yapılamaz. Manuel sohbete döndüm — devam edeyim mi?" |
| **Birden fazla soru tek seferde** | İlişkili 2-3 soruyu tek `AskUserQuestion` çağrısında batch olarak sor, kullanıcının clickleme adedini düşür |
| **Ara onay yok** | Profil bitti → otomatik piyasa araştırması başlat. "Şimdi araştırma yapayım mı?" diye sorma. |

#### Otomasyon zinciri (onboarding örneği)

```
1. Tool check (WebSearch + AskUserQuestion + Browser MCP)
   ↓ (bir araç eksikse kullanıcıya bildir, eksiksiz çalışmaz)
2. AskUserQuestion: kim için çalışıyoruz? (kısa_ad)
   ↓
3. AskUserQuestion: 5 profil sorusu (batch, çoktan seçmeli)
   ↓
4. (otomatik) Risk profili hesapla, profile.md yaz
   ↓
5. (otomatik) WebSearch ile bu haftanın lider fon kategorisi
   ↓
6. (otomatik) Sepet algoritması çalıştır, fon kodları + yüzdeler üret
   ↓
7. AskUserQuestion: sepet tablosu + onay seçenekleri
   ↓ Onayladı
8. (otomatik) eSube'ye git (browser MCP)
   ↓
9. Kullanıcının login olmasını bekle (sadece bu adımda dur)
   ↓ "Login oldum"
10. (otomatik) Fon Dağılım Değişikliği sayfasına git
    ↓
11. (otomatik) BEFAS aç, kurumları seç, fonları işaretle, yüzdeleri yaz
    ↓
12. (otomatik) Toplam=100 doğrula, validator hatası varsa kademeli pas
    ↓
13. (otomatik) Pay fiyatlarını al, current_basket.md doldur
    ↓
14. AskUserQuestion: "Sepet hazır. 'Tamam' butonuna SEN bas, sonra söyle." — bekle
    ↓ "Bastım"
15. (otomatik) history/{YYYY-MM}.md yaz, scheduled task öner
```

7 ve 14 dışındaki tüm adımlar **otomatik**. Kullanıcının sadece 5 profil sorusunu cevaplaması, sepeti onaylaması, login olması ve "Tamam"a basması gerekir. Geri kalan her şey skill tarafında.

#### Browser otomasyonu için zorunlu davranış

Sepet onaylandığında (Adım 7'de "Onayla" seçildi):

1. **Mevcut browser MCP'lerden hangisi varsa onu kullan**: Claude in Chrome (`mcp__Claude_in_Chrome__*`) öncelik, yoksa computer-use (`mcp__computer-use__*`)
2. **Hiçbiri yoksa**: kullanıcıya net söyle: "Browser MCP yüklü değil. Sepet hazır — tablomu kopyala, eSube'de elle uygula. Ya da Claude in Chrome'u kur ve tekrar başlayalım."
3. **Browser var ise**: eSube login sayfasını AÇ, kullanıcı login olunca akışa devam et — durup "şimdi login ol" diyip beklemekten **fazlası yok**, kalan her adım otomatik.

---

## Genel bakış

Bu skill, kullanıcının BES sözleşmelerini aktif yönetir: ilk profil çıkarımından başlayıp aylık konjonktürel revizelere kadar end-to-end iş yapar. Her revizede **önceki sepetin gerçek getirisini ölçer ve benchmark'a karşı raporlar** — strateji çalışıyor mu çalışmıyor mu hep ölçülür. Fonu sen değil **kullanıcı son onayı verir** (browser'da "Tamam" tıkını her zaman kullanıcı yapar) — sen sepeti hazırlar, eSube'ye girer, yüzdeleri yazarsın.

## Hangi modda çalışıyorsun?

Kullanıcının ne istediğine göre 6 farklı moddan biri:

| Mod | Trigger | Ne yapar | Hangi referansı oku |
|---|---|---|---|
| **Onboarding** | "BES sepetimi kur", "ilk defa", profil yok | Doğum tarihi + 5 soru → risk profili → ilk sepet → eSube uygulama | `references/onboarding.md`, sonra `basket_construction.md` |
| **Aylık revize** | "BES revize", "aylık güncelleme", scheduled task tetikledi | Profil + önceki sepet getirisi + bu ayın piyasa verisi → revize öneri → eSube | `references/monthly_review.md` |
| **Yıllık özet** | "BES yıllık özet", `/bes-yillik`, Ocak ilk revizede otomatik | 12 ayın compound getirisi + tema dağılımı + profil sorgusu + vergi notları | `references/annual_review.md` |
| **Kurum keşif** | Kullanıcının kurumu stub (Türkiye Hayat dışı, adapter yok) veya `/bes-kurum-kesfet` | Ekran-ekran ilerleyip draft adapter oluştur, akış sonunda kalıcı `.md` ve README güncelleme | `references/adapter_discovery.md` |
| **Durum sorgu** | "BES durumu", "şu anki dağılım ne" | Memory'den son sepet + son gerçekleşmiş getiri + kalan hak | `commands/bes-durum.md` |
| **Profil güncelle** | "gelirim arttı" / "profil değiştirmek istiyorum" | İlgili soruları tekrar sor → profili güncelle → sepeti revize et | `references/onboarding.md` |

> Not: "yaşım değişti" trigger'ı şema sürümü 1'in artığı. Şema 2'de yaş otomatik hesaplanıyor (doğum tarihinden), kullanıcı manuel söyleme gerek yok. Onboarding sırasında "kaç yaşında" değil "doğum tarihi" sorulur.

Hangi modda olduğun belli değilse kullanıcıya sor. Belli olduğunda ilgili referansı oku ve takip et.

## Kullanıcı belleği (memory)

Her kullanıcının BES profili ve sepet geçmişi `memory/users/{kullanıcı_kısa_adı}/` altında saklanır:

```
memory/users/{kısa_ad}/
├── profile.md          # Doğum tarihi, gelir, vade, risk profili, sözleşmeler, override geçmişi
├── current_basket.md   # Şu an aktif sepet + talep tarihi pay fiyatları + önceki sepetin gerçek getirisi
└── history/
    ├── 2026-05.md      # O ayın revizesi: piyasa özeti + sepet + sebep + gerçek getiri
    ├── 2026-06.md
    └── 2026-yillik.md  # Yıllık özet (yıl sonu)
```

İlk çalıştırmada: `memory/users/{kısa_ad}/` yoksa **Onboarding moduna gir**.
Sonraki çalıştırmalarda: profile.md'yi oku, kullanıcıyı tanı, ona göre devam et.

`memory/_template/` altında boş bir yapı var — yeni kullanıcı için onu kopyala. Şema sürümü 2 (frontmatter'da `Şema sürümü: 2`).

## Onboarding (ilk açılış)

Kullanıcıya kim olduğunu sor, sonra `references/onboarding.md` dosyasındaki **5 soruyu** sorarak profilini çıkar. AskUserQuestion tool'u varsa onu kullan (daha iyi UX), yoksa düz sorularla. **Soru 1 doğum tarihi** — yaş manuel kayıt edilmez, doğum tarihi tutulur, yaş her revizede otomatik hesaplanır.

Sorulardan sonra:

1. Cevapları `memory/users/{kısa_ad}/profile.md`'ye yaz (template'i kopyala)
2. `references/risk_profile.md`'i okuyarak hangi risk profiline (defansif / dengeli / agresif) düştüğünü hesapla
3. `references/fund_research.md`'i okuyarak son hafta + son ay verilerini topla (yedekli zincir)
4. `references/basket_construction.md`'i okuyarak risk profili × güncel piyasa → sepet kur
5. Sepeti kullanıcıya göster, onay al
6. **Kurum kontrolü** — `references/providers/{kurum}.md` var mı?
   - **Var** (Türkiye Hayat, veya başka bir keşfi tamamlanmış kurum): adapter'ı oku, eSube'de uygula
   - **`{kurum}_draft.md` var** (önceki keşif yarım kalmış): "kaldığımız yerden devam edelim mi?" sor → onaylarsa devam, reddederse manuel mod
   - **Yok** (stub kurum): **Kurum keşif moduna gir** — `references/adapter_discovery.md`'i takip et, kullanıcıya iki seçenek sun (birlikte keşfet / bu sefer manuel)
7. Her fonun talep tarihi pay fiyatını eSube'den/TEFAS'tan al, `current_basket.md`'ye yaz
8. `history/{YYYY-MM}.md`'yi yaz
9. Aylık scheduled task'ı kur (bkz. `scripts/schedule_monthly.py`)

## Aylık revize akışı

Scheduled task ya da manuel komutla tetiklenir. `references/monthly_review.md`'i takip et. **9 adımdan oluşan disiplinli akış**:

1. Memory'i aç (profile + current_basket + son 3 ay history)
2. **Yaş kontrolü** (otomatik, doğum tarihinden) → eşik geçildiyse kullanıcıya sor (sadece ilk kez)
3. **Önceki sepetin gerçekleşmiş getirisini hesapla** (TEFAS pay fiyatlarıyla) — atla yasak
4. Bu ayın piyasa verisi (yedekli zincir: CNBCe → besfongetirileri → fintables → TEFAS → manuel)
5. Karşılaştır: değişiklik gerekli mi? Önceki performansı dikkate al
6. Yeni sepeti hesapla (gerekirse)
7. Kullanıcıya öneri sun (önceki performans dahil format)
8. Onay → eSube'ye gir → uygula → pay fiyatlarını al
9. History yaz, current_basket güncelle

## Yıllık özet akışı

Her takvim yılının ilk revizesi yıllık özetle başlar. Manuel: `/bes-yillik`. `references/annual_review.md`'i takip et: 12 ayın compound getirisi, hak kullanımı analizi, tema dağılımı, profil sorgusu, vergi notları.

Vergi sezonu (Mart-Nisan) yakınsa kullanıcıya bir kez hatırlatma çıkarılır.

## Kurum keşif akışı (adapter yoksa)

V1'de tam test edilmiş tek kurum **Türkiye Hayat ve Emeklilik**. Diğer 17 BES kurumu için adapter yok — ama skill **boş öneriyle bırakmaz**. Kullanıcı stub bir kurumdaysa:

1. `references/adapter_discovery.md`'i oku — keşif sürecinin tam playbook'u orada
2. Kullanıcıya net iki seçenek sun:
   - **A) Birlikte keşfedelim**: 30-60 dk ekran-ekran, sonunda kalıcı adapter; sonraki kullanımlar otomatik
   - **B) Bu sefer manuel**: skill önerisi verir, kullanıcı eSube'de elle uygular
3. A seçildiyse `_stub_template.md`'i `references/providers/{kurum}_draft.md` olarak kopyala, frontmatter doldur (`adapter_durumu: KEŞİF`, `keşif_başlangıcı: {tarih}`)
4. 10 adımlık keşif akışını yürüt: Login → Hesap yapısı → Fon dağılım menüsü → Sayfa yapısı → JS selector keşfi → BEFAS → Yüzde girme testi → Doğrulama → Hata sapmaları → Pay fiyatı çekme
5. Her adımda drafte yaz; her ekranda kullanıcının gördüğünü teyit et
6. Akış başarıyla tamamlandığında promosyon teklif et: `_draft.md` → `.md`, frontmatter `TEST EDİLMİŞ ✅`, README tablosu güncelleme
7. Topluluğa katkı PR'ı önerisi (opsiyonel — `CONTRIBUTING.md` rehberi)

Yarım kalan keşif `_draft.md` olarak kalır; bir sonraki kullanımda skill kullanıcıya "kaldığımız yerden devam edelim mi?" sorar (son tamamlanan adımı söyleyerek).

**Mahremiyet**: Keşif sırasında kullanıcının ekranında sözleşme no/ad-soyad/birikim görünür ama drafte **yazılmaz** — sadece UI yapısı, akış, JS davranışı kayda geçer.

## Browser otomasyonu kuralları (kritik)

eSube'de fon dağılımı değiştirirken **şu kurallar mutlak**:

1. **Son "Tamam"/"Onayla"/"Gönder" tıkını ASLA sen yapma** — her zaman kullanıcı yapar. Sen yüzdeleri girip durursun, "Tamam'a sen bas" dersin.
2. **SMS doğrulama / şifre / TC kimlik / kart bilgisi GİRME** — bunlara dokunma, kullanıcı kendi yazar.
3. **BEFAS bilgilendirme onayı** kullanıcı izin verirse işaretlenebilir, aksi halde sor.
4. **Yüzde toplamı 100 olmalı** — set ettikten sonra her zaman doğrula. Bazı eSube'lerde plan validator otomatik yüzdeleri düşürür → ikinci pas at, toplamı kontrol et. Gerekirse `references/error_recovery.md` Senaryo 2'yi uygula.
5. **Aynı fon iki satırda görünebilir** (THE'de mevcut + BEFAS'ta yeni eklenen) — bunu kontrol et, birini sıfırla. (Senaryo 6)
6. **"Mevcut + gelecek" radio'su seçili olsun** (default zaten bu, ama doğrula).
7. **Hata oluştuğunda sessiz kurtarma yasak** — `references/error_recovery.md`'i oku, ilgili senaryoyu kullanıcıyla şeffaf yürüt.

Browser otomasyonu adımlarının kurum-spesifik detayları `references/providers/{kurum}.md` altında. V1'de tam test edilmiş tek kurum **Türkiye Hayat** — diğer kurumlar için adapter'lar deneysel, kullanıcıya bildir.

## Veri kaynağı disiplini

- **Tek kaynaktan veri yetmez** — `references/fund_research.md`'deki 4 kademeli yedekli zinciri kullan
- Hiç kaynak çalışmadıysa: kullanıcıdan manuel veri iste (sessiz tahmin yasak)
- Pay fiyatlarını her revizede topla — gerçek getiri hesabı buna bağlı

## Güvenlik ve uyarılar

- **Bu skill yatırım tavsiyesi vermez.** Sadece momentum verisi + risk profiline göre operasyonel rehberdir. Kararı kullanıcı verir.
- Geçmiş getiri gelecek getiriyi garanti etmez.
- Momentum stratejisi trend kırıldığında hızla zarar yazabilir. **Önceki sepetin gerçek getirisi ölçülür**, 2 ay üst üste benchmark altıysa stratejiyi kullanıcıyla yeniden değerlendir.
- Kullanıcının fon değişiklik hakkı yılda 12 (Genelge 2026/1, Madde 8/Y) — boşa kullanma. Eğer revize değişikliği marjinalse "bu ay pas geçelim" demek değerli bir cevaptır.
- **Fon gider iadesi** sözleşmenin 6. yılından itibaren başlar (BES Yönetmeliği Madde 22/A). BEFAS üzerinden alınan diğer kurum fonlarının gider kesintileri **iade hesaplamasına dahil edilmez** — sadece kendi kurum fonlarınkiler hesaba girer. Kullanıcıya BEFAS açarken bu bilgiyi sun. (Bu, devlet katkısı **kazancını** etkilemez — devlet katkısı katkı payı üzerinden hesaplanır, fonlardan bağımsız.)
- 18 yaş altı kumbara hesabı varsa, ekstra ihtiyat: agresif sepet ancak kullanıcı açıkça istiyorsa.

## Komutlar

`commands/` altında hazır komutlar var:

- `/bes-onboard` — yeni kullanıcı veya profil sıfırlama
- `/bes-revize` — manuel aylık revize
- `/bes-durum` — şu anki sepet + kalan hak + son revize + son gerçekleşmiş getiri
- `/bes-yillik` — yıllık özet (12 ayın compound getirisi + analiz)

## Veri kaynakları (özet)

- **Haftalık fon getirileri**: cnbce.com → besfongetirileri.com → fintables.com → TEFAS (yedekli zincir)
- **Pay fiyatları (gerçek getiri)**: TEFAS resmi (https://www.tefas.gov.tr) + eSube fon detayı
- **Benchmark**: BIST 100 (TCMB EVDS), TÜFE (TÜİK)
- **Resmi mevzuat**: emeklilik.egm.org.tr (Genelge 2026/1, BES Yönetmeliği)
- **Makro**: TCMB faiz, USDTRY (web search ile günlük)

Detayı `references/fund_research.md`'de.

## Yıllık takvim

- Ayın 1'inde scheduled task (kullanıcı kabul ettiyse)
- Ocak ilk revizede otomatik yıllık özet
- Mart-Nisan vergi sezonu hatırlatma
- Manuel `/bes-revize` ya da `/bes-yillik` istediği zaman

12 ay × 1 revize = 12 değişiklik hakkından yıl içinde tipik 6-9 kullanılır (her ay aktif değişiklik anlamlı değil; bazı aylar pas geçilir). Kalan haklar yıl sonuna doğru daha cömertçe kullanılabilir.

## Şema sürümü ve geriye uyum

Şema sürümü 2 ile çalışıyoruz (profile.md'de `Şema sürümü: 2`). Sürüm 1'den geçiş:
- "Yaş: 32" alanı varsa → kullanıcıya doğum tarihini sor, yaş alanını sil, doğum tarihi yaz
- Eski sözleşmelerde "Açılış tarihi" yoksa → kullanıcıya sor (fon gider iadesi zamanlaması için kritik)
- Eski current_basket.md'de pay fiyatları yoksa → bir sonraki revizede gerçek getiri hesabı atla, "veri yok" notu düş, ileri revizelerde topla

---

**Bir şey unutma:** Bu skill bir kullanıcı için tek seferde değil, **yıllarca kullanılacak**. Kararlar kümülatiftir, geçmişi (history klasöründe) gözden geçir, "şunu zaten denedik, işe yaramamıştı" gibi notları dikkate al. Önceki sepetin gerçek getirisi her revizede ölçülür — eğer strateji çalışmıyorsa kullanıcıyla açık ol, profil veya yaklaşım değiştirme önerisi getir. Kullanıcı zaman içinde değişir; profili güncel tut.
