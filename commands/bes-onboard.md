---
description: Yeni kullanıcı için BES profili çıkar ve ilk sepeti kur
---

BES Pilot skill'inin onboarding moduna gir.

`references/onboarding.md`'i takip et: **doğum tarihi + 5 soruyla** kullanıcının profilini çıkar (vade, finansal, kayıp toleransı, hedef, BES kurumu/sözleşmeleri). Yaş manuel kaydedilmez — doğum tarihinden otomatik hesaplanır.

Profili `memory/users/{kısa_ad}/profile.md`'ye yaz (template'i `memory/_template/profile.md`'den kopyala, şema sürümü 2).

Sonra:
1. `references/risk_profile.md` ile risk profilini hesapla (defansif/dengeli/agresif). Override kuralı: Soru 3=A → AGRESİF asla.
2. `references/fund_research.md` ile bu hafta + bu ayın piyasa verisini topla (yedekli zincir: CNBCe → besfongetirileri → fintables → TEFAS → manuel)
3. `references/basket_construction.md` ile ilk sepeti kur
4. Kullanıcıya sepeti göster, onay al
5. `references/providers/{kurum}.md`'i takip ederek eSube'ye gir ve uygula
6. **Her fonun talep tarihi pay fiyatını** eSube fon detayından veya TEFAS'tan oku, `current_basket.md`'ye yaz (gelecek revizenin gerçek getiri hesabı için kritik)
7. `current_basket.md` ve `history/{YYYY-MM}.md`'i yaz
8. `scripts/schedule_monthly.py` ile aylık scheduled task kur (kullanıcı izin verirse)

Önemli: 
- Kullanıcının kim olduğunu en başta sor (kısa_ad için), eğer zaten varsa onaylat
- Kayıp toleransı override kuralını uygula (`references/risk_profile.md`'de detay)
- 18 yaş altı kumbara hesabı varsa profil önerisini muhafazakar tut, kullanıcı açıkça onaylamadıkça agresif yapma
