---
description: Yeni bir BES kurumu için adapter keşfini manuel başlat
---

BES Pilot skill'inin **Kurum keşif** moduna manuel olarak gir.

`references/adapter_discovery.md`'i takip et:

1. Kullanıcıya kurumunu sor (Türkiye Hayat hariç hangisi: Anadolu Hayat / Garanti / Allianz / Agesa / HDI Fiba / NN / AvivaSA / Vakıf / AXA / BNP Cardif / Bereket / Katılım / MetLife / QNB / Vienna Life / Zurich)

2. Mevcut adapter durumunu kontrol et:
   - `references/providers/{kurum}.md` varsa: "Bu kurum zaten test edilmiş, sepet kurmak için `/bes-revize` veya `/bes-onboard` kullanabilirsin." → çık
   - `{kurum}_draft.md` varsa: kullanıcıya "Bu kurum için keşif daha önce başlamış (son adım: {X}). Devam edelim mi yoksa baştan mı?"
   - Yoksa: yeni keşif başlat

3. Yeni keşif için:
   - `references/providers/_stub_template.md`'i `references/providers/{kurum_kisa_adi}_draft.md` olarak kopyala
   - Frontmatter doldur (`adapter_durumu: KEŞİF`, `keşif_başlangıcı: {bugün}`, `keşfeden: {kullanıcı kısa_ad}`)
   - `references/adapter_discovery.md`'deki 10 adımlık akışı yürüt

4. Akış sonunda kullanıcı "Tamam"a bastıktan ve "Talep alındı" mesajını gördükten sonra:
   - "Bu deneyimi kalıcı adapter olarak kaydedelim mi?" sor
   - Onay: `_draft.md` → `.md`, frontmatter `TEST EDİLMİŞ ✅`, README tablosu 🟡 → ✅
   - Topluluk katkısı için PR önerisi (CONTRIBUTING.md'ye yönlendir)

5. Yarım kalırsa `_draft.md` korunur; bir sonraki kullanımda kaldığı yerden devam edilebilir.

**Önemli**:
- Kullanıcının kredentialleri / TC kimlik / SMS koduna **asla dokunma**
- Sözleşme no, ad-soyad, birikim tutarı **drafte yazılmaz** — sadece UI yapısı, akış, JS davranışı kayda alınır
- Son "Tamam" tıkını her zaman kullanıcı basar (browser otomasyonu kuralları geçerli)
- Bu komut tek başına BES sepetini değiştirmez; bir keşif/değişiklik akışı yürütür ve sonunda gerçek revize bunun parçası olarak çalışır

Bu komut isteğe bağlı — yaygın akış: `/bes-onboard` veya `/bes-revize` zaten stub kuruma rastlayınca kullanıcıya keşif önerir. Manuel `/bes-kurum-kesfet` özellikle "şimdi vakit var, adapter'ı bitirelim" demek istediğinde kullanışlı.
