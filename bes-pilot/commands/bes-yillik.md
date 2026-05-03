---
description: Yıllık BES özet — yıl içi karar, getiri, hak kullanımı analizi
---

BES Pilot skill'inin **yıllık özet** moduna gir.

`references/annual_review.md`'i takip et. Adımlar:

1. `memory/users/{kısa_ad}/history/{YYYY}-*.md` dosyalarının hepsini oku (12 ay)
2. Compound yıllık getiri hesapla
3. BIST 100 ve TÜFE benchmark'ları topla (TCMB EVDS ve TÜİK)
4. Hak kullanım dağılımını çıkar
5. Tema dağılımını hesapla
6. Profil değişikliklerini özetle (profile.md "Override geçmişi"nden)
7. Vergi sezonu hatırlatma notları (Mart-Nisan beyan dönemine yakınsa öne çıkar)
8. Kullanıcıya sun: yıllık özet formatında
9. `memory/users/{kısa_ad}/history/{YYYY}-yillik.md` adıyla kaydet

**Önemli**: Bu bir vergi danışmanlığı veya yatırım önerisi değil. Sadece geriye dönüp bakma + ileri planlama destek aracı. Kullanıcı vergi konularında YMM'ye danışmalı.

Komut yıl içinde herhangi bir zaman çağrılabilir, kullanıcı tipik olarak Ocak başında veya Mart vergi sezonunda kullanır. Eğer yıl tamamlanmadıysa (örn. Haziran'dayız 2026 için), sadece yıl başından bugüne kadar olan veriyle çalış, "henüz tam yıl değil" notu düş.
