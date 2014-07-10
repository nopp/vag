"""
Simple Python Varnish socket interface.
"""
import socket, re, string, json

try:
    import hashlib
    hashlib_loaded = True
except ImportError:
    hashlib_loaded = False

class VarnishAdminSocket(object):
    """Varnish Administration Socket Library"""
    def __init__(self, **kwargs):
        """Initialise the Class, default some variables"""

        # Check kwargs for overrides
        self.host = kwargs.pop('host', '127.0.0.1')
        self.port = kwargs.pop('port', 6082)
        self.secret = kwargs.pop('secret', False)
        self.timeout = kwargs.pop('timeout', 5)
        self.secret_file = kwargs.pop('secret_file', False)

        # If auto_connect = True, attempt to connect on instantiation
        self.auto_connect = kwargs.pop('auto_connect', False)
        if self.auto_connect:
            self.connect()
        else:
            self.conn = False

    # Connect to the socket and attempt authentication if necessary
    def connect(self):
        """Make the socket connection"""

        # Determine if we were able to import hashlib. We can't do secret key authentication
        # without it.
        global hashlib_loaded

        # Try to use self.timeout, if we can't make it into an integer
        # default to 5
        try:
            local_timeout = int(self.timeout)
        except ValueError:
            local_timeout = 5

        # Connect to the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(1)
        sock.settimeout(local_timeout)

        # Enforce integer for the port
        try:
            self.port = int(self.port)
        except ValueError:
            # Port couldn't be made an integer
            self.close()
            raise Exception('VarnishAdminSocket: Port could not be made an integer')
            return False

        # Make the connection
        sock.connect( (self.host, self.port) )

        # Store the socket makefile
        self.conn = sock.makefile()

        # Close the socket object now that we have makefile
        sock.close()

        # Read the banner
        (code, response) = self.read()

        # If we get code 107, we need to try to authenticate
        if code == 107:
            # Hashlib needs to be loaded for secret key authentication
            # If it's not loaded, raise an error
            if not hashlib_loaded:
                e = "VarnishAdminSocket: The hashlib module must be available for secret key authentication"
                raise Exception(e)

            # Run get secret to try to load
            # the secret from a file if secret_file is set
            self.__get_secret()

            # Check to make sure we've defined a secret key
            if not self.secret:
                raise Exception("VarnishAdminSocket: Authentication is required, please set the secret key.")
                self.close()
                return False

            challenge = string.split(response, "\n", 1)[0]
            secret = self.secret

            # Try for hashlib
            auth_response = hashlib.sha256("%s\n%s%s\n" % (challenge, secret, challenge)).hexdigest()

            (check_code, check_response) = self.send("auth " + auth_response)
            if check_code != 200:
                raise Exception("VarnishAdminSocket: Bad Authentication")
                return False
                self.close()
        else:
            return True

    # Runs the status command and returns true or false
    def status(self):
        """Runs the status command and returns true or false"""
        (code, response) = self.send('status')
        s = re.search('Child in state (\w+)', response)
        if s:
            if(s.group(1) == "running"):
                return True
            else:
                return False
        else:
            return False

    ## Commands ##

    # Alias for the ban command
    # Returns the code
    def ban(self, expr):
        """Send a ban command to Varnish"""
        (code, response) = self.send("ban %s" % expr)
        return code

    # Alias for the ban.url command
    # Returns the code
    def ban_url(self,path):
        """Send a ban command to Varnish"""
        (code, response) = self.send("ban.url %s" % path)
        return code

    # Runs the ban.list command
    # Returns the response
    def ban_list(self):
        """Runs the ban.list command"""
        (code, response) = self.send("ban.list")
        return response

    # Runs the vcl.list command
    # Returns the response
    def vcl_list(self):
        """Runs the vcl.list command"""
        (code, response) = self.send("vcl.list")
        return response

    def vcl_show(self,vclName):
        """Runs the ban.list command"""
        (code, response) = self.send("vcl.show "+vclName)
        return response

    def vcl_inline(self,vclName,vclContent):
		"""Runs the vcl.inline command"""
		(code, response) = self.send('vcl.inline '+vclName+' "'+vclContent+'"')
		return response

	#def vcl_use(self,vclName):
	#	"""Runs the vcl.use command"""
	#	(code, response) = self.send("vcl.use "+vclName)
	#	return response

    # Send the start command
    # Returns true or false
    def start(self):
        """Send the start command"""
        (code, response) = self.send("start")
        if code == 200:
            return True
        else:
            return False

    # Send the stop command
    # Returns true or false
    def stop(self):
        """Send the stop command"""
        (code, response) = self.send("stop")
        if code == 200:
            return True
        else:
            return False

    # Run any varnish command
    # Returns the response and code
    # ok = the code varnish needs to return for this function to return response,
    # otherweise the function returns False
    def command(self, cmd, ok=200):
        """Runs any command against the varnish socket and returns the response"""
        ok = int(ok)
        (code, response) = self.send(cmd)
        if(code == ok):
            return response
        else:
            # Raise an exception
            return False

    # Send a command to the socket
    def send(self, cmd):
        """Sends a command to the socket"""
        if not self.conn:
            raise Exception('Your are not connected')
            return False

        self.conn.write("%s\n" % cmd)
        self.conn.flush()

        read = self.read()
        if self.auto_connect and not re.match("auth|quit", cmd):
            self.quit()
        return read

    # Read from the socket
    def read(self):
        """Returns the socket information"""
        # TODO: Raise exceptions here if we can't read
        (code, blen) = self.conn.readline().split()
        msg = self.conn.read(int(blen)+1)

        return [int(code), msg.rstrip()]

    # Returns boolean for self.conn
    def connected(self):
        """Return connection status"""
        if self.conn:
            return True
        else:
            return False

    # A more graceful quit, send the quit command first, then closes the socket
    def quit(self):
        """Graceful quit"""
        self.send('quit')
        return self.close()

    # Close the socket
    def close(self):
        """Close the socket connection"""
        if self.connected():
            self.conn.close()
        self.conn = False
        return True

    # If self.secret_file is set we'll try to load the file into self.secret
    # If we can't load the file, or self.secret_file is not set, we return
    # self.secret
    def __get_secret(self):
        # If a secret file is set, try to load it, and set the
        if self.secret_file:
            try:
                load = open(self.secret_file).read()
                self.secret = load
                return load
            except:
                return False

        # Default to returning the contents of the secret var
        return self.secret
