#!/usr/bin/env python3
import socketserver
import sys
from http.server import SimpleHTTPRequestHandler


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


PORT = 8001

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8001.")

    # Big red startup message with emojis and ASCII art
    print("\n" + "=" * 60)
    print("🚀 " + "\033[1;31m" + "PCA TEACHERS SERVER STARTING" + "\033[0m" + " 🚀")
    print("=" * 60)
    print(
        "📡 "
        + "\033[1;33m"
        + "PORT REUSE ENABLED"
        + "\033[0m"
        + " - No more 'Address already in use' errors! 🎉"
    )
    print("🌐 " + "\033[1;36m" + "CORS ENABLED" + "\033[0m" + " - Cross-origin requests allowed 🔓")
    print("=" * 60)

    with ReusableTCPServer(("", PORT), CORSRequestHandler) as httpd:
        print(f"🔥 \033[1;32mServer blazing at http://localhost:{PORT}/\033[0m 🔥")
        print("⚡ \033[1;35mPress Ctrl+C to stop the server\033[0m ⚡")
        print("=" * 60 + "\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n" + "=" * 60)
            print("🛑 " + "\033[1;31m" + "SERVER STOPPED" + "\033[0m" + " 🛑")
            print(
                "👋 " + "\033[1;33m" + "Thanks for using PCA Teachers Server!" + "\033[0m" + " 👋"
            )
            print("=" * 60)
            httpd.shutdown()
