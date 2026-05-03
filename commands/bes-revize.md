---
description: Aylık BES sepet revizesi — manuel tetikleme
---

BES Pilot skill'inin **monthly review** moduna gir.

`references/monthly_review.md`'i takip et — 9 adımlık disiplinli akış:

1. `memory/users/{kısa_ad}/profile.md` + `current_basket.md` + son 3 ay history → durum çıkar
2. **Yaş kontrolü** (otomatik, doğum tarihinden hesaplanır). Eşik geçildiyse profile.md "Override geçmişi"ne bak — daha önce sorulduysa atla, sorulmadıysa kullanıcıya sor.
3. **Önceki sepetin gerçekleşmiş getirisini hesapla**: 
   - current_basket.md'deki "Talep tarihi pay fiyatı"nı al
   - TEFAS / eSube fon detayından bugünün pay fiyatını al
   - Ham getiri ve ağırlıklı sepet getirisini hesapla
   - BIST 100 (TCMB EVDS) ve TÜFE (TÜİK) benchmark'larıyla karşılaştır
   - current_basket.md'deki "Önceki sepetin gerçekleşmiş getirisi" bölümünü doldur
4. `references/fund_research.md` ile bu ayın piyasa verisini topla (yedekli zincir)
5. Karşılaştır → değişiklik gerekli mi? **Önceki sepet 2 ay üst üste benchmark altıysa stratejiyi sorgula.**
6. Eğer gerekiyorsa `references/basket_construction.md` ile yeni sepeti hesapla
7. Kullanıcıya öneriyle gel — formatına dikkat et (önceki performans + bu ayın önerisi)
8. Onay → `references/providers/{kurum}.md` ile eSube'ye gir → uygula. Hata oluşursa `references/error_recovery.md` playbook'unu kullan.
9. Yeni `history/{YYYY-MM}.md` yaz, `current_basket.md`'i güncelle (yeni sepet + yeni pay fiyatları)

Eğer profile.md yoksa onboarding'e yönlendir (`/bes-onboard`).

Eğer pas geçilecekse (değişiklik anlamlı değil), history dosyasına gene yaz: "değişiklik yapılmadı, gerekçesi: ..." + önceki sepetin gerçek getirisi yine hesaplanır (performans verisi zincirinde delik olmasın).

Eğer Ocak'taysak ve bu yılın **ilk** revizesi ise: önce `/bes-yillik`'i tetikle (geçen yılın özeti), sonra normal aylık akışa devam et.
