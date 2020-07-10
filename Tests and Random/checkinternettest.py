import socket

def CheckInternet(host = "8.8.8.8", port = 53, timeout = 3):
    # Checks google-public-dns-a.google.com for internet connection on 53/tcp
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

print(CheckInternet())
