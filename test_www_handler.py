#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import re
import argparse
import pytest
import threading
import requests
from www_handler import WWWHandler

@pytest.fixture
def server():
    httpd = HTTPServer(('', 8000), WWWHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    yield
    httpd.shutdown()
    httpd.server_close()
    thread.join()


def test_root_route(server):
    response = requests.get('http://localhost:8000/')
    assert response.status_code == 404
    response = requests.post('http://localhost:8000/')
    assert response.status_code == 404


def test_current_logo_route(server):
    response = requests.get('http://localhost:8000/current_logo')
    assert response.status_code == 200


def test_reset_logo_route(server):
    response = requests.get('http://localhost:8000/reset_logo')
    assert response.status_code == 200


def test_salt_route(server):
    response = requests.get('http://localhost:8000/salt')
    assert response.status_code == 404
    response = requests.post('http://localhost:8000/salt')
    assert response.status_code == 200
    assert response.text == ''


def test_upload_route(server):
    response = requests.put('http://localhost:8000/upload')
    assert response.status_code == 201
