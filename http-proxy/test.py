from unittest import TestCase
from time import sleep
from cache import Cache
from message import Message

class Test(TestCase):

    def test_create_message(self):
        message = Message()
        message.set_start_line("GET /background.png HTTP/1.0")
        message.add_header('Host', 'example.org')
        message.add_header('Content-Length', '110')
        message.append_to_body(b'<html><body><a href="http://example.com/about.html#contacts">Click here</a></body></html>')
        self.assertEqual(b'GET /background.png HTTP/1.0\r\nHost: example.org\r\nContent-Length: 110\r\n\r\n<html><body><a href="http://example.com/about.html#contacts">Click here</a></body></html>\r\n', message.to_bytes())

    def test_get_host_message(self):
        message = Message()
        message.set_start_line("GET /background.png HTTP/1.0")
        message.add_header('Host', 'example.org')
        message.add_header('Content-Length', '110')
        message.append_to_body(b'<html><body><a href="http://example.com/about.html#contacts">Click here</a></body></html>')
        host = message.get_host()
        self.assertEqual(('example.org', 80), host)

    def test_need_cash_message(self):
        message = Message()
        message.set_start_line("GET /background.png HTTP/1.0")
        message.add_header('Host', 'example.org')
        message.add_header('Content-Length', '110')
        message.append_to_body(b'<html><body><a href="http://example.com/about.html#contacts">Click here</a></body></html>')
        can = message.can_cache()
        message.add_header('Cache-Control', 'no-store')
        cant = message.can_cache()
        self.assertEqual(True, can)
        self.assertEqual(False, cant)

    def test_put_in_cash(self):
        message = Message()
        message.set_start_line("GET /background.png HTTP/1.0")
        message.add_header('Host', 'example.org')
        message.add_header('Content-Length', '110')
        message.append_to_body(b'<html><body><a href="http://example.com/about.html#contacts">Click here</a></body></html>')
        cache = Cache(1000, 100000)
        cache.put(message, message)
        _, getting_message = cache.get(message)
        self.assertEqual(message, getting_message)

    def test_expire_cash(self):
        message = Message()
        message.set_start_line("GET /background.png HTTP/1.0")
        message.add_header('Host', 'example.org')
        message.add_header('Content-Length', '110')
        message.append_to_body(
            b'<html><body><a href="http://example.com/about.html#contacts">Click here</a></body></html>')
        cache = Cache(1, 100000)
        cache.put(message, message)
        sleep(5)
        getting_message = cache.get(message)
        self.assertEqual(None, getting_message)

    def test_size_cash(self):
        message = Message()
        message1 = Message()
        message.set_start_line("GET /background.png HTTP/1.0")
        message1.set_start_line("GET /background.png HTTP/1.0")
        message.add_header('Host', 'example.org')
        message.add_header('Content-Length', '110')
        message1.add_header('Content-Length', '110')
        message.append_to_body(
            b'<html><body><a href="http://example.com/about.html#contacts">Click here</a></body></html>')
        message1.append_to_body(
            b'<html><body><a href="http://example.com/about.html#contacts">Click here</a></body></html>')
        cache = Cache(100000, 1)
        cache.put(message, message)
        _, getting_message = cache.get(message)
        cache.put(message1, message1)
        _, getting_message1 = cache.get(message1)
        empty_message = cache.get(message)
        self.assertEqual(message, getting_message)
        self.assertEqual(message1, getting_message1)
        self.assertEqual(None, empty_message)
