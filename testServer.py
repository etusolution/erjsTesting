import SimpleHTTPServer
import SocketServer
import sys

PORT = 1548

class MyHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    log_file = open('logfile.txt', 'w')
    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.client_address[0],
                             self.log_date_time_string(),
                             format%args))

Handler = MyHTTPHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT

httpd.serve_forever()