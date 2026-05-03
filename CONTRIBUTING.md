# Katkıda Bulunma Rehberi

BES Pilot, Türkiye Bireysel Emeklilik Sistemi için açık kaynak bir Claude skill'idir. Topluluk katkıları memnuniyetle karşılanır — özellikle yeni kurum adapter'ları, daha iyi veri kaynakları ve risk profili kalibrasyon iyileştirmeleri.

## Katkı türleri

### 1. Yeni kurum adapter'ı (en büyük etki)

V1'de tam test edilmiş tek kurum **Türkiye Hayat ve Emeklilik**. Diğer 17 kurum için adapter'lar stub modunda — ekran-ekran keşif ile çalışıyor. Senin BES'in farklı bir kurumdaysa adapter yazmak en değerli katkıdır.

**Adımlar**:
1. `references/providers/_stub_template.md`'i oku — yeni adapter yazma rehberi
2. Kendi kurumunda bir aylık revize sürecini skill ile birlikte ekran ekran yap
3. Skill'in keşfettiği eSube akışını `references/providers/{kurum_kisa_adi}.md` olarak yaz (örn: `garanti.md`, `anadolu_hayat.md`)
4. `turkiye_hayat.md` formatını taklit et: login akışı, hesap yapısı, fon dağılım değişikliği akışı, BEFAS akışı, JS snippet'leri (yüzde girme + doğrulama), bilinen tuhaflıklar, hata kurtarma sapmaları
5. README.md'deki "Desteklenen kurumlar" tablosunda kurumun durumunu 🟡 → ✅ olarak güncelle
6. PR aç, başlık: `feat(provider): {Kurum} adapter'ı`

**Kabul kriterleri**:
- Adapter en az bir gerçek kullanıcı hesabında test edilmiş (PII paylaşma — sadece "test edildi" notu)
- JS snippet'leri kuruma özel CSS/element ID'leri ile çalışıyor
- En az 3 hata senaryosu (oturum timeout, validator, BEFAS) kurum perspektifinden ele alınmış
- Pay fiyatı çekme yöntemi belgelenmiş (gerçek getiri hesabı için kritik)

### 2. Veri kaynağı iyileştirmesi

`references/fund_research.md`'deki yedekli zincir kırılganlıklara açık (CNBCe URL pattern'i değişebilir, besfongetirileri DOM yenilenebilir). Daha iyi parser, ek kaynak veya akıllı fallback önerilebilir.

**Örnek katkılar**:
- `scripts/fetch_fund_returns.py`'de yeni kaynak (örn. TEFAS API kullanımı)
- Mevcut parser'ları daha esnek regex/CSS selector'a çevirme
- Veri tutarlılık çapraz doğrulaması (iki kaynaktan getiri farklıysa uyarı)

### 3. Risk profili kalibrasyonu

`references/risk_profile.md`'deki eşikler (yaş 40/55, override puan ±3) **klinik veriyle kalibre edilmedi** — varsayımsal. Backtest, akademik kaynak veya gerçek kullanıcı geri bildirimiyle iyileştirme önerileri kıymetli.

**Veri varsa**: 12+ ay BES revize geçmişiyle yapılmış backtest sonuçları, hangi profil eşiklerinin underperform/overperform'a yol açtığını gösterir.

### 4. Mobile eSube desteği

Bazı kurumların web eSube'si kötü ama mobil uygulamaları daha iyi (örn. AvivaSA, Garanti BBVA Mobil). Mobil otomasyon (computer-use MCP veya benzeri) ile mobil-first adapter yazılabilir.

### 5. Çeviri / dokümantasyon

Bu skill şu an Türkçe. İngilizce çeviri (`README.en.md`, `SKILL.en.md`) aday — ama BES Türkiye'ye özgü olduğu için ana hedef kitle Türkçe konuşanlar. Yine de uluslararası okuyucular için ana dosyaların açıklayıcı bir İngilizce özeti faydalı olabilir.

## Geliştirme akışı

```bash
# 1. Repo'yu fork et, klonla
git clone https://github.com/{senin_kullaniciadın}/bes-pilot.git
cd bes-pilot

# 2. Yeni branch
git checkout -b feat/yeni-adapter-kurum-adi

# 3. Geliştirme dizinini Cowork/CLI'ya bağla (sembolik link önerilir)
mkdir -p ~/Library/Application\ Support/Claude/skills
ln -sf "$(pwd)" ~/Library/Application\ Support/Claude/skills/bes-pilot

# 4. Geliştir, dosya değiştir, Cowork'ü yeniden başlat
# 5. Skill'in çalışıp çalışmadığını test et
```

## PR kontrol listesi

PR açmadan önce:

- [ ] **PII yok**: `grep -r "@\|TR[0-9]\{2\}\|[0-9]\{11\}\b" .` boş döner; özel ad-soyad, sözleşme no, doğum tarihi, TL tutarı, email, telefon yok
- [ ] **Şablon disiplini**: Örnek alanlar `{Tam Ad}`, `{YYYY-MM-DD}`, `{XXXXXXXXX}` gibi placeholder'larla yazılmış (gerçek görünür sahte veri değil)
- [ ] **Cross-reference doğru**: Yeni dosya/komut ekledİysen SKILL.md, README.md ve ilgili `references/*.md` dosyalarına bağlantı ekledin
- [ ] **Syntax temiz**: `python3 -m py_compile scripts/*.py` ve `python3 -c "import json; json.load(open('evals/evals.json'))"` hata vermez
- [ ] **CI yeşil**: `.github/workflows/ci.yml` GitHub Actions'da geçer
- [ ] **Eval güncellendi**: Yeni davranış eklediysen `evals/evals.json`'a en az 1 test ekledin
- [ ] **CHANGELOG**: `CHANGELOG.md`'de Unreleased bölümüne notunu yazdın

## Tartışma kanalları

- **GitHub Issues**: Hata raporu, özellik isteği, soru
- **GitHub Discussions** (opsiyonel, owner açtıysa): Stratejik tartışmalar, kalibrasyon sohbetleri
- **PR yorumları**: Spesifik kod/içerik geri bildirimi

## Mahremiyet ve güvenlik

- **Asla başka kullanıcının verisini taşıma**: PR'da sözleşme no, ad-soyad, finansal tutarlar olmamalı
- **memory/users/ asla commitlenmez**: `.gitignore` zaten kapsıyor, ama PR diff'i kontrol et
- **Adapter test notları kişiselleşmesin**: "Test edildi" yeterli, "Eren'in hesabıyla test edildi" değil
- **Özel API anahtarları/token yasak**: Skill içinde sabit kodlu kimlik bilgisi olmamalı

## Yatırım tavsiyesi reddi

Bu skill **yatırım tavsiyesi vermez**. PR'larda da bu disiplini koru:
- Spesifik fon/strateji önerisi yapacak değişiklik kabul edilmez
- "Bu fon daima iyi getirir" tarzı iddialar yasak
- Geçmiş getiri verisi gelecek getiri garantisi olarak sunulmamalı
- Tüm kararların kullanıcıya ait olduğu vurgusu korunmalı

## Lisans

Katkıda bulunarak kodunuzun MIT lisansı altında dağıtılmasını kabul etmiş olursunuz (bkz. [LICENSE](LICENSE)).
