#!/usr/bin/env python3
"""Append approved conversation feedback to local style memory."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from style_utils import load_json, write_json


def main(argv):
    parser = argparse.ArgumentParser(description="Update style memory after explicit user approval or long-term feedback wording.")
    parser.add_argument("--memory-dir", default="assets/style_memory")
    parser.add_argument("--accepted", action="append", default=[], help="Reusable accepted style trait.")
    parser.add_argument("--rejected", action="append", default=[], help="Reusable rejected style trait.")
    parser.add_argument("--source", default="user_feedback")
    parser.add_argument("--note", default="")
    parser.add_argument("--approved", action="store_true", help="Required: user approved saving this as reusable style memory.")
    parser.add_argument("--list", action="store_true", help="List current style memory and exit.")
    parser.add_argument("--remove", help="Remove a trait from accepted and rejected lists in style_profile.json.")
    args = parser.parse_args(argv)

    memory_dir = Path(args.memory_dir).resolve()
    profile_path = memory_dir / "style_profile.json"
    if args.list:
        profile = {"accepted_traits": [], "negative_preferences": []}
        if profile_path.exists():
            try:
                profile = load_json(profile_path)
            except Exception as exc:
                print(json.dumps({"status": "error", "reason": f"Could not read style_profile.json: {exc}"}, ensure_ascii=True, indent=2))
                return 1
        print(json.dumps({"status": "ok", "profile": str(profile_path), "style_memory": profile}, ensure_ascii=True, indent=2))
        return 0

    if args.remove:
        if not profile_path.exists():
            print(json.dumps({"status": "skipped", "reason": "style_profile.json does not exist."}, ensure_ascii=True, indent=2))
            return 0
        profile = load_json(profile_path)
        removed = []
        for key in ("accepted_traits", "negative_preferences"):
            values = profile.get(key, [])
            if args.remove in values:
                profile[key] = [v for v in values if v != args.remove]
                removed.append(key)
        write_json(profile_path, profile)
        print(json.dumps({"status": "ok", "removed_from": removed, "profile": str(profile_path), "manual_note": "Review user_feedback_log.md and negative_preferences.md manually if you need a fully clean history."}, ensure_ascii=True, indent=2))
        return 0

    if not args.approved:
        print(json.dumps({"status": "skipped", "reason": "Use --approved only after user approval or explicit long-term wording."}, ensure_ascii=True, indent=2))
        return 0

    memory_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now().isoformat(timespec="seconds")
    log_path = memory_dir / "user_feedback_log.md"
    neg_path = memory_dir / "negative_preferences.md"

    entry = [f"## {now}", "", f"- Source: {args.source}"]
    if args.note:
        entry.append(f"- Note: {args.note}")
    for item in args.accepted:
        entry.append(f"- Accepted: {item}")
    for item in args.rejected:
        entry.append(f"- Rejected: {item}")
    entry.append("")
    with log_path.open("a", encoding="utf-8") as f:
        f.write("\n".join(entry))

    if args.rejected:
        with neg_path.open("a", encoding="utf-8") as f:
            for item in args.rejected:
                f.write(f"- {item}\n")

    profile = {"accepted_traits": [], "negative_preferences": [], "source": "style_memory", "scope": "research_html_slides"}
    if profile_path.exists():
        try:
            profile = load_json(profile_path)
        except Exception:
            pass
    profile.setdefault("accepted_traits", [])
    profile.setdefault("negative_preferences", [])
    for item in args.accepted:
        if item not in profile["accepted_traits"]:
            profile["accepted_traits"].append(item)
    for item in args.rejected:
        if item not in profile["negative_preferences"]:
            profile["negative_preferences"].append(item)
    profile["updated_at"] = now
    write_json(profile_path, profile)
    print(json.dumps({"status": "ok", "log": str(log_path), "profile": str(profile_path)}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
