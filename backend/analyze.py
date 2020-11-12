import random
import json

from collections import *

def tryjson(s):
  try:
    return json.loads(s)
  except:
    return {}

lines = [tryjson(s) for s in open("log.txt").readlines()]
relevant = [e for e in lines if e.get('webTimeStamp', '').startswith('2020-07-15')]
relevant += [e for e in lines if e.get('webTimeStamp', '').startswith('2020-07-16')]
#relevant = [e for e in lines if e.get('webTimeStamp', '').startswith('2020-07-23')]
#relevant += [e for e in lines if e.get('webTimeStamp', '').startswith('2020-07-24')]

print("Unique conversations", len([e for e in Counter([e['userID'] for e in relevant]).values() if e > 3]))
print("Unique utterances", len([e['userID'] for e in relevant if 'User sent' in e.get("text", "")]))
print("Unique feedback", len([e['userID'] for e in relevant if 'User feedback' in e.get("text", "")]))
print("Unique correction", len([e['userID'] for e in relevant if 'User correction' in e.get("text", "")]))
print("Unique liked", len([e['userID'] for e in relevant if 'User liked' in e.get("text", "")]))
print("Unique disliked", len([e['userID'] for e in relevant if 'User Disliked' in e.get("text", "")]))

#print("Example feedback: ", [random.choice([e.get("text", "") for e in relevant if 'User feedback' in e.get("text", "")]) for _ in range(3)])
print("Example feedback: ", [e.get("text", "") for e in relevant if 'User feedback' in e.get("text", "")])
print("Example correction: ", [random.choice([e.get("text", "") for e in relevant if 'User correction' in e.get("text", "")]) for _ in range(3)])
