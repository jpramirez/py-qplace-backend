from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string,sys

import json

from models import SplitSilence
from models import Recognition
from models import Convertion

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



class UploadHandlerConvert(RequestHandler):
    def post(self,param1):
        fileID = param1
        file1 = self.request.files['files'][0]
        original_fname = file1['filename']
        print (original_fname)
        extension = os.path.splitext(original_fname)[1]
        #fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        #final_filename= fname+extension
        output_file = open("audio/" + original_fname, 'wb')
        output_file.write(file1['body'])
        output_file.close()

        if param1 == "splitfile":
            sp = SplitSilence.SplitSilence("audio/" + original_fname,param1)
            ret = sp.Split()
        elif param1 == "recognize":
            rc = Recognition.Recognizer(output_file)
            ret = rc.Recognize()
        elif param1 == "convert":
            ret = Recognition.Recognizer(output_file)
        
        self.write({'message':'processed','files':'uploaded','data':ret})
        #self.finish("file" + final_filename + " is uploaded")





class UploadHandlerRecognize(RequestHandler):
    
    def post(self,param1):
        fileID = param1
        file1 = self.request.files['files'][0]
        original_fname = file1['filename']
        print (original_fname)
        extension = os.path.splitext(original_fname)[1]
        #fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        #final_filename= fname+extension
        output_file = open("audio/" + original_fname, 'wb')
        output_file.write(file1['body'])
        output_file.close()

        rc = Recognition.Recognizer("audio/" + original_fname)
        ret = rc.Recognize()
  
        self.write({'message':'processed','files':'uploaded','data':ret})
        #self.finish("file" + final_filename + " is uploaded")

class UploadHandlerSplit(RequestHandler):
    def post(self,param1):
        fileID = param1
        file1 = self.request.files['files'][0]
        original_fname = file1['filename']
        print (original_fname)
        extension = os.path.splitext(original_fname)[1]
        #fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        #final_filename= fname+extension
        output_file = open("audio/" + original_fname, 'wb')
        output_file.write(file1['body'])
        output_file.close()

        sp = SplitSilence.SplitSilence("audio/" + original_fname,param1)
        retpath = sp.Split()

        with open(retpath, 'rb') as f:
                data = f.read()
            
        self.set_header("Content-type",  "application/zip")
        self.write(data)
        self.finish()        
        ##self.write({'message':'processed','files':'uploaded','data':ret})
        #self.finish("file" + final_filename + " is uploaded")

class Liveness (RequestHandler):
    def get (self):
        self.write({'message':'alive'})
        
        
class ListingDirectory (RequestHandler):
    def get (self,param1):
        path = "./audio/"+param1
        self.set_header("Content-type",  "application/json")        
        self.write(json.dumps(path_to_dict(path)))



class GetFile(RequestHandler):
    def get(self, param1, param2):
        path = "./audio/"+param1+"/"+param2    
        print (path)
        try:
            with open(path, 'rb') as f:
                data = f.read()
            
            self.set_header("Content-type",  "audio/wav")
            self.write(data)
            self.finish()
        except IOError:
            raise tornado.web.HTTPError(404, 'Invalid archive')
    
def make_app():
  urls = [
      ("/api/v1/liveness", Liveness),
      (r"/api/v1/process/split/?(?P<param1>[^\/]+)?", UploadHandlerSplit),
      (r"/api/v1/process/recognize/?(?P<param1>[^\/]+)?", UploadHandlerRecognize),
      (r"/api/v1/process/convert/?(?P<param1>[^\/]+)?", UploadHandlerConvert),
      (r"/api/v1/list/?(?P<param1>[^\/]+)?",ListingDirectory),
      (r"/api/v1/file/?(?P<param1>[^\/]+)/?(?P<param2>[^\/]+)?",GetFile)
      ]
  return Application(urls)
  
  
  
def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d
    
    
if __name__ == '__main__':
    app = make_app()

    app.listen(3000)
    IOLoop.instance().start()