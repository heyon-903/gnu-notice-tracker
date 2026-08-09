import json
import os
from datetime import datetime, timezone

import notify
import scrape_nerum
import scrape_sansi

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "data")

SOURCES = {
    "nerum": scrape_nerum,
    "sansi": scrape_sansi,
}


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _data_path(source):
    return os.path.join(DATA_DIR, f"{source}.json")


def _load_previous(source):
    path = _data_path(source)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(source, items):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_data_path(source), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def process_source(source, module):
    previous = _load_previous(source)
    is_first_run = previous is None
    previous_by_id = {item["id"]: item for item in (previous or [])}

    current_items = module.scrape()
    now = _now_iso()

    new_items = []
    merged_items = []
    for item in current_items:
        prev = previous_by_id.get(item["id"])
        if prev:
            item["first_seen_at"] = prev.get("first_seen_at", now)
        else:
            item["first_seen_at"] = now
            if not is_first_run:
                new_items.append(item)
        item["fetched_at"] = now
        merged_items.append(item)

    _save(source, merged_items)
    print(
        f"[{source}] first_run={is_first_run} total={len(merged_items)} "
        f"new={len(new_items)}"
    )
    return new_items


def main():
    new_items_by_source = {}
    for source, module in SOURCES.items():
        new_items_by_source[source] = process_source(source, module)

    notify.send_email(new_items_by_source)


if __name__ == "__main__":
    main()
