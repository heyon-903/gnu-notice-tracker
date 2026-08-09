# GNU 공지 트래커

경상국립대 학생역량관리시스템의 "비교과 프로그램" 목록과 산업시스템공학부 "산시알리미" 참여프로그램
게시판의 새 글을 한 페이지에서 모아 보고, 새 글이 있으면 이메일로 알려주는 도구입니다.

## 동작 방식

- `.github/workflows/update.yml`이 매일 11:00(KST)에 `scraper/main.py`를 실행합니다.
- 스크립트는 두 사이트를 로그인 없이 스크래핑해 `docs/data/nerum.json`, `docs/data/sansi.json`을
  갱신하고, 이전 실행 대비 새로 생긴 글이 있으면 이메일을 보냅니다.
- `docs/index.html`은 위 JSON 파일을 읽어 보여주는 정적 페이지로, GitHub Pages로 호스팅합니다.

## 로컬 실행

```bash
pip install -r scraper/requirements.txt
python scraper/main.py
```

첫 실행은 기준 데이터만 저장하고 이메일은 보내지 않습니다. 이후 실행부터 새 글이 있으면
`GMAIL_USER`, `GMAIL_APP_PASSWORD` 환경변수가 설정된 경우에 한해 이메일을 보냅니다.

## 이메일 알림 설정 (GitHub Actions Secret)

1. Gmail 계정(알림을 보낼 계정)에서 2단계 인증을 켜고 [앱 비밀번호](https://myaccount.google.com/apppasswords)를 발급받습니다.
2. 저장소 Settings → Secrets and variables → Actions에서 아래 두 개를 등록합니다.
   - `GMAIL_USER`: 발신에 사용할 Gmail 주소
   - `GMAIL_APP_PASSWORD`: 위에서 발급받은 16자리 앱 비밀번호
   - (선택) `NOTIFY_TO`: 받는 사람 주소를 다르게 하려면 설정. 비워두면 `GMAIL_USER`로 발송됩니다.
3. `gh` CLI를 쓴다면:
   ```bash
   gh secret set GMAIL_USER --body "tkghkhun@gmail.com"
   gh secret set GMAIL_APP_PASSWORD
   ```

## GitHub Pages 배포

Settings → Pages → Source를 `main` 브랜치의 `/docs` 폴더로 설정하면
`https://<계정>.github.io/gnu-notice-tracker/`에서 확인할 수 있습니다.
