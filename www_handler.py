#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import re
import argparse
import dbus


class WWWHandler(BaseHTTPRequestHandler):
    def _send_response(self, message, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        if self.path == '/current_logo':
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            logo = '/opt/victronenergy/themes/ccgx/images/mobile-builder-logo.png'
            if os.path.isfile('/data/themes/overlay/mobile-builder-logo.png'):
                logo = '/data/themes/overlay/mobile-builder-logo.png'
            with open(logo, 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/reset_logo':
            if os.path.isfile('/data/themes/overlay/mobile-builder-logo.png'):
                os.unlink('/data/themes/overlay/mobile-builder-logo.png')
            self._send_response('ok')
        elif self.path == '/language':
            bus = dbus.SystemBus()
            try:
                langObject = bus.get_object('com.victronenergy.settings', '/Settings/Gui/Language')
            except dbus.DBusException:
                raise SystemExit('### Fetching object failed')

            try:
                langValue = langObject.GetValue(dbus_interface='com.victronenergy.BusItem')
            except:
                langValue = 'unknown'
            self._send_response(langValue)
        else:
            self._send_response('404 Not Found', status=404)

    def do_POST(self):
        if self.path == '/salt':
            if not os.path.isfile('/data/conf/vncpassword.txt'):
                salt = ''
            else:
                with open('/data/conf/vncpassword.txt', 'r') as f:
                    salt = f.read(29)
                match = re.search(r'^\$2a\$08\$[A-Za-z0-9+\\.\/]{22}$', salt)
                if not match:
                    salt = ''
            self._send_response(salt)
        else:
            self._send_response('404 Not Found', status=404)

    def do_PUT(self):
        filename = "/data/themes/overlay/mobile-builder-logo.png"

        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'ok'
        self.wfile.write(reply_body.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=WWWHandler, port=9249):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9249,
                        help='The port to listen on')
    return parser.parse_args()


def main():
    try:
        bus = dbus.SystemBus()
    except dbus.DBusException:
        raise SystemExit("### Failed to connect to SystemBus!")

    args = parse_args()
    if args.port:
        run(port=args.port)
    else:
        run()


if __name__ == '__main__':
    main()
