import json
users = [(json.loads(l)['userID'],l) for l in open("log.txt").readlines() if "User sent" in l and "SSTTAA" not in l]
feedback = [(json.loads(l)['userID'],l) for l in open("log.txt").readlines() if "feedback" in l.lower() and "SSTTAA" not in l]
liked = [(json.loads(l)['userID'],l) for l in open("log.txt").readlines() if "liked" in l.lower() and "SSTTAA" not in l]
correction = [(json.loads(l)['userID'],l) for l in open("log.txt").readlines() if "correct" in l.lower() and "SSTTAA" not in l]

print("total", len(set([e[0] for e in users])))
print("feedback", len(set([e[0] for e in feedback])))
print("feedback", len([e[0] for e in feedback]))
print("correction", len(set([e[0] for e in correction])))
print("correction", len([e[0] for e in correction]))
print("liked", len(set([e[0] for e in liked])))
print("liked", len([e[0] for e in liked]))

def remove_successive(arr):
  narr = [arr[0]]
  for e in arr[1:]:
    if e['userID'] != narr[-1]['userID'] or e['text'] != narr[-1]['text']:
      if "liked" in e['text'] and "liked" in narr[-1]['text']:
        narr[-1] = e
      else:
        narr.append(e)

  return [json.dumps(e) for e in narr]

def get_last_sys_utt(rows, i, uid):
  last = [e for e in rows[:i] if "User received" in e and str(uid) in e]
  if len(last) == 0:
    return "NORESPONSE"
  return json.loads(last[-1])['text']

def get_last_usr_utt(rows, i, uid):
  last = [e for e in rows[:i] if "User sent" in e and str(uid) in e]
  if len(last) == 0:
    return "NORESPONSE"
  return json.loads(last[-1])['text']

def get_next_usr_utt(rows, i, uid):
  last = [e for e in rows[i+1:] if "User sent" in e and str(uid) in e]
  if len(last) == 0:
    return "NORESPONSE"
  return json.loads(last[0])['text']

def get_length(rows, uid):
  return len([e for e in rows if str(uid) in e and "User sent" in e])


def get_stats(rows):
  users = [(json.loads(l)['userID'],l) for l in rows if "User sent" in l and "SSTTAA" not in l]
  total = len(set([e[0] for e in users]))
  print("Unique users", len(set([e[0] for e in users])))

  feedback = [(json.loads(l)['userID'],l,i) for i,l in enumerate(rows) if "feedback" in l.lower() and "SSTTAA" not in l]
  print("Unique users with feedback", len(set([e[0] for e in feedback]))/total)

  liked = [(json.loads(l)['userID'],l,i) for i,l in enumerate(rows) if ("user liked" in l.lower() or "user disl" in l.lower()) and "SSTTAA" not in l]
  print("Unique users with liked", len(set([e[0] for e in liked]))/total)

  correction = [(json.loads(l)['userID'],l,i) for i,l in enumerate(rows) if "user correct" in l.lower() and "SSTTAA" not in l]
  print("Unique users with correction", len(set([e[0] for e in correction]))/total)

  print("Unique users with feedback", len(set([e[0] for e in feedback+liked+correction]))/total)


  print("Unique users with feedback", len([e[0] for e in feedback])/total)

  print("Unique users with liked", len([e[0] for e in liked])/total)

  print("Unique users with correction", len([e[0] for e in correction])/total)

  print("Unique users with feedback", len([e[0] for e in feedback+liked+correction])/total)

  # annotate feedback
  a =correction
  past = [get_last_sys_utt(rows, e[2], e[0]) for e in a] 
  last = [get_last_usr_utt(rows, e[2], e[0]) for e in a] 
  future = [get_next_usr_utt(rows, e[2], e[0]) for e in a] 
  lengths = [get_length(rows, e[0]) for e in a] 
  lengths = {e[0]:l for l,e in zip(lengths,a)}.values()
  import pdb; pdb.set_trace()

liked_lens = [2, 19, 9, 42, 3, 3, 5, 11, 6, 12, 7, 3, 4, 13, 6, 6, 3, 4, 30, 3, 10, 5, 6, 3, 27, 5, 7]
other_lens = [29, 6, 14,6, 14, 6, 12, 3, 5, 15, 34]

comb_lens = [29, 14, 11, 2, 17, 5, 16, 5, 2, 3, 5, 35, 5, 15, 2, 2, 5]  

for i in range(4):
  print("="*40)
  print("Exp state {0}".format(i))
  #get_stats([ e for e in open("log.txt").readlines() if json.loads(e)["expState"] == i])
  print("="*40)
  get_stats(remove_successive([ json.loads(e) for e in open("log.txt").readlines() if json.loads(e)["expState"] == i]))

users = [(json.loads(l)['userID'],l) for l in open("log.txt").readlines() if "User sent" in l and "SSTTAA" not in l]
print(len(set([e[0] for e in users])))
print(len(users))
