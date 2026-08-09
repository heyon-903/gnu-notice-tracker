import json
import re

from bs4 import BeautifulSoup

from common import fetch

LIST_URL = "https://nerum.gnu.ac.kr/ptfol/imng/icmpNsbjtPgm/findIcmpNsbjtPgmList.do"
DETAIL_URL = "https://nerum.gnu.ac.kr/ptfol/imng/icmpNsbjtPgm/findIcmpNsbjtPgmInfo.do"

SOURCE = "nerum"


def _clean(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def _parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for li in soup.select("div.lica_wrap > ul > li"):
        detail_btn = li.select_one(".detailBtn")
        if not detail_btn or not detail_btn.get("data-params"):
            continue
        try:
            params = json.loads(detail_btn["data-params"])
        except (ValueError, TypeError):
            continue
        item_id = params.get("encSddpbSeq")
        if not item_id:
            continue

        title_el = li.select_one(".tit.ellipsis")
        desc_el = li.select_one(".desc.ellipsis")
        major_type = [
            _clean(el.get_text()) for el in li.select(".major_type li")
        ]
        apply_dd = li.select_one(".apl_date dd")
        edu_dd = li.select_one(".edu_date dd")
        tags = [_clean(t.get_text()) for t in li.select(".label_box .label")]

        items.append(
            {
                "id": item_id,
                "source": SOURCE,
                "title": _clean(title_el.get_text()) if title_el else "",
                "org": major_type[0] if len(major_type) > 0 else "",
                "type": major_type[1] if len(major_type) > 1 else "",
                "desc": _clean(desc_el.get_text()) if desc_el else "",
                "apply_period": _clean(apply_dd.get_text()) if apply_dd else "",
                "edu_period": _clean(edu_dd.get_text()) if edu_dd else "",
                "tags": tags,
                "url": f"{DETAIL_URL}?encSddpbSeq={item_id}&paginationInfo.currentPageNo=1",
            }
        )
    return items


def scrape(pages=2):
    all_items = []
    seen_ids = set()
    for page in range(1, pages + 1):
        html = fetch(
            LIST_URL,
            params={
                "sort": "0001",
                "paginationInfo.currentPageNo": page,
            },
        )
        page_items = _parse_page(html)
        if not page_items:
            break
        for item in page_items:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                all_items.append(item)
    return all_items


if __name__ == "__main__":
    for entry in scrape():
        print(entry)
