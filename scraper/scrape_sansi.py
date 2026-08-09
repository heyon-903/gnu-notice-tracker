import re

from bs4 import BeautifulSoup

from common import fetch

LIST_URL = "https://www.gnu.ac.kr/ise/na/ntt/selectNttList.do"
DETAIL_URL = "https://www.gnu.ac.kr/ise/na/ntt/selectNttInfo.do"

MI = "3001"
BBS_ID = "1373"

SOURCE = "sansi"


def _clean(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def _parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for row in soup.select("table tbody tr"):
        link = row.select_one("a.nttInfoBtn")
        if not link or not link.get("data-id"):
            continue
        item_id = link["data-id"].strip()
        tds = row.find_all("td")
        author = _clean(tds[2].get_text()) if len(tds) > 2 else ""
        date = _clean(tds[3].get_text()) if len(tds) > 3 else ""
        views = _clean(tds[4].get_text()) if len(tds) > 4 else ""

        items.append(
            {
                "id": item_id,
                "source": SOURCE,
                "title": _clean(link.get_text()),
                "author": author,
                "date": date,
                "views": views,
                "url": f"{DETAIL_URL}?mi={MI}&bbsId={BBS_ID}&nttSn={item_id}",
            }
        )
    return items


def scrape(pages=2):
    all_items = []
    seen_ids = set()
    for page in range(1, pages + 1):
        html = fetch(
            LIST_URL,
            params={"mi": MI, "bbsId": BBS_ID, "currPage": page},
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
