# BES Pilot 🇹🇷

**Türkiye Bireysel Emeklilik Sistemi (BES) için kişisel pilot — Claude skill'i**

BES sözleşmenizi sizinle birlikte aktif yönetir: yaş, gelir, vade ve risk toleransınıza göre fon sepeti kurar; her ay piyasa konjonktürünü takip ederek revize eder; eSube üzerinden tarayıcıyla gerçek fon dağılımı değişikliğini birlikte yapar (son "Tamam"ı her zaman siz basarsınız).

> ⚠️ **Yatırım tavsiyesi değildir.** Operasyonel rehber ve momentum tabanlı sepet aracıdır. Tüm yatırım kararları kullanıcının sorumluluğundadır.

## Ne yapar?

- 🎯 **Onboarding**: Doğum tarihi + 5 soruda risk profilinizi çıkarır (defansif / dengeli / agresif). Yaş otomatik takip edilir, manuel "yaşım değişti" demeye gerek yok.
- 📊 **Sepet kurar**: Risk profili + güncel piyasa verisini birleştirip 6-10 fonluk sepet önerir
- 📈 **Performansı ölçer**: Her revizede önceki sepetin gerçek getirisini hesaplar, BIST 100 ve TÜFE benchmark'larıyla karşılaştırır — strateji çalışıyor mu çalışmıyor mu hep ölçülür
- 🌐 **Tarayıcıyla uygular**: eSube'ye girer, BEFAS'tan kurumları/fonları ekler, yüzdeleri yazar — son onayı siz verirsiniz
- 📅 **Aylık + yıllık takip**: Otomatik scheduled task + manuel `/bes-revize` ve `/bes-yillik` komutları
- 🧠 **Bellek**: Profilinizi, sepet geçmişinizi, ay-ay piyasa kararlarını saklar
- 💰 **Hak yönetimi**: Yıllık 12 fon değişiklik hakkını (Genelge 2026/1) kontrollü kullanır, gereksiz revizeden kaçınır
- 🛡️ **Hata kurtarma**: eSube'de oturum kopması, validator hataları, BEFAS modal sorunları — hepsi için açık playbook (sessiz başarısızlık yok)
- 🔁 **Yedekli veri kaynağı**: CNBCe → besfongetirileri → fintables → TEFAS → manuel — tek kaynak kırılırsa otomatik geçer
- 🔍 **Yaşayan adapter keşfi**: Kurumunuzun adapter'ı yoksa skill sizinle birlikte ekran-ekran keşfeder, kalıcı adapter oluşturur — tek seferlik 30-60 dk yatırım, sonraki tüm aylar (ve sonraki tüm kullanıcılar için PR atarsanız) otomatik

## Desteklenen kurumlar (V1)

| Kurum | Adapter Durumu |
|---|---|
| Türkiye Hayat ve Emeklilik | ✅ Tam test edilmiş |
| Anadolu Hayat | 🟡 Stub — kullanıcıyla keşif modunda çalışır |
| Garanti Emeklilik | 🟡 Stub |
| Allianz Yaşam | 🟡 Stub |
| Allianz Hayat | 🟡 Stub |
| Agesa | 🟡 Stub |
| HDI Fiba | 🟡 Stub |
| AvivaSA | 🟡 Stub |
| NN Hayat | 🟡 Stub |
| Vakıf | 🟡 Stub |
| AXA | 🟡 Stub |
| BNP Paribas Cardif | 🟡 Stub |
| Bereket Emeklilik | 🟡 Stub |
| Katılım Emeklilik | 🟡 Stub |
| MetLife | 🟡 Stub |
| QNB Sağlık | 🟡 Stub |
| Vienna Life | 🟡 Stub |
| Zurich Yaşam | 🟡 Stub |

### Stub kurum nasıl çalışır?

Türkiye Hayat dışındaki tüm kurumlar **stub** olarak işaretli — yani henüz tam test edilmemiş. Bu, "skill o kurumda çalışmaz" demek **değil**:

1. Kullanıcı kurumunu söylediğinde, skill iki seçenek sunar:
   - **Birlikte keşfedelim** (30-60 dk, ekran-ekran) → sonunda o kurum için **kalıcı adapter** üretilir, sonraki aylar otomatik çalışır. Detay: [`references/adapter_discovery.md`](references/adapter_discovery.md)
   - **Bu sefer manuel** → skill öneri verir, kullanıcı eSube'de elle uygular
2. Keşif tamamlandığında dosya `references/providers/{kurum}.md` olarak yazılır, README tablosu 🟡 → ✅ olur
3. PR atılırsa **tüm topluluk** o kurum için otomatik adapter'a kavuşur — `CONTRIBUTING.md`'de PR rehberi

**Adapter olgunluk seviyeleri**:
- 🔴 Stub: hiç keşfedilmedi
- 🟡 Keşif (`_draft.md`): aktif keşif sürüyor
- 🟢 Test edilmiş: bir kez baştan sona çalıştı
- ✅ Olgun: 3+ revize, 2+ kullanıcı doğrulaması

Manuel keşif komutu: `/bes-kurum-kesfet`

## Kurulum

> ⚠️ **Bu skill şu an sadece Claude Code (CLI) içinde test edilmiştir.** Cowork (Claude Desktop) tarafında skill keşfi sürümler arasında değişiyor — orada güvenilir şekilde çalışmıyor olabilir. Önerilen kullanım Claude Code.

### Claude Code (terminal) — önerilen

Önkoşul: [Claude Code](https://claude.ai/code) yüklü olmalı (`claude` komutu çalışıyor).

```bash
# 1. Repo'yu klonla
git clone https://github.com/ViberProDevAI/bes-pilot.git ~/Projects/bes-pilot

# 2. Claude Code skill dizinine bağla (sembolik link — git pull ile otomatik güncellenir)
mkdir -p ~/.claude/skills
ln -s ~/Projects/bes-pilot/bes-pilot ~/.claude/skills/bes-pilot
```

Test et:

```bash
claude "BES sepetimi kur"
```

Yanıtın **ilk satırında** `🎯 **bes-pilot v0.2.0** — {mod}` görüyorsan skill çalışıyor demektir. Görmüyorsan skill yüklenmemiş.

### Düz kopya (link istemezsen)

```bash
git clone https://github.com/ViberProDevAI/bes-pilot.git
mkdir -p ~/.claude/skills
cp -r bes-pilot/bes-pilot ~/.claude/skills/bes-pilot
```

### Güncelleme

```bash
cd ~/Projects/bes-pilot && git pull
# Symlink kullandıysan otomatik yansır
```

### Cowork (Claude Desktop) — ZIP yükleme yöntemi

> ⚠️ **Anthropic bilinen bug** ([Issue #39400](https://github.com/anthropics/claude-code/issues/39400)): Marketplace üzerinden kurulan plugin'lerin skill dosyaları Cowork container'ına mount edilmiyor. Plugin listede görünür ama "skill bulunamadı" hatası alırsın. ZIP yükleme yöntemi bu bug'ı atlatıyor.

**Adımlar (Pro/Max/Team/Enterprise gerekiyor):**

1. ZIP'i indir:
   - Repo'yu klonladıysan: `cd ~/Projects/bes-pilot && zip -r ~/Desktop/bes-pilot.zip bes-pilot .claude-plugin LICENSE README.md -x "*/__pycache__/*" -x "*/.DS_Store"`
   - Klonlamadıysan: GitHub'dan repo'yu ZIP olarak indir, içinden `bes-pilot/` ve `.claude-plugin/` klasörlerini birleştir

2. Cowork'te:
   - **Cowork sekmesi** → sol sidebar **"Customize"**
   - **"Browse plugins"** → **"Add plugin"** → **"Upload"**
   - `bes-pilot.zip` seç
   - Yüklendi mesajını gör

3. Cowork'ü Cmd+Q ile tamamen kapat + tekrar aç

4. Yeni sohbet → `/bes-pilot` veya "BES sepetimi kur"

5. Yanıtın ilk satırında `🎯 **bes-pilot v0.2.0** —` görmüyorsan skill yüklenmemiştir.

### Bağımlılıklar

- Tarayıcı otomasyonu için **Claude in Chrome** uzantısı (önerilir) — eSube'de tıklama ve form doldurma için
- Veri toplama için **WebSearch + WebFetch** araçları (Claude Code'da varsayılan)
- Aylık otomatik tetikleme için **scheduled-tasks MCP** (opsiyonel)

## Skill nasıl düşünür? (karar gerekçesi)

Skill, BES sepetini **dört katmanlı disiplinli bir karar süreciyle** kurar — basit "şu fonlar iyi" yaklaşımı değil. Her katman farklı bir veri kaynağına dayanır:

### Katman 1 — Risk profili (5 soru, 4 boyut)

| Soru | Ne ölçer | Örnek puan etkisi |
|---|---|---|
| Doğum tarihi + hedef yaş | **Vade** (yıl) | ≥20 yıl: +2 / <10 yıl: −2 |
| Aylık katkı + birikim | **DCA gücü** | Katkı ≥ gelirin %10'u: +1 |
| "%15 düştü, ne yaparsın?" | **Kayıp toleransı (psikolojik)** | A: −3 / B: 0 / C: +3 — **HARD OVERRIDE** |
| BES'ten beklenti | **Hedef** | A: −2 / B: 0 / C: +2 |
| Kurum + sözleşmeler | **Operasyonel** | (puanlamaz, adapter seçimi için) |

Toplam puan ≤ −3 = DEFANSİF, −2 ile +2 = DENGELİ, ≥ +3 = AGRESİF.

> **Sert kural**: Soru 3'te A diyene **agresif sepet asla yapılmaz**, başka cevaplar ne olursa olsun. Kullanıcı paniklerse erken bozdurur, en kötü senaryo bu.

### Katman 2 — Konjonktürel araştırma (her revizede yeniden)

`references/fund_research.md` — **4 kademeli yedekli veri zinciri** ile 6 soruya cevap arar:

```
CNBCe haftalık derleme → besfongetirileri.com → fintables.com → TEFAS → manuel kullanıcı girişi
```

En az **2 kaynaktan teyit** alır. Hepsi başarısızsa kullanıcıya açık olur ("veri yok, manuel ver"), sessiz tahmin yapmaz.

6 soru:
1. **Lider tema** nedir? (teknoloji / altın / borçlanma / ...)
2. **Konsantrasyon**: top 10'un kaçı tek kategoride? (≥7 = belirgin sinyal)
3. **Trend doğrulanmış mı**? (hafta = ay yönü)
4. **Counter-momentum fırsatı** var mı? (en kötü kategori 3+ ay düşmüş mü)
5. **Makro şok** var mı? (TCMB faizi, USDTRY, jeopolitik)
6. **Regülasyon değişikliği** var mı? (Genelge takip)

### Katman 3 — Sepet algoritması (`references/basket_construction.md`)

Profil iskeletine konjonktürel **tilt** uygular:

| Durum | Tilt |
|---|---|
| Belirgin tema lider (top 10'un %70+'ı) | O kategoriye **+%10**, defansif kategorilerden −%10 |
| Trend doğrulanmış | Tilt korunur |
| Trend belirsiz | Tilt yapılmaz, iskelete sadık kal |
| Makro şok | Defansife **+%10** geçici geçiş |
| **Defansif kullanıcı** | Tilt **max ±%5** (sektör bahsi yapılmaz) |

**Çoklu fon kuralı** (tek kategori içinde, yönetici risk dağıtımı):
- Ağırlık <%15 → 1 fon
- %15-30 → **2 farklı kurucu**
- >%30 → **3 farklı kurucu**

**Stabilite cezası** (12 hak/yıl boşa harcanmasın):
- Geçen ay sepetiyle <%15 değişiklik → "**pas geç**" öneri
- <%2 ek getiri beklentisi olan değişiklik → yapma

### Katman 4 — Performans geri besleme (yeni!)

Her revizede **önceki sepetin gerçek getirisi ölçülür**:

```
sepet_getiri = Σ (fon_ağırlığı × (yeni_pay_fiyatı / önceki_pay_fiyatı − 1))
reel_getiri = sepet_getiri − TÜFE
benchmark_farkı = sepet_getiri − BIST 100
```

Pay fiyatları: TEFAS resmi + eSube fon detayı. Benchmark'lar: TCMB EVDS (BIST), TÜİK (TÜFE).

**Eğer 2 ay üst üste benchmark altıysa skill stratejiyi sorgular**: "Önceki yaklaşım çalışmadı, profili gözden geçirelim mi?" Yani strateji **inanç** değil, **ölçüm** meselesi.

## Kişiselleştirme garantisi

> Senin sepetin başka birine **bire bir** verilmez — 4 boyutta kişiselleşir:

1. **Risk profili**: Defansif vs agresif tamamen farklı sepet (%25 hisse vs %75 hisse)
2. **Kurum**: BEFAS kapalıysa sadece kendi kurum fonların. Türkiye Hayat'ta TVH/TBJ, Anadolu'da BHT
3. **Vade + yaş**: Yaş eşik geçişlerinde profil otomatik gözden geçirilir (40, 55) — kullanıcı override edebilir, kayıt altında
4. **Sözleşme ekosistemi**: 18 yaş altı kumbara hesabı varsa farklı (kullanıcı açıkça istemediği sürece muhafazakar). Birden fazla sözleşme = her biri ayrı revize seçeneği

Ek kişiselleşme:
- `profile.md` "Kullanıcı override geçmişi" — "Bu eşik bana uymaz" dediğin tüm kararlar kayıtlı
- `current_basket.md` "Önceki sepetin gerçek getirisi" — sadece sana özel performans verisi
- `history/{YYYY-MM}.md` — tüm aylık kararlar, gerekçeler, sonuçlar

## Sonraki ay ne olacak? (aylık akış)

`/bes-revize` (manuel) veya scheduled task tetiklediğinde **9 adım**:

1. Memory aç (profile + current_basket + son 3 ay history)
2. **Yaş kontrolü** (otomatik, doğum tarihinden)
3. **Önceki sepetin gerçek getirisini ölç** — TEFAS pay fiyatı + BIST 100 + TÜFE
4. Bu ayın piyasa verisi (yedekli zincir, 6 soruya cevap)
5. Karşılaştır → değişiklik gerekli mi? **2 ay üst üste underperform stratejiyi sorgular**
6. Yeni sepeti hesapla (gerekirse)
7. Kullanıcıya öneri (önceki performans dahil format)
8. Onay → eSube → uygula → pay fiyatlarını al
9. history yaz, current_basket güncelle

Yıl başında (Ocak ilk revize) önce **yıllık özet** çalışır:
- 12 ayın **compound** getirisi (basit ortalama değil)
- Aylık BIST 100 + TÜFE benchmark karşılaştırması
- Tema dağılımı (kaç ay teknoloji, enerji, altın, ...)
- En isabetli karar / geriye dönüp baktığımızda hata
- Hak kullanım analizi
- Vergi sezonu hatırlatma (Mart-Nisan)

## Kısa örnek diyalog

```
Sen: BES sepetimi kur

Claude: Hoş geldin. Önce kim için çalışacağımızı bilmem lazım — adın? 
        Sonra 5 soruyla profilini çıkaracağım.
        
Sen: [profil bilgileri verir]

Claude: Profilin DENGELİ (puan +1). Soru 3'te B dedin, override yok.
        Bu hafta + bu ay piyasa verisi topluyorum...
        
        [4 kademeli yedekli zincirden veri çeker, en az 2 kaynaktan teyit alır]
        
        Bu ayın özeti:
        - Lider tema: Teknoloji (haftalık 7/10 fon, aylık 9/10)
        - Trend doğrulanmış (hafta = ay yönü)
        - Makro: TCMB faiz sabit, USDTRY 35.40
        
        Önerilen sepet (Türkiye Hayat + BEFAS):
        - VES 20% (Borçlanma TL — koruma)
        - VGA 10% (Altın katılım — enflasyon hedge)
        - TVH 13% + TBJ 13% (Teknoloji — 2 farklı kurucu, %26 ağırlık için)
        - GCN 12% + YZD 12% + FFC 10% (Teknoloji çeşitlendirme)
        - ENF 10% (Enerji rotasyonu)
        
        Gerekçe: Dengeli iskeletten teknoloji teması için +%10 tilt 
        (top 10'un %70+'ı tek kategoride). Borçlanma %25→%20'ye 
        çekildi. 4 farklı kurucudan teknoloji fonu — yönetici risk 
        dağıtımı (>%30 ağırlık için 3+ kurucu kuralı).
        
        Toplam %100. Onaylıyor musun? Yoksa ayar isteyen var mı?

Sen: [onayladıktan sonra eSube otomasyonu, kullanıcı "Tamam"a basar, 
      pay fiyatları kaydedilir, history yazılır]

[Bir ay sonra /bes-revize çalıştırılınca]

Claude: Önceki sepetinin gerçek getirisi (33 gün):
        - Sepet: +%3.45
        - BIST 100 aynı aralık: +%2.83  
        - TÜFE Nisan: +%1.92
        - Reel getiri: +%1.53 ✅ (TÜFE üstü)
        - Benchmark farkı: +%0.62 ✅ (BIST üstü)
        
        Strateji çalıştı. Bu ayın piyasa özeti:
        [...yeni veri]
        
        Önerim: PAS GEÇ (sepet ile öneri %92 örtüşüyor, 
        marjinal değişiklik anlamlı değil — fon hakkını koruyalım, 
        kalan: 8/12).
```

## Güvenlik

- 🔒 **Kredentialler hiç dokunulmaz**: Şifre, TC kimlik, SMS kodu — hepsini siz yazarsınız
- 🛑 **Son onay her zaman siz**: "Tamam" / "Onayla" / "Gönder" butonlarına Claude basmaz, siz basarsınız
- 🚫 **Memory pushlanmaz**: `.gitignore` `memory/users/` dizinini hariç tutar — finansal bilginiz GitHub'a gitmez
- ⚠️ **Yatırım tavsiyesi yok**: Skill operasyonel rehberdir, kararlar size aittir

## Mimari

Repo, Claude Code plugin marketplace formatındadır:

```
bes-pilot/                          # repo root (marketplace)
├── .claude-plugin/
│   ├── marketplace.json            # Marketplace tanımı (plugin listesi)
│   └── plugin.json                 # Plugin metadata
├── bes-pilot/                      # Plugin içeriği (skill kendisi)
│   ├── SKILL.md                    # Ana orchestration (6 mod)
│   ├── references/                 # İlgili modlarda yüklenen rehberler
│   │   ├── onboarding.md           # Doğum tarihi + 5 soru
│   │   ├── risk_profile.md         # Profil → temel allokasyon (kanıt + gerekçe)
│   │   ├── fund_research.md        # 4 kademeli yedekli veri zinciri
│   │   ├── basket_construction.md  # Sepet algoritması + performans geri besleme
│   │   ├── monthly_review.md       # 9 adımlık aylık akış
│   │   ├── annual_review.md        # Yıllık compound + tema dağılımı + vergi notları
│   │   ├── error_recovery.md       # 9 senaryo hata kurtarma playbook
│   │   ├── adapter_discovery.md    # Yeni kurum keşif akışı (10 adım)
│   │   └── providers/
│   │       ├── turkiye_hayat.md    # ✅ Tam test edilmiş + pay fiyatı çekme
│   │       └── _stub_template.md   # 🟡 Keşif iskeleti
│   ├── commands/
│   │   ├── bes-onboard.md
│   │   ├── bes-revize.md
│   │   ├── bes-durum.md
│   │   ├── bes-yillik.md
│   │   └── bes-kurum-kesfet.md     # Manuel adapter keşfi
│   ├── scripts/
│   │   ├── schedule_monthly.py
│   │   └── fetch_fund_returns.py   # Yedekli zincir + yapılandırılmış hata
│   ├── memory/                     # Kalıcı kullanıcı verisi (gitignored)
│   │   ├── README.md
│   │   ├── _template/              # Şema 2: doğum tarihi + pay fiyatları + override geçmişi
│   │   └── users/                  # Gerçek kullanıcı verisi (gitignored)
│   └── evals/
│       └── evals.json              # 20 test (5 trigger + 15 unit/edge case)
├── README.md                       # Bu dosya
├── CONTRIBUTING.md                 # Topluluğa katkı + adapter PR rehberi
├── CHANGELOG.md                    # Sürüm geçmişi
├── LICENSE
├── .gitignore
└── .github/workflows/ci.yml        # Syntax + PII + cross-reference CI
```

## Topluluk katkısı

PR'lar memnuniyetle karşılanır:

- **Yeni kurum adapter'ı** — `_stub_template.md`'i takip ederek o kurumun eSube'sini test edip yaz
- **Daha iyi piyasa veri kaynakları** — `references/fund_research.md`'e ekle
- **Risk profili kalibrasyon iyileştirmesi** — onboarding sorularını ve eşikleri test et, daha iyisini öner
- **Mobile eSube desteği** — bazı kurumların web'i kötü ama mobile uygulaması var; mobil otomasyon eklenebilir mi?

## Sıkça Sorulan

**S: Skill her ay otomatik fon değiştiriyor mu?**
H: Hayır. Her ay tetiklenir, **öneriyle gelir**, siz onaylar veya reddedersiniz. Sepet değişikliği marjinalse "pas geç" der. Yıllık 12 hak harcanmaz.

**S: BEFAS'ı zorunlu açıyor mu?**
H: Hayır. Açmak isterseniz açar (sepet daha geniş olur), açmak istemezseniz sadece kendi kurumunuzun fonlarından sepet kurar. Trade-off'unu açıklar.

**S: Devlet katkısını kaybeder miyim?**
H: Devlet katkısı **kazancı** etkilenmez — katkı payı üzerinden hesaplanır, hangi fonu seçtiğinizden bağımsızdır. BEFAS açıldığında değişen şey **fon gider iadesi**dir (sözleşmenin 6. yılından itibaren başlayan iade, BES Yönetmeliği Madde 22/A): BEFAS üzerinden alınan diğer kurum fonlarının gider kesintileri iade hesaplamasına dahil edilmez. Skill bunu BEFAS açma anında hatırlatır.

**S: Birden fazla sözleşmem var, hepsi aynı sepet mi?**
H: Sizin tercihinize göre. Skill her sözleşme için ayrı sepet de yapabilir (örn. ana sözleşme dengeli, çocuk kumbara hesabı agresif).

**S: Skill çok mu agresif/defansif kuruyor?**
H: Risk profili 5 sorudan çıkar, ama her zaman ayarlayabilirsiniz: "daha defansif yap" / "daha agresif yap" deyin, sepeti tilt eder.

## Lisans

MIT — bkz. [LICENSE](LICENSE)

## Teşekkür

- Anthropic Claude ekibine — agent SDK ve Cowork mode için
- BES regülasyon yapısını anlaşılır kılan EGM'ye
- Verilerini topladığımız CNBCe, fintables, besfongetirileri.com'a

## Yasal Uyarı

Bu skill yatırım tavsiyesi vermez, finansal danışmanlık hizmeti değildir. Geçmiş getiriler gelecek getirileri garanti etmez. Tüm yatırım kararlarınızdan kendiniz sorumlusunuz. Şüphede iseniz bir SPK lisanslı yatırım danışmanına danışın.
