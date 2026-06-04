import re
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
LOG_FILE = "课设1数据.log"
CSV_OUT = "parsed_课设1数据.csv"
SUMMARY_OUT = "summary_课设1数据.txt"

def short_url(u, max_len=35):
    if not isinstance(u, str):
        return ""
    return u if len(u) <= max_len else u[:max_len] + "..."
pattern = re.compile(
    r'(?P<IP>\S+)\s+'
    r'(?P<logname>\S+)\s+'
    r'(?P<user>\S+)\s+'
    r'\[(?P<day>\d{2}/\w{3}/\d{4}):'
    r'(?P<time>\d{2}:\d{2}:\d{2})\s+'
    r'(?P<zone>[+\-]\d{4})\]\s+'
    r'"(?P<method>\S+)\s+'
    r'(?P<url>\S+)\s+'
    r'(?P<protocol>[^"]+)"\s+'
    r'(?P<status>\d{3})\s+'
    r'(?P<bytes>\S+)\s+'
    r'"(?P<referer>[^"]*)"\s+'
    r'"(?P<user_agent>[^"]*)"\s+'
    r'"(?P<unknown1>[^"]*)"\s+'
    r'"(?P<responseTime>[^"]*)"'
)

def parse_line(line):
    m = pattern.search(line)
    if not m:
        return None

    gd = m.groupdict()
    try:
        dt = datetime.strptime(
            f"{gd['day']} {gd['time']} {gd['zone']}",
            "%d/%b/%Y %H:%M:%S %z"
        )
    except:
        dt = None

    return {
        "IP": gd["IP"],
        "logname": gd["logname"],
        "user": gd["user"],
        "day": gd["day"],
        "time": gd["time"],
        "zone": gd["zone"],
        "datetime": dt,
        "method": gd["method"],
        "url": gd["url"],
        "protocol": gd["protocol"],
        "status": int(gd["status"]),
        "bytes": int(gd["bytes"]) if gd["bytes"].isdigit() else 0,
        "referer": gd["referer"],
        "user_agent": gd["user_agent"],
        "unknown1": gd["unknown1"],
        "responseTime": float(gd["responseTime"])
            if gd["responseTime"].replace('.', '', 1).isdigit() else None
    }
rows = []
with open(LOG_FILE, encoding="utf-8", errors="ignore") as f:
    for line in f:
        p = parse_line(line)
        if p:
            rows.append(p)

df = pd.DataFrame(rows)
df_csv = df[
    [
        "IP", "logname", "user",
        "day", "time", "zone",
        "method", "url", "protocol",
        "status", "bytes",
        "referer", "user_agent",
        "unknown1", "responseTime"
    ]
]
df_csv.to_csv(CSV_OUT, index=False, encoding="utf-8-sig")
top_ip = df["IP"].value_counts().head(10)
top_ip.plot(kind="bar", figsize=(8, 5))
plt.title("Top 10 活跃 IP")
plt.ylabel("请求次数")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("fig_top_ip.png")
plt.clf()
top_url = df["url"].value_counts().head(20)
top_url_disp = top_url.copy()
top_url_disp.index = [short_url(u) for u in top_url.index]
top_url_disp.plot(kind="barh", figsize=(8, 6))
plt.title("Top 20 热门页面")
plt.xlabel("访问次数")
plt.tight_layout()
plt.savefig("fig_top_url.png")
plt.clf()
status_count = df["status"].value_counts().sort_index()
status_count.plot(kind="bar")
plt.title("HTTP 状态码分布")
plt.xlabel("状态码")
plt.ylabel("次数")
plt.tight_layout()
plt.savefig("fig_status_code.png")
plt.clf()

error_404 = df[df["status"] == 404]["url"].value_counts().head(10)
df["hour"] = df["datetime"].dt.hour
hour_dist = df["hour"].value_counts().sort_index()
hour_dist.plot()
plt.title("按小时访问量分布")
plt.xlabel("小时")
plt.ylabel("访问次数")
plt.tight_layout()
plt.savefig("fig_hour_dist.png")
plt.clf()
df = df.sort_values("datetime")
session_gap = timedelta(minutes=30)
session_lengths = []

for (ip, ua), g in df.groupby(["IP", "user_agent"]):
    last = None
    length = 0
    for t in g["datetime"]:
        if last is None or t - last > session_gap:
            if length > 0:
                session_lengths.append(length)
            length = 1
        else:
            length += 1
        last = t
    session_lengths.append(length)

avg_session_len = sum(session_lengths) / len(session_lengths)
bounce_rate = sum(1 for x in session_lengths if x == 1) / len(session_lengths)
ua = df["user_agent"].str.lower()
bot_mask = ua.str.contains(
    "bot|spider|crawl|baidu|google|bing|yandex|soso",
    regex=True
)
bot_count = bot_mask.sum()
human_count = len(df) - bot_count

plt.bar(["爬虫", "真人"], [bot_count, human_count])
plt.title("爬虫与真人访问对比")
plt.tight_layout()
plt.savefig("fig_bot_vs_human.png")
plt.clf()
referer_top = df["referer"].value_counts().head(10)
resp = df["responseTime"].dropna()
resp = resp[resp <= 5]
plt.figure(figsize=(7, 4))
plt.hist(resp, bins=40)
plt.xlim(0, 2)
plt.title("响应时间分布（0–2 秒）")
plt.xlabel("响应时间（秒）")
plt.ylabel("请求数")
plt.tight_layout()
plt.savefig("fig_response_time.png")
plt.clf()
avg_resp = resp.mean()
slow_req = df[df["responseTime"] > 1.0]
with open(SUMMARY_OUT, "w", encoding="utf-8") as f:
    f.write(f"日志文件：{LOG_FILE}\n")
    f.write(f"总请求数：{len(df)}\n")
    f.write(f"不同 IP 数：{df['IP'].nunique()}\n\n")

    f.write("【Top 10 活跃 IP】\n")
    f.write(top_ip.to_string())
    f.write("\n\n")

    f.write("【Top 20 热门页面（完整 URL）】\n")
    f.write(top_url.to_string())
    f.write("\n\n")

    f.write("【404 错误最多的 URL】\n")
    f.write(error_404.to_string())
    f.write("\n\n")

    f.write("【会话分析】\n")
    f.write(f"平均会话长度：{avg_session_len:.2f} 次请求\n")
    f.write(f"跳出率：{bounce_rate:.2%}\n\n")

    f.write("【爬虫识别】\n")
    f.write(f"疑似爬虫请求数：{bot_count}\n")
    f.write(f"真人请求数：{human_count}\n\n")

    f.write("【入口来源 Top10】\n")
    f.write(referer_top.to_string())
    f.write("\n\n")

    f.write("【性能指标】\n")
    f.write(f"平均响应时间：{avg_resp:.3f} 秒\n")
    f.write(f"慢请求（>1 秒）数量：{len(slow_req)}\n")

print("分析完成")