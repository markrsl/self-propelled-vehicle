#!/usr/bin/pythonRoot
# bring in the libraries
from flup.server.fcgi import WSGIServer
import sys, urlparse
import main

# all of our code now lives within the app() function which is called for each http request we receive
def app(environ, start_response):
    # start our http response
    start_response("200 OK", [("Content-Type", "text/html")])
    # look for inputs on the URL
    i = urlparse.parse_qs(environ["QUERY_STRING"])

    yield ('&nbsp;')  # flup expects a string to be returned from this function

    # if there's a url variable named 'q'
    if "q" in i:
        if i["q"][0] == "run":
            main.run(True)
        elif i["q"][0] == "stop":
            main.run(False)
# by default, Flup works out how to bind to the web server for us, so just call it with our app() function and let it get on with it
WSGIServer(app).run()