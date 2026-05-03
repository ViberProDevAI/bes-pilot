#!/usr/bin/env python3
"""
schedule_monthly.py — BES Pilot için aylık scheduled task kurma

Kullanım: python schedule_monthly.py {user_kisa_ad}

Bu script, her ayın 1'inde Cowork'ün scheduled-tasks MCP'si üzerinden
BES Pilot skill'ini tetikler. Tetiklenen prompt skill'in monthly_review
moduna girip kullanıcıya bu ayın özetini sunar.

Eğer scheduled-tasks MCP yoksa: macOS'ta launchd, Linux'ta cron için
örnek konfig çıkarır.
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

USAGE = """
BES Pilot — Aylık Scheduled Task Kurulumu

Kullanım:
  python schedule_monthly.py {user_kisa_ad}

Örnek:
  python schedule_monthly.py {kısa_ad}

Bu script, scheduled-tasks MCP varsa direkt task oluşturur.
Yoksa cron/launchd örnek konfig'i ekrana yazar.
"""


def make_prompt(user_short_name: str) -> str:
    """BES Pilot skill'ini tetikleyecek aylık prompt"""
    return (
        f"BES Pilot aylık revize zamanı geldi (kullanıcı: {user_short_name}). "
        f"references/monthly_review.md'i takip et: profili oku, "
        f"bu ayın piyasa verisini topla, sepetimi gözden geçir, "
        f"değişiklik gerekiyorsa öneriyle gel, gerekmiyorsa pas geç de. "
        f"Mevcut sözleşmelerime ve önceki revizelere bak, ona göre çalış."
    )


def emit_cron(user_short_name: str, prompt: str) -> str:
    """Cron için örnek konfig"""
    return f"""
# BES Pilot aylık revize — {user_short_name}
# Her ayın 1'inde sabah 9'da çalışsın
0 9 1 * * cd ~/skills/bes-pilot && claude --print "{prompt}" >> ~/bes-pilot.log 2>&1
"""


def emit_launchd(user_short_name: str, prompt: str) -> str:
    """macOS launchd plist"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.user.bes-pilot.{user_short_name}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/claude</string>
    <string>--print</string>
    <string>{prompt}</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Day</key><integer>1</integer>
    <key>Hour</key><integer>9</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>/tmp/bes-pilot-{user_short_name}.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/bes-pilot-{user_short_name}.err</string>
</dict>
</plist>
"""


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(USAGE)
        sys.exit(0)

    user_short_name = sys.argv[1]
    prompt = make_prompt(user_short_name)

    # Memory yolu kontrol
    memory_path = Path(__file__).parent.parent / "memory" / "users" / user_short_name
    if not memory_path.exists():
        print(f"⚠️  Uyarı: {memory_path} bulunamadı. Önce onboarding yap:")
        print(f"   skill'i çağır → 'BES sepetimi kur'")
        print()

    print("=" * 60)
    print("BES Pilot Scheduled Task — kurulum talimatları")
    print("=" * 60)
    print()
    print(f"Kullanıcı: {user_short_name}")
    print(f"Tetikleme: Her ayın 1'inde 09:00")
    print()
    print("Prompt:")
    print(f"  {prompt}")
    print()
    print("---")
    print("Seçenek 1: Cowork scheduled-tasks MCP (Cowork'teyken):")
    print("  Skill'in içinde Claude'a şu komutu söyle:")
    print(f'  "Aylık BES revize için scheduled task oluştur, kullanıcı: {user_short_name}, ayın 1\'inde 09:00, prompt: {prompt}"')
    print()
    print("---")
    print("Seçenek 2: macOS launchd:")
    plist_path = Path.home() / "Library/LaunchAgents" / f"com.user.bes-pilot.{user_short_name}.plist"
    print(f"  Aşağıdaki plist'i şuraya yaz: {plist_path}")
    print(emit_launchd(user_short_name, prompt))
    print(f"  Sonra: launchctl load {plist_path}")
    print()
    print("---")
    print("Seçenek 3: Linux/macOS cron:")
    print("  crontab -e ile aşağıdaki satırı ekle:")
    print(emit_cron(user_short_name, prompt))
    print()
    print("=" * 60)
    print("Not: Manuel /bes-revize komutu da her zaman çalışır.")
    print("Otomatik tetikleme + manuel komut her ikisi de aktif.")
    print("=" * 60)


if __name__ == "__main__":
    main()
