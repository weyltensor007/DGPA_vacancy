import pandas as pd
import os


target_url = "https://web3.dgpa.gov.tw/WANT03FRONT/AP/WANTF00003.aspx?GETJOB=Y"

on_github = True  # True -> 在 github 運作; False -> 在 local 運作; 要啟用 action 時要記得換回 True

need_columns = ["ORG_NAME",  # 徵才機關
                "RANK",  # 官職等
                "TITLE",  # 職稱
                "SYSNAM",  # 職系
                "WORK_PLACE_TYPE",  # 工作地點
                "VIEW_URL",  # 資訊網址
                ]


if on_github:
    # default parser = lxml, 但不相容 poetry 環境, 故另用 etree
    df = pd.read_xml(target_url, parser='etree')
    df = df.loc[:, need_columns]

else:
    data_csv = 'data.csv'
    if os.path.exists(data_csv):
        df = pd.read_csv(data_csv)
        df = df.loc[:, need_columns]
    else:
        df = pd.read_xml(target_url, parser='etree')
        df = df.loc[:, need_columns]
        df.to_csv('data.csv', index=False)

# make pandas query string
pd_query_conditions = [
    "SYSNAM == '經建行政'",
    "RANK.str.contains('薦任')",
    # "WORK_PLACE_TYPE.str.contains('臺中市|南投縣|臺北市')",
]
query_str = " and ".join(pd_query_conditions)


df_filter = df.query(query_str)

# 使用 view_url 裡面的 workid 進行排序, 排序完後 drop
df_filter["work_id"] = df_filter["VIEW_URL"].apply(
    lambda x: int(x.split("=")[-1]))
df_filter = df_filter.sort_values(by="work_id", ascending=False)
df_filter = df_filter.drop("work_id", axis=1)

# insert hyperlink
df_filter["VIEW_URL"] = df_filter["VIEW_URL"].apply(
    lambda x: f"<a href={x}>事求人詳細資訊</a>"
)
print(df_filter.shape)
# output html
df_filter.to_html("result.html", index=False, render_links=True, escape=False)
