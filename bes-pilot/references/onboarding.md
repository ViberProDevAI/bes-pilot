# Onboarding — Çoktan Seçmeli Wizard Akışı

Yeni kullanıcı için **AskUserQuestion ile çoktan seçmeli** wizard akışı. Hedef: kullanıcıyı 2-3 dakikada tanı, **bütün sorular tıklanabilir seçenekli olsun**, açık-uçlu yazma minimum tut.

## 🚨 ZORUNLU: AskUserQuestion her soruda

Her soruda `AskUserQuestion` tool'u kullan. **Tool yoksa skill çalışamaz** — kullanıcıya açıkla: "AskUserQuestion tool yok, çoktan seçmeli wizard yapamam. Düz metinle sorabilirim ama UX yetersiz olur — devam edeyim mi?" Cevap "evet" değilse skill'i durdur.

**Birden fazla ilişkili soruyu BATCH halinde sor** — `AskUserQuestion` tek çağrıda 2-3 soru destekliyor. Kullanıcının click sayısını azalt.

## Soru sırası — KURUM EN BAŞTA

Skill'in adapter seçimini erken yapabilmesi için **kurum sorusu önce gelir**. Stub kurum ise keşif modu, test edilmiş kurum ise normal akış.

---

### Soru 1 — Kurum (sözleşme nerede?)

**AskUserQuestion** çağır:

```
question: "BES sözleşmen hangi kurumda?"
options:
  - "Türkiye Hayat ve Emeklilik" (✅ tam test edilmiş)
  - "Anadolu Hayat Emeklilik" (🟡 keşif modu)
  - "Garanti Emeklilik" (🟡)
  - "Allianz Yaşam" (🟡)
  - "Allianz Hayat" (🟡)
  - "Agesa" (🟡)
  - "HDI Fiba" (🟡)
  - "AvivaSA" (🟡)
  - "NN Hayat" (🟡)
  - "Vakıf Emeklilik" (🟡)
  - "AXA Hayat" (🟡)
  - "BNP Paribas Cardif" (🟡)
  - "Bereket" (🟡)
  - "Katılım Emeklilik" (🟡)
  - "MetLife" (🟡)
  - "QNB Sağlık ve Hayat" (🟡)
  - "Vienna Life" (🟡)
  - "Zurich" (🟡)
  - "Birden fazla kurumda var"
multiSelect: false
```

**Eğer "Birden fazla"** seçildiyse: ikinci `AskUserQuestion` ile ana kurumu seç (öncelikli olarak yöneteceğimiz). Diğerleri için sonraki revize.

**Eğer Türkiye Hayat seçildiyse**: tam test edilmiş adapter var, normal akışa geç.

**Eğer stub kurum seçildiyse** (THE dışı): kullanıcıya bildir:
```
question: "{Kurum} için adapter henüz test edilmedi. Şu an iki seçenek var:"
options:
  - "Birlikte keşfedelim — 30-60 dk ekran ekran, sonunda kalıcı adapter"
  - "Bu sefer manuel — sepet öneririm, sen elle eSube'de uygularsın"
```

Detay: `references/adapter_discovery.md`

---

### Soru 2 — Sözleşme sayısı + tipi

**AskUserQuestion** çağır:

```
question: "Bu kurumda kaç aktif sözleşmen var?"
options:
  - "1 sözleşme"
  - "2 sözleşme"
  - "3+ sözleşme"
```

Eğer 2+ ise ek soru (batch içinde olabilir):

```
question: "Sözleşmelerden 18 yaş altı kumbara hesabı var mı?"
options:
  - "Yok, hepsi yetişkin BES"
  - "Evet, 1 tane çocuk için kumbara"
  - "Evet, 2+ çocuk kumbara"
```

Kumbara hesabı = ekstra ihtiyat. Risk profili agresif olsa bile kullanıcının açık onayı şart.

---

### Soru 3 — Doğum tarihi + Hedef emeklilik yaşı (vade hesabı)

**AskUserQuestion** batch çağır:

```
question 1: "Doğum yılın hangi aralıkta?"
options:
  - "1980 ve öncesi"
  - "1981-1990"
  - "1991-2000"
  - "2001-2010"
  - "Tam tarihi yazmak istiyorum (DD.MM.YYYY)"

question 2: "BES'i kaç yaşında bozdurmayı planlıyorsun?"
options:
  - "56 (yasal asgari)"
  - "60"
  - "65"
  - "70+"
  - "Henüz emin değilim (defaultu 56 al)"
```

Eğer "Tam tarihi yazmak istiyorum" seçildiyse, sonraki turda free-text doğum tarihi al, parse et. Tam tarih `profile.md`'ye yazılır (yaş eşiği hesabı için kritik).

**Çıkarım kuralları (vade)**:
- Vade ≥ 20 yıl → "uzun" (agresife eğilim)
- 10-20 yıl → "orta"
- < 10 yıl → "kısa" (defansife eğilim)

---

### Soru 4 — Aylık katkı + Mevcut birikim (DCA gücü)

**AskUserQuestion** batch:

```
question 1: "Aylık BES'e ne kadar koyuyorsun?"
options:
  - "<1000 TL"
  - "1000-3000 TL"
  - "3000-7000 TL"
  - "7000-15000 TL"
  - "15000+ TL"
  - "Düzensiz, bazen koyuyorum bazen koymuyorum"

question 2: "Şu ana kadar BES'te yaklaşık ne kadar birikti (devlet katkısı dahil)?"
options:
  - "<50K TL"
  - "50K-200K TL"
  - "200K-500K TL"
  - "500K-1M TL"
  - "1M+ TL"
  - "Bilmiyorum (eSube'de bakalım)"
```

**Çıkarım kuralları**:
- Aylık katkı 7K+ TL ve birikim 200K+ → DCA gücü "yüksek" (+1 puan)
- Düzensiz → DCA gücü "düşük" (-1 puan)
- Diğer → "orta" (0)

---

### Soru 5 — Kayıp toleransı (psikolojik — SERT OVERRIDE)

**AskUserQuestion** çağır:

```
question: "Diyelim ki BES portföyün tek bir ayda %15 düştü, gazete manşetlerinde 'kriz' yazıyor. İlk tepkin ne olur?"
options:
  - "A: Hemen panikle satışa çık, kaybı durdur, defansife geç"
  - "B: Bekle ama uykum kaçar; 1-2 ay sonra hala düşükse değiştiririm"
  - "C: Düşüşte yeni para koyarım, fırsat bilirim"
```

⚠️ **A cevabı SERT OVERRIDE**: Toplam puan ne olursa olsun **AGRESİF profil yasak**. risk_profile.md'deki override kuralı.

---

### Soru 6 — Hedef beklenti

**AskUserQuestion** çağır:

```
question: "BES'ten beklentin ne?"
options:
  - "A: Sadece devlet katkısını alıp enflasyon kadar koruyayım yeter"
  - "B: Reel olarak (enflasyon üstü) makul bir getiri (yıllık enflasyon + %5-10)"
  - "C: Agresif büyüme — emekli olduğumda iyi para olsun, oynaklığa razıyım"
```

---

### Puan tablosu

| Soru | A puan | B puan | C puan |
|---|---|---|---|
| 3 (vade) | < 10 yıl: -2 | 10-20: 0 | ≥ 20: +2 |
| 4 (DCA gücü) | Düşük: -1 | Orta: 0 | Yüksek: +1 |
| 5 (kayıp tepkisi) | A: -3 + AGRESİF YASAK | B: 0 | C: +3 |
| 6 (hedef) | A: -2 | B: 0 | C: +2 |

**Toplam**:
- ≤ -3 → **DEFANSİF**
- -2 ile +2 → **DENGELİ**
- ≥ +3 → **AGRESİF** (Soru 5=A ise yasak, DENGELİ'ye düş)

---

## Sonraki adımlar — OTOMATİK, ARA CHECKPOINT YOK

Sorular bitti. Aşağıdaki adımlar **kesintisiz** çalışır, kullanıcıya "devam edeyim mi?" sorma:

1. **`profile.md` yaz** — `memory/users/{kısa_ad}/profile.md` (template'i kopyala, doldur)
2. **Risk profili hesapla** — `references/risk_profile.md` ile temel allokasyon
3. **Piyasa verisi topla** — `references/fund_research.md` 4 kademeli yedekli zinciri **WebSearch + WebFetch ile** çalıştır
4. **Sepet kur** — `references/basket_construction.md` algoritması
5. **Sepet onayı al** — sadece bu noktada AskUserQuestion ile tekrar dur:

```
question: "Senin için kurduğum sepet bu. Onaylıyor musun?"
options:
  - "Onayla, eSube'ye gir ve uygula"
  - "Detayını göster (her fonun gerekçesi)"
  - "Daha defansif yap"
  - "Daha agresif yap"
  - "İptal, sadece kaydet, sonra düşüneyim"
```

6. **Onaylandıysa**: `references/providers/{kurum}.md`'i takip ederek browser otomasyonuyla eSube'ye gir → fon dağılım sayfasına git → BEFAS aç → fonları seç → yüzdeleri yaz → toplam doğrula → "Tamam"a kullanıcı bassın diyene kadar **durmadan** ilerle.

---

## Profili kaydet

Soru-cevap bittiğinde `memory/users/{kısa_ad}/profile.md`'ye yaz. `memory/_template/profile.md`'i başlangıç noktası olarak kopyala, tüm `{...}` placeholder'larını cevaplarla doldur. Kişisel kullanıcı verisi sadece bu dosyada — repo'ya gitmez (`.gitignore`).

## AskUserQuestion gerçekten yoksa

Eğer Cowork/CLI sürümünde AskUserQuestion mevcut değilse, fallback:

```
[Skill]: Üzgünüm, bu Claude sürümünde çoktan seçmeli soru tool'u (AskUserQuestion) yok.
Düz metinle sorabilirim ama deneyim daha hantal olur. Devam edeyim mi?
```

Devam onayı geldiyse: aynı seçenekleri **numaralı liste** olarak yaz, kullanıcı sayı ile cevaplasın. Çıkarım kuralları aynı, sadece UI farklı.
