import requests
import socket
import os
import json
import time
from datetime import datetime
import re

bearer_token = "INSERT_TOKEN_HERE"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # Rule list reference
    # https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule#list
    requiredRules = "-is:retweet -giveaway -#giveaway lang:en"

    rules = [
        {"value": f"(crypto OR cryptocurrency OR \"crypto currency\") {requiredRules}", "tag": "cryptocurrency indicator"},
        {"value": f"from:DocumentingBTC {requiredRules}"},
        {"value": f"from:APompliano {requiredRules}"},
        {"value": f"from:NickSzabo4 {requiredRules}"},
        {"value": f"from:100trillionUSD {requiredRules}"},
        {"value": f"from:aantonop {requiredRules}"}
    ]
    payload = {"add": rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set, conn):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            write(json_response)
            now = datetime.now()   
            current_time = now.strftime("%H:%M:%S")
            print(f"Got Tweet at {current_time}, Sending")
            payload = json_response["data"]["text"]
            payload = re.sub(r"\n", " ", payload) + "\n"
            print(repr(payload))
            conn.sendall(payload.encode("utf-8"))
            time.sleep(5)

def write(json_response):
    f = open("tweets.txt", "a")
    f.write(json.dumps(json_response, indent=4, sort_keys=True))
    f.write("\n")
    f.close()

def main():
    f = open("tweets.txt", "w")
    f.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 9999))
    s.listen(1)
    print("Waiting for connection...")
    conn, addr = s.accept()
    print("Got connection")
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set, conn)


if __name__ == "__main__":
    main()
