# Changelog

Tüm önemli değişiklikler bu dosyada belgelenecek.

Format: [Keep a Changelog](https://keepachangelog.com/tr/1.1.0/), versiyonlama: [Semantic Versioning](https://semver.org/lang/tr/).

## [Unreleased]

### Eklenen
- **Yaşayan adapter keşif sistemi** (`references/adapter_discovery.md`): Stub kurumlarda kullanıcıyla ekran-ekran 10 adımlık keşif akışı; sonunda kalıcı adapter ve README güncellemesi
- `commands/bes-kurum-kesfet.md`: Manuel keşif komutu
- Yeni mod: **Kurum keşif** (SKILL.md'de 5 → 6 mod)
- Adapter olgunluk seviyeleri: 🔴 Stub → 🟡 Keşif (`_draft.md`) → 🟢 Test edilmiş → ✅ Olgun
- Yarım kalan keşif desteği: `_draft.md` korunur, sonraki kullanımda kaldığı yerden devam

### Değişen
- `references/providers/_stub_template.md`: Pasif şablondan aktif keşif iskeletine dönüştürüldü, frontmatter şeması eklendi
- `commands/bes-onboard.md` + `bes-revize.md`: Stub kuruma rastlandığında otomatik keşif tetikleme
- `SKILL.md`: 6. mod (Kurum keşif) eklendi, kurum kontrolü 3 yollu (var / draft / yok)

## [0.2.0] — 2026-05-03

### Eklenen
- Doğum tarihi tabanlı yaş takibi (Şema sürümü 2) — yaş otomatik hesaplanır, manuel "yaşım değişti" gereği ortadan kalktı
- Önceki sepetin gerçekleşmiş getiri hesabı her revizede zorunlu (TEFAS pay fiyatı + BIST 100 + TÜFE benchmark)
- Yıllık özet akışı (`/bes-yillik` komutu, `references/annual_review.md`): compound getiri + tema dağılımı + vergi sezonu hatırlatması
- Hata kurtarma playbook (`references/error_recovery.md`): 9 senaryo (timeout, validator, BEFAS modal, çift satır, hak 0, bakım, SMS, "Tamam" hatası, atıl sözleşme)
- Yedekli veri kaynağı zinciri (`references/fund_research.md`, `scripts/fetch_fund_returns.py`): CNBCe → besfongetirileri → fintables → TEFAS → manuel
- Override geçmişi tablosu (`memory/_template/profile.md`): yaş eşik öneri kullanıcı kararları kaydedilir, tekrar tekrar sorulmaz
- Genişletilmiş eval kapsamı (5 trigger → 20 test, 8 kategori): risk profili, override, stabilite, yaş eşiği, veri yedekleme, hata kurtarma
- Resmi mevzuat referansları: Genelge 2026/1 (12 hak/yıl), BES Yönetmeliği Madde 22/A (BEFAS fon gider iadesi)

### Değişen
- `current_basket.md` şeması: talep tarihi pay fiyatları + önceki sepetin gerçekleşmiş getirisi alanları zorunlu
- `monthly_review.md`: 5 adımdan 9 adıma genişledi, gerçek getiri hesabı 3. adım olarak eklendi
- BEFAS açıklaması düzeltildi: devlet katkısı kazancı etkilenmiyor; etkilenen şey **fon gider iadesi** (sözleşme 6. yılı sonrası, BES Yönetmeliği Madde 22/A)
- Risk profili eşikleri (yaş, tilt, stabilite) gerekçelendi ve "kalibre edilmedi" şeffaflığı eklendi

### Düzeltilen
- Veri kaynağı tek nokta arızası (CNBCe URL değişimi tüm akışı kıracaktı) — yedekli zincir ve yapılandırılmış hata raporu
- Yaş eşiği geçişlerinde tekrar tekrar sorulma sorunu — override geçmişi tablosu
- eSube hata senaryolarında sessiz başarısızlık — playbook ile şeffaf kurtarma

## [0.1.0] — 2026-04-XX

İlk sürüm.

### Eklenen
- Onboarding (5 soru → risk profili → ilk sepet)
- Aylık revize akışı (manuel + scheduled task)
- Türkiye Hayat eSube adapter (tam test edilmiş)
- 17 BES kurumu için stub adapter şablonu
- Slash komutlar: `/bes-onboard`, `/bes-revize`, `/bes-durum`
- Memory yapısı: `profile.md`, `current_basket.md`, `history/`
- Browser otomasyonu kuralları (son onay her zaman kullanıcıda)

[Unreleased]: https://github.com/OWNER/bes-pilot/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/OWNER/bes-pilot/releases/tag/v0.2.0
[0.1.0]: https://github.com/OWNER/bes-pilot/releases/tag/v0.1.0
