from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

class Liveness (RequestHandler):
    def get (self):
        self.write({'message':'alive'})

class SplitFile(RequestHandler):
    def get (self):
        self.write({'message':'processed'})
        
def make_app():
  urls = [
      ("/api/v1/liveness", Liveness),
      ("/api/v1/splitfile", SplitFile)
      ]
  return Application(urls)
  
if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()