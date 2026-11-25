import json, os, sys, urllib.request, urllib.parse

msg = os.environ["MESSAGE"].strip()
channels = json.load(open("channels.json", encoding="utf-8"))


def post(url, data, as_json=False):
    if as_json:
        body = json.dumps(data).encode()
        headers = {"Content-Type": "application/json"}
    else:
        body = urllib.parse.urlencode(data).encode()
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
    req = urllib.request.Request(url, body, headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def send(ch):
    p, chat = ch["platform"], ch["chat_id"]
    if p == "bale":
        t = os.environ["BALE_TOKEN"]
        return post(f"https://tapi.bale.ai/bot{t}/sendMessage",
                    {"chat_id": chat, "text": msg})
    if p == "eitaa":
        t = os.environ["EITAA_TOKEN"]
        return post(f"https://eitaayar.ir/api/{t}/sendMessage",
                    {"chat_id": chat, "text": msg})
    if p == "rubika":
        t = os.environ["RUBIKA_TOKEN"]
        return post(f"https://botapi.rubika.ir/v3/{t}/sendMessage",
                    {"chat_id": chat, "text": msg}, as_json=True)
    raise ValueError("platform نامعتبر: " + p)


failed = 0
for ch in channels:
    try:
        res = send(ch)
        print("OK  ", ch["name"], res[:200])
    except Exception as e:
        failed += 1
        print("FAIL", ch["name"], e)

sys.exit(1 if failed else 0)
