---
description: Mevcut BES sepetini, kalan hakkı, son revizeyi, son gerçekleşmiş getiriyi göster
---

`memory/users/{kısa_ad}/`'i oku ve özet çıkar. profile.md, current_basket.md ve son history dosyasından.

Şu formatta sun:

```markdown
## BES Pilot — {Kullanıcı} Durumu

**Profil**: {risk profili} (son hesaplama: {tarih})
**Yaş** (otomatik): {hesaplanan yaş, doğum tarihinden}
**Hedef emeklilik**: {tarih} (vade kalan: {N} yıl)
**Aktif sözleşme(ler)**: {sayı}, kurum(lar): {liste}

### Mevcut sepet
| Kod | Fon | Kurucu | % |
|---|---|---|---|
... (current_basket.md'den)

**Toplam**: %100
**Talep tarihi**: {tarih}
**Gerçekleşme tarihi**: {tarih}
**Kullanılan değişiklik hakkı**: N/12 (kalan: M)
**Bir sonraki otomatik revize**: {tarih}

### Son ay performansı (gerçekleşmiş)
- Sepet getirisi: %{X.XX} ({N} gün)
- BIST 100 aynı aralık: %{Y.YY}
- TÜFE: %{Z.ZZ}
- **Reel getiri**: %{X-Z} ({pozitif/negatif})
- **Benchmark farkı**: %{X-Y} ({üstü/altı})

### Son 3 ay özeti
- {YYYY-MM}: {tema}, karar: {revize/pas}, gerçek getiri: %X
- {YYYY-MM-1}: {tema}, karar: {revize/pas}, gerçek getiri: %X
- {YYYY-MM-2}: {tema}, karar: {revize/pas}, gerçek getiri: %X

### Aksiyon
- Şu anda yapacak bir şey yoksa, bir sonraki revizeye kadar bekle
- Manuel revize istiyorsan: `/bes-revize`
- Yıllık özet için: `/bes-yillik`
- Profili manuel güncellemek istiyorsan: "gelirim değişti" / "profil değiştirmek istiyorum" söyle
```

Profil yoksa: "Önce onboarding gerek, `/bes-onboard` çalıştır."

Profile.md'de "Şema sürümü" alanı yoksa veya 1 ise: kullanıcıya şemayı güncelleme önerisi sun (yaş alanı → doğum tarihi geçişi). Onay alırsa elle güncelle, almazsa eski şemayla devam et ama yaş otomatik hesaplanmadığı için yaş eşik kontrolü manuel olur.
