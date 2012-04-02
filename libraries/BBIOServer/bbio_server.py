"""
 BBIOServer - v0.1
 Copyright 2012 Alexander Hiam
 A dynamic web interface library for PyBBIO.
"""

import os, sys, urlparse, traceback
from multiprocessing import Process
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

from bbio import *

THIS_DIR = os.path.dirname(__file__)
PAGES_DIR = "%s/pages" % THIS_DIR
HEADER = "%s/src/header.html" % THIS_DIR
SIDEBAR = "%s/src/sidebar.html" % THIS_DIR
FOOTER = "%s/src/footer.html" % THIS_DIR
INDEX_TEMPLATE = "%s/src/index.html.template" % THIS_DIR
INDEX = "%s/index.html" % THIS_DIR

# Change working directory to the BBIOServer library directory,
# otherwise the request handler will try to deliver pages from the
# directory where the program using the library is being run from:
os.chdir(THIS_DIR)

# This is where we store the function strings indexed by their
# unique ids:
FUNCTION_STRINGS = {}


class BBIORequestHandler(SimpleHTTPRequestHandler):

  def do_GET(self):
    """ Overrides SimpleHTTPRequestHandler.do_GET() to handle
        PyBBIO function calls. """
    url = self.raw_requestline.split(' ')[1]
    if ('?' in url):
      # We've received a request for a PyBBIO function call,
      # parse out parameters:
      url = url.split('?')[1]
      params = urlparse.parse_qs(url)
      function_id = params['function_id'][0]

      # This should be a key in the FUNCTION_STRINGS dictionary: 
      if (function_id in FUNCTION_STRINGS):
        function = FUNCTION_STRINGS[function_id]

        if ("entry_text" in params):
          # This is a request from a text entry, so we also need to
          # parse out the text to be passed to the function:
          text = params['entry_text'][0]
          if (text == " "):
            # An empty text box is converted into a space character
            # by the Javascript, because otherwise the parsed url
            # would not have an entry_text param and we'd get errors
            # trying to call the function; convert it back:
            text = "" 
          # If we inserted the text into the function string and 
          # evaluated it at this point, the text received would be 
          # evaluated by Python, which we really don't want. If we
          # put it in an extra set of quotes it will evaluate to a 
          # string correctly: 
          text = "'%s'" % text
          function = function % (text)

        # Evaluate the function string and capture the return value
        # in a string (which will be an empty string if function has 
        # no return value):
        response = str(eval(function))

      else:
        # The function id is not in the dictionary. This happens if
        # the server has restarted, which generates new function ids, 
        # and the page has not been refreshed.
        response = "*Refresh page*"

      # Send the HTTP headers:
      self.send_response(200)
      self.send_header('Content-Type', 'text/html')
      # Our length is simply the length of our function return value:
      self.send_header("Content-length", len(response))
      self.send_header('Server', 'PyBBIO Server')
      self.end_headers()

      # And finally we write the response:
      self.wfile.write(response)
      return

    # If we get here there's no function id in the request, which
    # means it's a normal page request; let SimpleHTTPRequestHandler
    # handle it the standard way:
    SimpleHTTPRequestHandler.do_GET(self)
    

class BBIOHTTPServer(HTTPServer):

  def handle_error(self, request, client_address):
    """ Overrides HTTPServer.handle_error(). """
    # Sometimes when refreshing or navigating away from pages with
    # monitor divs, a Broken pipe exception is thrown on the socket
    # level. By overriding handle_error() we are able to ignore these:
    error = traceback.format_exc()
    if ("Broken pipe" in error):
      return

    # Otherwise we want to print the error like normal, except that,
    # because BBIOServer redirects stderr by default, we want it to
    # print to stdout:
    traceback.print_exc(file=sys.stdout)
    print '-'*40
    print 'Exception happened during processing of request from',
    print client_address    
    print '-'*40


class NoPrint():
  # This acts as a file object, but it doesn't print anything.
  def write(self, string):
    pass
  def flush(self):
    pass

class BBIOServer():
  def __init__(self, port=8000, verbose=False):
    if not(verbose):
      # A log of every request to the server is written to stderr.
      # This makes for a lot of printing when using the monitors. 
      # We can avoid this by redirecting stderr to a NoPrint() instance:
      sys.stderr = NoPrint()

    self._server = BBIOHTTPServer(('',port), BBIORequestHandler)

  def start(self, *pages):
    """ Takes a list of Page instances, creates html files, and starts
        the server. """

    # Make sure pages/ directory exists:
    if not(os.path.exists(PAGES_DIR)):
      os.system("mkdir %s" % PAGES_DIR)
    # Remove old pages if any:
    if (os.listdir(PAGES_DIR)):
      os.system("rm %s/*" % PAGES_DIR)
    
    # We treat the first page passed in as the home page and create
    # an index.html page in the base directory that redirects to it:
    home = pages[0]
    with open(INDEX, 'w') as index:
      with open(INDEX_TEMPLATE, 'r') as index_template:
        index.write(index_template.read() % home.filename)

    # Generate a list of links for the sidebar:
    links = ''
    for page in pages:
      links += '<li><a href="%s">%s</a></li>\n' % (page.filename, page.title)

    # Add sidebar to each page and write them to files:
    for page in pages:
      path =  "%s/%s" % (PAGES_DIR, page.filename)
      with open(path, 'w') as f:
        f.write(str(page) % links)

    # The server is started as a subprocess. This way it's easy
    # to catch a KeyboardInterrupt and stop the server happily:
    self._server_process = Process(target=self._server.serve_forever)
    self._server_process.start()

    try:
      while(True):
        # Do as little as possible here to keep the CPU and memory
        # usage to a minimum:
        delay(10000)
    except KeyboardInterrupt:
      self.stop()
    except Exception, e:
      print e
      self.stop()

  def stop(self):
    self._server_process.terminate()
    

class Page(object):
  def __init__(self, title):
    self.title = title
    # Convert the title to a valid .html filename:
    not_allowed = " \"';:,.<>/\|?!@#$%^&*()+="
    self.filename = ''
    for c in title: 
      self.filename += '' if c in not_allowed else c
    self.filename += ".html" 
   
    # The header template has three string formatting operators:
    # the document and page titles, and the sidebar. The sidebar
    # template has one formatting operator where the list of links
    # goes. When we insert the two titles and the sidebar content
    # into the header template, we end up with the one formatting
    # operator from the sidebar template. This way the BBIOServer
    # will be able to insert the links even though the pages are 
    # all created separately:
    self.html = open(HEADER, 'r').read() % \
                (title, title, open(SIDEBAR, 'r').read())

  def add_heading(self, text):
    """ Add a heading to the current position in the page. """
    self.html += '<div class="heading">%s</div>\n' % (text)

  def add_text(self, text, newline=False):
    """ Add text to the current position in the page. If newline=True
        the text will be put on a new line, otherwise it will be stacked
        on the current line. """
    style = "clear: left;" if newline else ''
    self.html += '<div class="text" style="%s">%s</div>\n' %\
                 (style, text)

  def add_button(self, function_str, label, newline=False, pointer=None):
    """ Add a button to the current position in the page with the given
        label, which will execute the given function string, e.g.:
        'digitalWrite(USR3, HIGH)'. If the function is not part of the 
        PyBBIO library, a pointer to the function must be passed in as
        pointer, e.g.: add_button('my_funct(USR3)', pointer=my_funct). 
        If newline=True the text will be put on a new line, otherwise it 
        will be stacked on the current line. """
    # Use system time to create a unique id for the given function.
    # This is used as a lookup value in the FUNCTION_STRINGS dictionary.
    function_id = str(int(time.time()*1e6) & 0xffff)
    FUNCTION_STRINGS[function_id] = function_str

    style = "clear: left;" if newline else ''

    if (pointer): 
      # We need to add the fuction to this namespace. This is easy
      # with a little bit of Python wierdness:
      # Get the string of the function name from the pointer:
      name = pointer.__name__ 
      # Declare it as a global variable in this namespace and set
      # it equal to given function pointer:  
      exec("global %s; %s = pointer" % (name, name))

    # Add the HTML. Set the button to call the javascript function 
    # which communicates with the request handler, passing it the
    # function id and a string to indicate that it is a button:
    self.html +=\
      '<div class="object-wrapper" style="%s">\n' % (style) +\
      '<div class="button" onclick="call_function(%s, \'button\')">%s\n' %\
        (function_id, label) +\
     '</div>\n</div>\n'

  def add_entry(self, function_str, submit_label, newline=False, pointer=None):
    """ Add a text entry box and a submit button with the given label to the 
        current position in the page. When submitted, the function string 
        will be executed with the entered text inserted, and it must be in
        the form: 'my_funct(%s)'. If the function is not part of the PyBBIO
        library, a pointer to the function must be passed in as pointer. 
        If newline=True the text will be put on a new line, otherwise it 
        will be stacked on the current line. """

    # Create the unique id and store the function:
    function_id = str(int(time.time()*1e6) & 0xffff)
    FUNCTION_STRINGS[function_id] = function_str
    style = "clear: left;" if newline else ''

    if (pointer): 
      # Add function to this namespace:
      name = pointer.__name__
      exec("global %s; %s = pointer" % (name,name))

    # Add the HTML. Pass the Javascript function the function id,
    # as well as a string to indicate it's an entry. This way the
    # Javascript function will know to extract the text from the 
    # entry and pass it as part of its request. 
    self.html +=\
      '<div class="object-wrapper" style="%s">\n' % (style) +\
      '<input class="entry" id="%s" type="text" name="entry" />\n' %\
      (function_id) +\
      '<div class="button" onclick="call_function(%s, \'entry\')">%s\n' % \
      (function_id, submit_label) +\
     '</div>\n</div>\n'

  def add_monitor(self, function_str, label, units='', newline=False, 
                  pointer=None):
    """ Add a monitor to the current position in the page. It will be
        displayed in the format: 'label' 'value' 'units', where value is 
        the most recent return value of the given function; will be 
        updated every 200 ms or so. If the function is not part of the 
        PyBBIO library, a pointer to the function must be passed in as
        pointer. If newline=True the text will be put on a new line,
        otherwise it will be stacked on the current line. """
    
    # Create the unique id and store the function:
    function_id = str(int(time.time()*1e6) & 0xffff)
    FUNCTION_STRINGS[function_id] = function_str

    style = "clear: left;" if newline else ''

    if (pointer): 
      # Add function to this namespace:
      name = pointer.__name__
      exec("global %s; %s = pointer" % (name,name))

    # Add the HTML. Set the monitor id as the function id. When
    # the page loads a Javascript function is called which continually
    # loops throught each monitor, extracts the id, passes it to the
    # server, then sets the text in the monitor div to the return
    # value.
    self.html +=\
      '<div class="object-wrapper" style="%s">\n' % (style) +\
      '<div class="value-field">%s</div>\n' % (label) +\
      '<div class="monitor-field" id="%s"></div>\n' % (function_id) +\
      '<div class="value-field">%s</div>\n' % (units) +\
      '</div>\n'

  def __str__(self):
    # Return the HTML with the content of the footer template
    # appended to it: 
    return self.html + open(FOOTER, 'r').read()
