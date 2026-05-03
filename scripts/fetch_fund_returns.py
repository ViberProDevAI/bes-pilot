#!/usr/bin/env python3
"""
fetch_fund_returns.py — Haftalık BES fon getirilerini topla (yedekli zincir)

Kullanım:
    python fetch_fund_returns.py            # markdown çıktı
    python fetch_fund_returns.py --json     # JSON çıktı
    python fetch_fund_returns.py --debug    # ek tanılama logu

Veri kaynakları (öncelik sırasıyla denenecek):
    1. CNBCe — haftalık derleme yazısı (en güvenilir)
    2. besfongetirileri.com — aylık tablo (haftalık AJAX gerektirir)
    3. fintables.com — yedek (büyük HTML)
    4. TEFAS — son otomatik çare

Tüm zincir başarısız olursa: sıfır veri yerine açık başarısızlık raporu döner —
skill bu raporla kullanıcıya manuel girişi sorabilir.

Tasarım kuralı: hata yutma yasak. Her başarısız kaynak için neden başarısız
olduğu (HTTP hata kodu, parser eşleşmesi yok, timeout) raporda görünür.
"""

import sys
import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


@dataclass
class SourceResult:
    """Tek bir veri kaynağının sonucu — başarı veya yapılandırılmış başarısızlık."""
    source: str
    url: Optional[str] = None
    success: bool = False
    error_kind: Optional[str] = None  # "http", "timeout", "parse", "empty", "rate_limit"
    error_detail: Optional[str] = None
    pension_top_10: list = field(default_factory=list)  # [(name, pct_str), ...]
    raw_chars_seen: int = 0


def fetch(url: str, timeout: int = 15) -> tuple[str, Optional[SourceResult]]:
    """HTTP GET — User-Agent set ederek. Başarısızlıkta yapılandırılmış hata döner."""
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", errors="replace")
            return body, None
    except HTTPError as e:
        kind = "rate_limit" if e.code in (403, 429) else "http"
        return "", SourceResult(
            source="(fetch)",
            url=url,
            error_kind=kind,
            error_detail=f"HTTP {e.code} {e.reason}"
        )
    except URLError as e:
        kind = "timeout" if "timed out" in str(e.reason).lower() else "network"
        return "", SourceResult(
            source="(fetch)",
            url=url,
            error_kind=kind,
            error_detail=str(e.reason)
        )
    except Exception as e:
        return "", SourceResult(
            source="(fetch)",
            url=url,
            error_kind="unknown",
            error_detail=f"{type(e).__name__}: {e}"
        )


def try_cnbce() -> SourceResult:
    """Kaynak 1: CNBCe haftalık derleme yazısı."""
    base = "https://www.cnbce.com/etiket/yatirim-fonlari"
    html, err = fetch(base)
    if err:
        err.source = "cnbce-list"
        return err

    matches = re.findall(
        r'href="(/borsa/en-cok-kazandiran-ve-kaybettiren-fonlar-[^"]+)"',
        html
    )
    if not matches:
        return SourceResult(
            source="cnbce-list",
            url=base,
            error_kind="parse",
            error_detail="Haftalık yazı linki bulunamadı (HTML şablonu değişmiş olabilir)",
            raw_chars_seen=len(html),
        )

    article_url = f"https://www.cnbce.com{matches[0]}"
    article_html, err = fetch(article_url)
    if err:
        err.source = "cnbce-article"
        err.url = article_url
        return err

    pension_section = re.search(
        r'(en çok kazandıran emeklilik fon.*?)(en çok kayb|</article>)',
        article_html, re.IGNORECASE | re.DOTALL
    )
    if not pension_section:
        return SourceResult(
            source="cnbce-article",
            url=article_url,
            error_kind="parse",
            error_detail="Yazı içinde 'emeklilik fon' bölümü bulunamadı",
            raw_chars_seen=len(article_html),
        )

    text = pension_section.group(1)
    items = re.findall(
        r'([A-ZÇĞİÖŞÜ][A-Za-zÇĞİÖŞÜçğıöşü\s\.\-]+?'
        r'(?:EYF|Emeklilik Yatırım Fonu|EMEKLİLİK YATIRIM FONU))[^%]+?'
        r'([\d,\.]+)\s*%',
        text
    )
    if not items:
        return SourceResult(
            source="cnbce-article",
            url=article_url,
            error_kind="empty",
            error_detail="Bölüm bulundu ama fon listesi parse edilemedi",
            raw_chars_seen=len(text),
        )

    return SourceResult(
        source="cnbce-article",
        url=article_url,
        success=True,
        pension_top_10=[(n.strip(), p) for n, p in items[:10]],
        raw_chars_seen=len(text),
    )


def try_besfongetirileri() -> SourceResult:
    """
    Kaynak 2: besfongetirileri.com — aylık tablo.
    Hafta sekmesi AJAX, düz fetch'le aylık görünür. Aylık veri de değerli.
    """
    url = "https://www.besfongetirileri.com/"
    html, err = fetch(url)
    if err:
        err.source = "besfongetirileri"
        return err

    # Sitenin ay sekmesi tablosundan satırları çıkar.
    # Bilinen DOM yapısı: <tr> <td>kod</td> <td>fon adı</td> <td>%X.XX</td>
    rows = re.findall(
        r'<tr[^>]*>\s*<td[^>]*>([A-Z]{2,4})</td>\s*'
        r'<td[^>]*>([^<]+)</td>\s*'
        r'<td[^>]*>([\-\d,\.]+)\s*%?</td>',
        html
    )

    if not rows:
        return SourceResult(
            source="besfongetirileri",
            url=url,
            error_kind="parse",
            error_detail="Aylık tablo satırları bulunamadı (DOM değişmiş olabilir)",
            raw_chars_seen=len(html),
        )

    items = [(f"{name.strip()} ({code})", pct) for code, name, pct in rows[:10]]
    return SourceResult(
        source="besfongetirileri",
        url=url,
        success=True,
        pension_top_10=items,
        raw_chars_seen=len(html),
    )


def try_fintables() -> SourceResult:
    """
    Kaynak 3: fintables.com — büyük HTML, yedek olarak.
    Bu kaynağı tam parse etmek script ölçeğinde zor (>300K char), ama
    erişilebilirlik kontrolü olarak kullanılır: site açık mı, içerik var mı.
    """
    url = "https://fintables.com/fonlar/emeklilik-fonlari/getiri"
    html, err = fetch(url, timeout=25)
    if err:
        err.source = "fintables"
        return err

    if len(html) < 5000:
        return SourceResult(
            source="fintables",
            url=url,
            error_kind="empty",
            error_detail=f"Sayfa çok kısa ({len(html)} char), büyük olasılıkla bot block",
            raw_chars_seen=len(html),
        )

    # Burada fon adı + yüzde aramaya çalışıyoruz, ama büyük dosyada
    # tam parse skill'in kendi subagent çağrısına bırakılmalı.
    return SourceResult(
        source="fintables",
        url=url,
        success=True,
        pension_top_10=[],  # parse yok, yalnızca erişim doğrulaması
        error_kind="partial",
        error_detail=(
            "Sayfa erişilebilir ama scriptte tam parse yok. "
            "Skill subagent'a fetch'le açtırıp top 10'u çıkartabilir."
        ),
        raw_chars_seen=len(html),
    )


def try_tefas() -> SourceResult:
    """
    Kaynak 4: TEFAS son çare — pay fiyatı doğrulama için kullanılır,
    haftalık top performer için ideal değil ama erişilebilirliği kontrol et.
    """
    url = "https://www.tefas.gov.tr/FonAnaSayfa.aspx"
    html, err = fetch(url)
    if err:
        err.source = "tefas"
        return err

    if "TEFAS" not in html.upper() and "FON" not in html.upper():
        return SourceResult(
            source="tefas",
            url=url,
            error_kind="empty",
            error_detail="TEFAS sayfası beklenen başlık içermiyor",
            raw_chars_seen=len(html),
        )

    return SourceResult(
        source="tefas",
        url=url,
        success=True,
        pension_top_10=[],
        error_kind="partial",
        error_detail="TEFAS erişilebilir; pay fiyatı sorgusu için skill detay sayfasını çağırmalı",
        raw_chars_seen=len(html),
    )


def chain_fetch(debug: bool = False) -> dict:
    """Yedekli zinciri sırayla çalıştır, ilk başarılı sonucu kullan, hepsini raporla."""
    attempts = []

    for fn in (try_cnbce, try_besfongetirileri, try_fintables, try_tefas):
        result = fn()
        attempts.append(asdict(result))
        if debug:
            print(f"[debug] {result.source}: success={result.success} "
                  f"err={result.error_kind} ({result.error_detail or ''})",
                  file=sys.stderr)
        if result.success and result.pension_top_10:
            return {
                "ts": datetime.now().isoformat(),
                "primary": result.source,
                "data": {
                    "pension_top_10": result.pension_top_10,
                    "url": result.url,
                },
                "attempts": attempts,
            }

    # Hiçbiri başarılı olmadı
    return {
        "ts": datetime.now().isoformat(),
        "primary": None,
        "data": None,
        "attempts": attempts,
        "fallback_advice": (
            "Otomatik kaynaklar başarısız. Skill'in kullanıcıyla manuel veri girişi "
            "akışına geçmesi gerekir: tarayıcıda besfongetirileri.com 'Hafta' sekmesini "
            "aç ve top 10 fonu söyle (kod + getiri)."
        ),
    }


def render_markdown(payload: dict) -> str:
    out = []
    out.append(f"# BES Fon Getirileri — {payload['ts'][:10]}")
    out.append("")

    if payload["primary"]:
        out.append(f"**Birincil kaynak**: `{payload['primary']}`")
        data = payload["data"]
        if data and data.get("pension_top_10"):
            out.append("")
            out.append("## Top 10 Kazandıran Emeklilik Fonu")
            out.append("")
            out.append("| # | Fon | Getiri |")
            out.append("|---|---|---|")
            for i, (name, pct) in enumerate(data["pension_top_10"], 1):
                out.append(f"| {i} | {name} | %{pct} |")
            out.append("")
            if data.get("url"):
                out.append(f"_Kaynak: {data['url']}_")
    else:
        out.append("⚠️ **Tüm otomatik kaynaklar başarısız.**")
        out.append("")
        out.append(payload["fallback_advice"])

    out.append("")
    out.append("## Kaynak deneme raporu")
    out.append("")
    out.append("| Kaynak | Başarı | Hata türü | Detay |")
    out.append("|---|---|---|---|")
    for a in payload["attempts"]:
        ok = "✅" if a["success"] and a.get("pension_top_10") else "❌"
        out.append(
            f"| {a['source']} | {ok} | {a.get('error_kind') or '-'} | "
            f"{(a.get('error_detail') or '-')[:60]} |"
        )
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    json_mode = "--json" in args
    debug = "--debug" in args

    print("=" * 60, file=sys.stderr)
    print("BES Fon Getirileri — yedekli zincir", file=sys.stderr)
    print(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(file=sys.stderr)

    payload = chain_fetch(debug=debug)

    if json_mode:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(payload))

    # Çıkış kodu: tüm zincir başarısızsa 1 (skript çağıran rahatça branch'lar)
    sys.exit(0 if payload["primary"] else 1)


if __name__ == "__main__":
    main()
