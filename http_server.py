import os
import subprocess
from http.server import HTTPServer, CGIHTTPRequestHandler

# Get the user's home directory
home = os.path.expanduser("~")

# Define the directory containing your files
DIRECTORY = os.path.join(home, 'Documents', 'Public')

# Set the CGI script directory
CGI_DIRECTORY = os.path.join(home, 'Documents', 'Public')

# Set the path to the PHP interpreter
PHP_INTERPRETER = '/usr/bin/php'

# Define the HTTP request handler class
class CustomCGIHandler(CGIHTTPRequestHandler):
    def run_php(self, path):
        # Run the PHP script and return the output
        output = subprocess.check_output([PHP_INTERPRETER, path])
        return output

    def do_POST(self):
        self.send_error(501, "Unsupported method (POST)")

    def do_GET(self):
        # Check if the requested file is a PHP file
        if self.path.endswith('.php'):
            php_script = os.path.join(CGI_DIRECTORY, self.path[1:])
            if os.path.isfile(php_script):
                # Execute the PHP script and send the output
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = self.run_php(php_script)
                self.wfile.write(output)
                return
        # Otherwise, serve the file as usual
        return CGIHTTPRequestHandler.do_GET(self)

# Define the main function to run the server
def run():
    # Specify the server address and port
    server_address = ('', 80)

    # Create an instance of HTTPServer with the custom CGI request handler class
    httpd = HTTPServer(server_address, CustomCGIHandler)

    # Print a message indicating that the server is running
    print('Server is running on port 80...')

    # Run the server indefinitely
    httpd.serve_forever()

# Call the main function to start the server
if __name__ == '__main__':
    run()
