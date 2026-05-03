# Yıllık Özet

Her takvim yılının sonunda (veya yeni yılın ilk revizesinde) kullanıcıyla bir kez yapılan kapsamlı gözden geçirme. Aylık revizeden farkı: 12 ayın tüm kararlarını ve sonuçlarını tek pano'da topluyor, profili ve stratejiyi büyük resimde sorgu altına alıyor.

## Ne zaman tetiklenir?

- **Otomatik**: Her yılın **ilk** aylık revize tetiklemesinde (Ocak 1) → önce yıllık özet, sonra normal aylık akış
- **Manuel**: `/bes-yillik` komutuyla istediği zaman
- **Vergi sezonu yardımı**: Mart ortasında bir kez kullanıcıya hatırlat (vergi beyanı için BES bilgileri lazım olabilir)

## Akış

### Adım 1: Yıl içi tüm history dosyalarını oku

`memory/users/{kısa_ad}/history/{YYYY}-*.md` — yıl içindeki tüm aylık dosyalar.

12 ay için her birinde:
- Karar (revize / pas geç / köklü revize)
- Kullanılan hak
- Önceki sepet getirisi
- Tema

### Adım 2: Toplam yıl getirisini hesapla

> Bu hesap **basit ağırlıklı kümülatif** değil, her ayın getirisini çarpıyor (compound):
> 
> `yıllık_getiri = ∏ (1 + aylık_getiri/100) - 1`

Tabloyu çıkar:

| Ay | Sepet getirisi | BIST 100 | TÜFE | Reel | Benchmark farkı |
|---|---|---|---|---|---|
| 2026-01 | +2.34% | +1.89% | +1.20% | +1.14% | +0.45% |
| 2026-02 | +5.67% | +3.21% | +1.45% | +4.22% | +2.46% |
| ... | | | | | |
| **Yıllık compound** | +X.XX% | +Y.YY% | +Z.ZZ% | +A.AA% | +B.BB% |

### Adım 3: Hak kullanım analizi

- Yıl içinde kaç fon değişikliği yapıldı (toplam 12 üzerinden)
- Hangi aylarda pas geçildi
- Hangi revizeler geriye dönüp bakınca isabetli oldu, hangileri değildi

> "İsabet" tanımı: revize sonrası 3 ay içinde sepet benchmark üstü mü? Eğer evet, isabetli; değilse mantığı sorgula.

### Adım 4: Tema dağılımı

Yıl boyu hangi temalar kaç ay sepetin %30+'ında bulundu? Örnek:

```
- Teknoloji: 9 ay (Ocak-Eylül)
- Enerji: 4 ay (Mart-Haziran)
- Altın: 2 ay (Ekim, Kasım)
- Borçlanma TL: 12 ay (her zaman bir şekilde)
```

### Adım 5: Profil sorgulaması

Yıl içinde kullanıcının profili değişmiş mi?
- Yaş eşiği geçildi mi (otomatik veya manual)
- Manuel override yapılmış mı (profile.md "Override geçmişi"nden)
- "Daha agresif/defansif yap" gibi ad-hoc kullanıcı talepleri olmuş mu

Önümüzdeki yıl için soru:
- Bu profil hala doğru mu?
- Vade kısaldı, profil kayması düşünülmeli mi?

### Adım 6: Vergi notları (Türkiye'ye özgü)

> ⚠️ Bu bölüm **vergi danışmanlığı değil**, hatırlatmadır. Kullanıcı şüphedeyse SPK lisanslı yatırım danışmanına veya YMM'ye danışmalı.

- **BES devlet katkısı**: Yıl içinde toplam katkı payı × %30 (asgari ücret %25 tavanı, 2026 limiti farklı olabilir → DOĞRULANACAK her yıl)
- **Bireysel emeklilik primi gelir vergisi indirimi**: Çalışanlar için işveren BES priminin gelir vergisinden indirilmesi (kurum bordro üzerinden takip eder, kullanıcı bilse iyi olur)
- **Fon gider iadesi**: Sözleşmenin 6. yılından itibaren yıllık fon gider kesintisinin bir kısmı geri ödenir (BES Yönetmeliği Madde 22/A). BEFAS fonlarından alınan gider kesintileri **bu hesaplamaya dahil edilmez** — sadece kendi kurum fonlarından kesilenler hesaba girer
- **Erken çıkış vergisi**: 10 yıl dolmadan veya 56 yaş öncesi çıkış halinde stopaj uygulanır (oranlar dönem dönem değişir → DOĞRULANACAK)

### Adım 7: Önümüzdeki yıl için öneri

- Profil değişmeli mi? (yaş eşiği, kullanıcı isteği, performans yetersizliği)
- Strateji ayarı (örn. teknoloji üst üste 2 yıl underperform → momentum stratejisi sorgulanmalı)
- Tema beklentileri (makro: faiz patika, USDTRY yön)
- Hedef: yıl sonu birikim x değer X TL'ye ulaşma

### Adım 8: Kullanıcıya sun

```markdown
## BES Yıllık Özeti — {YYYY}

**Profil**: {profil} (yıl içi {değişiklik var mı?})
**Sözleşmeler**: {N} aktif, kurum(lar): {liste}
**Yıllık compound getiri**: %{X.XX}  ← BIST 100: %{Y.YY}, TÜFE: %{Z.ZZ}
**Reel getiri**: %{X-Z} ({pozitif/negatif})
**Hak kullanımı**: {N}/12 (en yoğun ay: {AY}, pas geçilen ay: {N})

### Tema dağılımı
{tablodaki gibi}

### En isabetli karar
- {AY}'da {KARAR} → sonraki 3 ayda benchmark üstü +X%

### Geriye dönüp baktığımızda hata
- {AY}'da {KARAR} → benchmark altı -Y%
- Sebep: {1-2 cümle teşhis}

### Bu yılın profil değişiklikleri
- {YYYY-MM}: {değişiklik}
- {YYYY-MM}: {değişiklik}

### Önümüzdeki yıl için (eğer farklıysa)
- {Yeni profil önerisi varsa: gerekçesi}
- {Strateji ayarı varsa: ne ve neden}
- {Vergi sezonu hatırlatma: Mart-Nisan beyan dönemine yakın}

### Vergi notları (hatırlatma)
- Yıl içi devlet katkısı tahmini: {hesap}
- Sözleşme yaş(lar)ı: en eski {N} yıl ({fon gider iadesi başladı/başlayacak: YYYY})
- Bu bilgiler vergi danışmanlığı değil — beyan için YMM'ye danış
```

### Adım 9: Yıllık özeti kaydet

`memory/users/{kısa_ad}/history/{YYYY}-yillik.md` adıyla yıl sonu özetini sakla. Sonraki yıllarda tarihsel referans olarak okunur.

## Yıl içi geriye dönüp bakma

Bu özet kullanıcıya sadece bir kez gösterilmez — sonraki yıllarda da çağırılabilir:
- "Geçen yıl Ekim'de hangi temadaydım?" → 2025 yıllık özetine bak
- "İlk yıl 2024 nasıl gitti?" → 2024 yıllık özetine bak
- Trend: 3+ yıllık verim varsa, profil ortalama yıllık getirisi vs. başlangıç beklentisi kıyaslanır

Bu, skill'in yıllar boyu birlikte çalıştığında değer getiren tarafıdır — tek seferlik bir araç değil, uzun süreli birikim ortağı.
