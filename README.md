# GNU 공지 트래커

경상국립대 학생역량관리시스템의 "비교과 프로그램" 목록과 산업시스템공학부 "산시알리미" 참여프로그램
게시판의 새 글을 한 페이지에서 모아 보는 도구입니다.

## 동작 방식

- `.github/workflows/update.yml`이 매일 11:00(KST)에 `scraper/main.py`를 실행합니다.
- 스크립트는 두 사이트를 로그인 없이 스크래핑해 `docs/data/nerum.json`, `docs/data/sansi.json`을 갱신합니다.
- `docs/index.html`은 위 JSON 파일을 읽어 보여주는 정적 페이지로, GitHub Pages로 호스팅합니다.
  새로 올라온 글은 `first_seen_at` 기준 최근 3일 이내면 "NEW" 뱃지가 붙습니다.

## 로컬 실행

```bash
pip install -r scraper/requirements.txt
python scraper/main.py
```

## GitHub Pages 배포

Settings → Pages → Source를 `main` 브랜치의 `/docs` 폴더로 설정하면
`https://<계정>.github.io/gnu-notice-tracker/`에서 확인할 수 있습니다.
