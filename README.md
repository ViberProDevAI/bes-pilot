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

> Stub adapter, kullanıcıyla birlikte ekran-ekran ilerleyip o kurumun eSube akışını öğrenir ve **kullanım sonrası kalıcı adapter'ı oluşturur**. Bir sonraki ay/kullanıcı için otomatik çalışır.
>
> Hangi kurumun adapter'ını yazıp PR atarsanız topluluğa katkı yapmış olursunuz!

## Kurulum

> Aşağıdaki komutlarda `OWNER/bes-pilot` kısmını **bu repo'nun gerçek GitHub adresi** ile değiştir (örn. `kullaniciadi/bes-pilot`).

### Cowork (Claude Desktop) — macOS

```bash
# 1. Repo'yu klonla
git clone https://github.com/OWNER/bes-pilot.git ~/Projects/bes-pilot

# 2. Cowork skill dizinine kopyala (veya sembolik link)
mkdir -p ~/Library/Application\ Support/Claude/skills
cp -r ~/Projects/bes-pilot ~/Library/Application\ Support/Claude/skills/

# 3. Cowork'ü (Claude Desktop) yeniden başlat
```

Yeni sohbette **"BES sepetimi kur"** yazarak başla — skill otomatik tetiklenir.

### Claude Code (CLI)

```bash
# 1. Repo'yu klonla
git clone https://github.com/OWNER/bes-pilot.git

# 2. ~/.claude/skills/ altına kopyala
mkdir -p ~/.claude/skills
cp -r bes-pilot ~/.claude/skills/

# 3. Yeni bir oturumda komut tetikle
claude "BES sepetimi kur"
```

### Güncelleme

Repo güncellendiğinde:
```bash
cd ~/Projects/bes-pilot && git pull
# Cowork:
cp -r ~/Projects/bes-pilot/* ~/Library/Application\ Support/Claude/skills/bes-pilot/
# CLI:
cp -r ~/Projects/bes-pilot/* ~/.claude/skills/bes-pilot/
```

Sembolik linkle kurduysan `git pull` yeterli; ek kopya gerekmez.

### Bağımlılıklar

- Tarayıcı otomasyonu için **Claude in Chrome** uzantısı (önerilir) — eSube'de tıklama ve form doldurma için
- Veri toplama için **WebSearch + WebFetch** araçları (Cowork'te varsayılan)
- Aylık otomatik tetikleme için **scheduled-tasks MCP** (Cowork'te varsayılan, opsiyonel)

## Hızlı Başlangıç

```
Sen: BES sepetimi kur

Claude: Hoş geldin! 5 soruda profilini çıkaracağım.
        1. Kaç yaşındasın? Emeklilikten ne zaman çıkmak istiyorsun?
        ...
        
[5 soru sonra]

Claude: Senin profilin "DENGELİ". Şu anda piyasada teknoloji teması güçlü.
        Önerilen sepet:
        - TVH 13%, TBJ 13%, GCN 12%, YZD 12%, FFC 10%, ENF 10%, VES 20%, VGA 10%
        Onaylıyor musun?

Sen: Evet

Claude: Tamam. Türkiye Hayat eSube'sine giriyorum...
        [browser ile eSube'ye girer, fon dağılımı değişiklik ekranına gider,
         BEFAS'ı açar, kurumları ekler, fonları seçer, yüzdeleri yazar]
        
        ✅ Sepet hazır, toplam %100. Şimdi sayfanın altındaki "Tamam" butonuna SEN bas.
        SMS doğrulamayı sen onaylayacaksın. İşlem 4-7 iş günü içinde gerçekleşir.

Sen: yaptım

Claude: Mükemmel. Kayıt edildi. Bir sonraki revize: 1 Haziran. 
        Otomatik scheduled task kurmak ister misin?
```

## Güvenlik

- 🔒 **Kredentialler hiç dokunulmaz**: Şifre, TC kimlik, SMS kodu — hepsini siz yazarsınız
- 🛑 **Son onay her zaman siz**: "Tamam" / "Onayla" / "Gönder" butonlarına Claude basmaz, siz basarsınız
- 🚫 **Memory pushlanmaz**: `.gitignore` `memory/users/` dizinini hariç tutar — finansal bilginiz GitHub'a gitmez
- ⚠️ **Yatırım tavsiyesi yok**: Skill operasyonel rehberdir, kararlar size aittir

## Mimari

```
bes-pilot/
├── SKILL.md                # Ana orchestration (5 mod)
├── README.md               # Bu dosya
├── LICENSE
├── .gitignore
├── references/             # İlgili modlarda yüklenen detaylı rehberler
│   ├── onboarding.md           # Doğum tarihi + 5 soru
│   ├── risk_profile.md         # Profil → temel allokasyon (kanıt + gerekçe)
│   ├── fund_research.md        # 4 kademeli yedekli veri zinciri
│   ├── basket_construction.md  # Sepet algoritması + performans geri besleme
│   ├── monthly_review.md       # 9 adımlık aylık akış
│   ├── annual_review.md        # Yıllık compound + tema dağılımı + vergi notları
│   ├── error_recovery.md       # 9 senaryo hata kurtarma playbook
│   └── providers/
│       ├── turkiye_hayat.md    # ✅ Tam test edilmiş + pay fiyatı çekme
│       └── _stub_template.md   # 🟡 Diğer kurumlar için
├── commands/
│   ├── bes-onboard.md
│   ├── bes-revize.md
│   ├── bes-durum.md
│   └── bes-yillik.md
├── scripts/
│   ├── schedule_monthly.py
│   └── fetch_fund_returns.py   # Yedekli zincir + yapılandırılmış hata
├── memory/                 # Kalıcı kullanıcı verisi (gitignored)
│   ├── README.md
│   ├── _template/          # Şema 2: doğum tarihi + pay fiyatları + override geçmişi
│   └── users/              # Gerçek kullanıcı verisi (gitignored)
└── evals/
    └── evals.json          # 20 test (5 trigger + 15 unit/edge case)
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
