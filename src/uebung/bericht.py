"""
python uebung/bericht.py classic
python uebung/bericht.py medium
python uebung/bericht.py pro

"""

import json
import sys
from datetime import datetime

ORDNER = "uebung/daten"

def report(m):
    p = ORDNER + "/" + m + ".json"
    f = open(p, encoding="utf-8")
    e = json.load(f)
    f.close()

    top = []
    for x in e:
        if len(top) < 3:
            top.append(x)

    s = 0
    for x in e:
        s = s + x["score"]
    avg = s / len(e)

    txt = "Bericht " + m + " vom " + datetime.now().strftime("%d.%m.%Y") + "\n"
    for i in range(len(top)):
        txt = txt + str(i + 1) + ". " + top[i]["name"] + " " + str(top[i]["score"]) + "\n"
    txt = txt + "Durchschnitt: " + str(round(avg, 1)) + "\n"
    
    print(txt)
    return txt

if __name__ == "__main__":
    report(sys.argv[1])
