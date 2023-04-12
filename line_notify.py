import requests
import configparser
import argparse
import json
on_github = True  # True -> 在 github 運作; False -> 在 local 運作; 要啟用 action 時要記得換回 True

parser = argparse.ArgumentParser()
parser.add_argument(
    "--token",
    "-t",
    type=str
)
args = parser.parse_args()

if on_github:
    line_token = args.token
else:
    config = configparser.ConfigParser()
    config.read('line_token.ini')
    line_token = config["token"]["value"]

s = line_token.split(":")
params = {
    'message':"\nhello\nworld"
}
requests.post("https://notify-api.line.me/api/notify",
    headers = {s[0]:s[1][1:]}, params=params
)
