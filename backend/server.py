import random
import json
import os
import requests
import tornado.ioloop
import tornado.web


class TestHandler(tornado.web.RequestHandler):
  def set_default_headers(self):
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

  def options(self):
    pass

  def get(self):
    self.write("ok")


state = None
class LeaderboardHandler(tornado.web.RequestHandler):
  def set_default_headers(self):
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

  def options(self):
    pass

  def random(self):
    names = ["Transformer Large", "Transformer Small", "DialoGPT Large", "DialoGPT Small"]
    columns = [
      [ "METEOR", "BERTScore", "USR", "human"],
      [ "METEOR", "BERTScore", "USR", "human"],
    ]
    ratings = ["sub1", "sub2"]
    state = {} 
    for r,c in zip(ratings, columns):
      rows = []
      for n in names:
        item = {"name": n} 
        for cn in c:
          item[cn] = int(random.random() * 10000)/100
        rows.append(item) 

      state[r]= {'data': rows}

    return state

  def get(self):
    state = requests.get("http://shikib.sp.cs.cmu.edu:8001/all_scores").json()
    self.write(json.dumps(state))
    

class MainHandler(tornado.web.RequestHandler):
  def set_default_headers(self):
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

  def options(self):
    pass

  def post(self):
    print(str(self.request.body.decode()))
    open("log.txt", "a+").write(str(self.request.body.decode())+"\n")
    self.write("ok")

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        extension = ".txt"
        fname = self.get_argument('filename').strip()
        extra = self.get_argument('extra').strip() == 'yes'
        test = self.get_argument('test').strip() == 'test'
 
        contents = file1['body'].decode().strip()

        try:
          if len(fname) == 0:
            self.finish("Your team/model name cannot be empty")
          elif "~" in fname or "_" in fname or "/" in fname or "." in fname:
            self.finish("Your team/model name cannot have an underscore, dot or a backslash")
          elif not test and len(contents.split("\n")) != 11274:
            self.finish("Your submission must have exactly 11,724 rows (the size of the frequent validation set)")
          elif test and len(contents.split("\n")) != 11207:
            self.finish("Your submission must have exactly 11,207 rows (the size of the frequent test set)")
          else:
            fns = [e.split(".")[0] for e in os.listdir("uploads/") if e.startswith(fname + "_v")]
            versions = [int(e.split("_v")[1]) for e in fns]

            cur_version = 0 if not versions else max(versions) + 1


            final_filename= ("test_" if test else "") + fname + "_v" + str(cur_version) + extension
            output_file = open("uploads/" + final_filename, 'w+')
            output_file.write(contents)

            if not test:
              url = "http://shikib.sp.cs.cmu.edu:8000/scores?filename={}&type={}".format(final_filename, "ex" if extra else "ap")
              self.finish("Your file: " + final_filename + " was successfully uploaded. You will be able to see the results at {} when they are ready. Please contact us on Slack if the results aren't ready in the ne xt 3 hours".format(url))
              requests.get(url)
            else:
              self.finish("Your file: " + final_filename + " was successfully uploaded. The results will not show up until AFTER the October 5th submission deadline. You can message us on Slack if you have any doubts about submission.")
        except:
          self.finish("Upload error. Please let the organizers know in the slack.")

def make_app():
  return tornado.web.Application([
      (r"/data", MainHandler),
      (r"/test", TestHandler),
      (r"/upload", UploadHandler),
      (r"/leaderboard", LeaderboardHandler),
  ])
                                                                                
if __name__ == "__main__":
  app = make_app()
  app.listen(8000)
  tornado.ioloop.IOLoop.current().start()

