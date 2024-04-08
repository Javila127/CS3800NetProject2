import sys
import string
import os
from socket import *

# Check the command line arguments
if len(sys.argv) != 3:
    print("Usage : webserver docroot port")
    sys.exit(0)

# Set the document root and port
docroot = sys.argv[1]
port = int(sys.argv[2])

# Open up a socket
serversock = socket(AF_INET, SOCK_STREAM)
serversock.bind(("", port))
serversock.listen(5)

print("Web-server listening on port %s " % (port,))

def handle_get_request(conn, document):
    # Form the full filename
    file = os.path.join(docroot, document)

    # Try opening the file
    try:
        f = open(file, 'rb')
        conn.send(b"HTTP/1.0 200 OK\n")
        # Figure out the content type
        if file.endswith(".html"):
            conn.send(b"Content-type: text/html\n")
        elif file.endswith(".gif"):
            conn.send(b"Content-type: image/gif\n")
        elif file.endswith(".jpg"):
            conn.send(b"Content-type: image/jpeg\n")
        else:
            conn.send(b"Content-type: text/plain\n")
        # Read the file and send it
        data = f.read()
        conn.send(b"Content-length: %d\n\n" % (len(data),))
        conn.send(data)
    except IOError:
        conn.send(b"HTTP/1.0 404 Not Found\n")
        conn.send(b"Content-type: text/html\n\n")
        conn.send(b"<h1> File Not Found</h1>")

def run_cgi_program(conn, document):
    # Set up two pipes that will be used to connect the server and the CGI program
    (pinput, coutput) = os.pipe()  # Create a pipe from child to parent
    (cinput, poutput) = os.pipe()  # Create a pipe from parent to child

    # Run the CGI program
    pid = os.fork()
    if pid != 0:
        # Parent process
        os.close(coutput)
        os.close(cinput)
        os.write(poutput, b"POST data if applicable")
        os.close(poutput)
        response = os.read(pinput, 1000)
        conn.send(response)
        os.waitpid(pid, 0)  # Wait for child to exit
    else:
        # Child process
        os.close(poutput)
        os.close(pinput)
        os.dup2(cinput, 0)
        os.dup2(coutput, 1)
        # Set environment variables
        os.environ['FOO'] = 'BAR'
        # Execute the CGI program
        os.execve("/usr/bin/python", ["python", document], os.environ)

while True:
    (conn, addr) = serversock.accept()  # Get a connection
    print("Connection from %s" % (addr,))
    request = ""
    c = conn.recv(1)
    while c != b"\n":
        request = request + c.decode('utf-8')
        c = conn.recv(1)
    request = request.split(" ")
    method = request[0]
    document = request[1]

    if method == "GET":
        # Handle GET request
        handle_get_request(conn, document)
    else:
        # Run CGI program
        run_cgi_program(conn, document)

    conn.close()
