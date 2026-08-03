#!/usr/bin/env python3
"""Check Proteinbase competitions page for open entries."""

from __future__ import annotations

import re
import sys
import urllib.request
from datetime import datetime, timezone

URL = "https://proteinbase.com/competitions"


def main() -> None:
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "protein-lab-monitor/1.0"})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"ERROR fetching {URL}: {e}")
        sys.exit(1)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ended = len(re.findall(r"Ended", html))
    open_entries = re.findall(r"Submissions Open|Submission Open|Currently open", html, re.I)

    print(f"Checked: {URL}")
    print(f"Time: {now}")
    print(f"Ended competitions detected: {ended}")
    if open_entries:
        print(f"Open submission markers: {open_entries[:3]}")
        print("ACTION: Review site — competition may be open.")
    else:
        print("MODE: practice-and-wait (no open submission window detected)")
        print("See binder_design/COMPETITION_STATUS.md for strategy.")


if __name__ == "__main__":
    main()
