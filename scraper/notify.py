import os
import smtplib
import ssl
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

SOURCE_LABELS = {
    "nerum": "비교과 프로그램",
    "sansi": "산시알리미",
}


def _format_section(label, items):
    lines = [f"■ {label} ({len(items)}건)", ""]
    for item in items:
        lines.append(f"- {item['title']}")
        lines.append(f"  {item['url']}")
    lines.append("")
    return "\n".join(lines)


def build_body(new_items_by_source):
    sections = [
        _format_section(SOURCE_LABELS.get(source, source), items)
        for source, items in new_items_by_source.items()
        if items
    ]
    return "\n".join(sections).strip()


def send_email(new_items_by_source):
    total = sum(len(v) for v in new_items_by_source.values())
    if total == 0:
        return

    gmail_user = os.environ.get("GMAIL_USER")
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD")
    to_addr = os.environ.get("NOTIFY_TO", gmail_user)

    if not gmail_user or not gmail_password:
        print("GMAIL_USER / GMAIL_APP_PASSWORD not set, skipping email.")
        return

    body = build_body(new_items_by_source)
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"[GNU 공지] 새 공지 {total}건"
    msg["From"] = gmail_user
    msg["To"] = to_addr

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, [to_addr], msg.as_string())
    print(f"Sent notification email for {total} new item(s) to {to_addr}.")
