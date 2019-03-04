import requests
import re
from collections import defaultdict

request_voting = requests.get("https://gromrada.mva.gov.ua/voting/public/public_report.txt")
request_candidate = requests.get("https://gromrada.mva.gov.ua/candidates/candidates.json?fbclid=IwAR15LYLz7A249-qhO4C3F6fhUuq351fn1qT5p6K3rcpMmGRHuF7cJVwA-aE")
candidates_json = request_candidate.json()
candidates = {str(c["id"]): c["name"] for c in candidates_json['candidates']}


votes = defaultdict(list)
for vote in request_voting.content.decode().split("\r\n"):
    if vote != "":
        str_candidates = re.search(r"SEL=([\d,]+)", vote).group(1)
        for c in str_candidates.split(","):
            votes[c].append(1)

votes = {candidate: len(votes) for candidate, votes in votes.items()}
votes = sorted(votes.items(), key=lambda kv: kv[1], reverse=True)
for i, (c, v) in enumerate(votes):
    print(
        "{iter:<5} {name:38} >>   {vote} ".format(iter=str(i+1)+".", name=candidates[str(c)], vote=v)
    )