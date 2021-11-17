import pandas as pd
import os

os.chdir("/opt/workspace/sentiment")

# Run through sentiment directory and combine all csv's
files = [file for file in os.listdir() if file.endswith(".csv")]
def read_csv(file):
    df = pd.read_csv(file, header = None)
    return pd.DataFrame(df.values, columns = ["tweets", "processed", "sentiment"])
dfs = []
for file in files:
    try: dfs.append(read_csv(file))
    except: 
        print(file)
        continue
final = pd.concat(dfs)

final.to_csv("../twitterStreamSentiment.csv", index=False)