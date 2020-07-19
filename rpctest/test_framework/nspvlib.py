#!/usr/bin/env python3
# Copyright (c) 2020 SuperNET developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://www.opensource.org/licenses/mit-license.php.

from slickrpc import Proxy
import ujson
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
import ast
import time
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))


class NSPVProxy(Proxy):
    def __getattr__(self, method):
        conn = self.conn
        _id = next(self._ids)

        def call(*params):
            postdata = ujson.dumps({"jsonrpc": "2.0",
                                    "method": method,
                                    "params": params,
                                    "id": _id})
            body = StringIO()
            conn.setopt(conn.WRITEFUNCTION, body.write)
            conn.setopt(conn.POSTFIELDS, postdata)
            conn.perform()
            resp = ujson.loads(body.getvalue())
            return resp
        return call


class NspvRpcCalls:

    def __init__(self, node_ip="", user_pass=""):
        self.node_ip = node_ip
        self.user_pass = user_pass

    @ staticmethod
    def assert_equal(first, second):
        if first != second:
            raise AssertionError(first, "not equal to", second)

    def assert_success(self, result):
        self.assert_equal(result.get('result'), 'success')

    @ staticmethod
    def assert_in(result, key, compare_list):
        content = result.get(key)
        if content in compare_list:
            pass
        else:
            raise AssertionError("Error:", content, "not in", compare_list)

    def assert_contains(self, result, key):
        """assert key contains expected data"""
        if type(result) == bytes:
            result = self.type_convert(result)
        content = result.get(key)
        if content:
            pass
        else:
            raise AssertionError("Unexpected response, missing param: ", key)

    @ staticmethod
    def assert_not_contains(result, key):
        """assert key contains expected data"""
        content = result.get(key)
        if not content:
            pass
        else:
            raise AssertionError("Unexpected response, missing param: ", key)

    @ staticmethod
    def assert_error(result):
        """ assert there is an error with known error message """
        error_msg = ['no height', 'invalid height range', 'invalid method', 'timeout', 'error', 'no hex',
                     'couldnt get addressutxos', 'invalid address or amount too small', 'not enough funds',
                     'invalid address or amount too small', 'invalid utxo', 'wif expired', 'not implemented yet',
                     'invalid utxo']
        error = result.get('error')
        if error:
            if error in error_msg:
                pass
            else:
                raise AssertionError("Unknown error message")
        else:
            raise AssertionError("Unexpected response")

    @ staticmethod
    def type_convert(bytez):
        """Wraps nspv_call response"""
        # r = json.loads(bytes.decode("utf-8"))
        r = ast.literal_eval(bytez.decode("utf-8"))
        time.sleep(1)
        return r

    @staticmethod
    def proxy_connection(url):
        return NSPVProxy(url, timeout=240)
