# {Tam Ad} — BES Profili

**Son güncelleme**: YYYY-MM-DD
**Şema sürümü**: 2

## Demografi
- **Doğum tarihi**: YYYY-MM-DD  ← yaş bunun üzerinden otomatik hesaplanır, manuel "yaşım değişti" demeye gerek yok
- Hedef emeklilik yaşı: 
- Hedef emeklilik tarihi: YYYY-MM-DD  ← doğum tarihi + hedef yaştan türetilir, doğrulama için yaz

## Finansal
- Aylık katkı (TL): 
- Aylık katkı son güncelleme: YYYY-MM-DD  ← gelir değişiminde bu tarihi de güncelle
- Mevcut toplam birikim (devlet katkısı dahil, TL): 
- Birikim son güncelleme: YYYY-MM-DD
- DCA gücü: düşük / orta / yüksek  ← onboarding.md kuralı

## Risk profili
- Soru 1 (vade) puanı: 
- Soru 2 (DCA) puanı: 
- Soru 3 (kayıp tepkisi) cevabı + puan: 
- Soru 4 (hedef) cevabı + puan: 
- **Toplam puan**: 
- **Risk profili**: defansif / dengeli / agresif
- Kayıp toleransı override aktif mi: evet/hayır
- Profil son hesaplama: YYYY-MM-DD

## BES sözleşmeleri

| # | Sözleşme No | Kurum | Plan adı | Kim için | Açılış tarihi | BEFAS aktif | Özel notlar |
|---|---|---|---|---|---|---|---|
| 1 | | | | | YYYY-MM-DD | evet/hayır | |
| 2 | | | | | | | |

## Yıllık takvim

- **Hak yılı**: Devlet katkısı için sözleşme yıldönümü (her sözleşme için ayrı). En eski sözleşmenin yıldönümü: YYYY-MM-DD
- **Fon değişiklik hakkı**: Her takvim yılında 12 (Genelge 2026/1, Madde 8/Y). Ocak 1'de sıfırlanır.
- **Bir sonraki revize**: YYYY-MM-DD
- **Yıl içi kullanılan hak**: 0/12

## Otomatik sürükleme — yaş eşik haritası

Aylık revize her açıldığında doğum tarihinden yaş hesaplanır. Şu eşikler kontrol edilir:

| Mevcut profil | Yaş eşiği geçilirse | Yeni öneri |
|---|---|---|
| AGRESİF | 40 | DENGELİ'ye geçiş öner |
| DENGELİ | 55 | DEFANSİF'e geçiş öner |
| (her seviye) | Kalan vade < 10 yıl | DEFANSİF'e geçiş öner |

> ⚠️ Eşikler **konvansiyonel emekliliğe-yakın korunma** mantığına dayanır (uzun vadede risk ödülü, kısa vadede koruma). Yaş == kader değil — kullanıcı override edebilir, ama skill her geçişte bir kez sorar ve cevabı buraya not eder.

## Kullanıcı override geçmişi

Eşik öneriler kabul/red edildiğinde buraya not at:

| Tarih | Skill önerisi | Kullanıcı kararı | Sebep |
|---|---|---|---|
| YYYY-MM-DD | "40 oldun, agresif → dengeli" | Reddedildi | "Vadem hala 25 yıl, riske devam" |

## Notlar
- 
