# -*- coding: utf-8 -*-


"""
Copyright (c) 2018 Keijack Wu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from abc import abstractmethod
import json
import socket
import os
import re
from sys import prefix

import threading
import asyncio

from asyncio.base_events import Server
from concurrent.futures import ThreadPoolExecutor
from asyncio.streams import StreamReader, StreamWriter
from ssl import PROTOCOL_TLS_SERVER, SSLContext
from collections import OrderedDict
from socketserver import TCPServer
from time import sleep
from urllib.parse import unquote

from typing import Any, Callable, Dict, List, Tuple

from simple_http_server import ControllerFunction, StaticFile, WebsocketHandlerClass
from .http_protocol_handler import HttpProtocolHandler, SocketServerStreamRequestHandlerWraper
from .wsgi_request_handler import WSGIRequestHandler

from .__utils import remove_url_first_slash, get_function_args, get_function_kwargs, get_path_reg_pattern
from .logger import get_logger

_logger = get_logger("simple_http_server.http_server")


class RoutingServer:

    HTTP_METHODS = ["OPTIONS", "GET", "HEAD",
                    "POST", "PUT", "DELETE", "TRACE", "CONNECT"]

    def __init__(self, res_conf={}):
        self.method_url_mapping: Dict[str,
                                      Dict[str, List[ControllerFunction]]] = {"_": {}}
        self.path_val_url_mapping: Dict[str, Dict[str, List[Tuple(ControllerFunction, List[str])]]] = {
            "_": OrderedDict()}
        self.method_regexp_mapping: Dict[str, Dict[str, List[ControllerFunction]]] = {
            "_": OrderedDict()}
        for mth in self.HTTP_METHODS:
            self.method_url_mapping[mth] = {}
            self.path_val_url_mapping[mth] = OrderedDict()
            self.method_regexp_mapping[mth] = OrderedDict()

        self.filter_mapping = OrderedDict()
        self._res_conf = []
        self.add_res_conf(res_conf)

        self.ws_mapping: Dict[str, ControllerFunction] = OrderedDict()
        self.ws_path_val_mapping: Dict[str, ControllerFunction] = OrderedDict()
        self.ws_regx_mapping: Dict[str, ControllerFunction] = OrderedDict()

        self.error_page_mapping = {}

    def put_to_method_url_mapping(self, method, url, ctrl):
        if url not in self.method_url_mapping[method]:
            self.method_url_mapping[method][url] = []
        self.method_url_mapping[method][url].insert(0, ctrl)

    def put_to_path_val_url_mapping(self, method, path_pattern, ctrl, path_names):
        if path_pattern not in self.path_val_url_mapping[method]:
            self.path_val_url_mapping[method][path_pattern] = []
        self.path_val_url_mapping[method][path_pattern].insert(0, (ctrl, path_names))

    def put_to_method_regexp_mapping(self, method, regexp, ctrl):
        if regexp not in self.method_regexp_mapping[method]:
            self.method_regexp_mapping[method][regexp] = []
        self.method_regexp_mapping[method][regexp].insert(0, ctrl)

    @property
    def res_conf(self):
        return self._res_conf

    @res_conf.setter
    def res_conf(self, val: Dict[str, str]):
        self._res_conf.clear()
        self.add_res_conf(val)

    def add_res_conf(self, val: Dict[str, str]):
        if not val or not isinstance(val, dict):
            return
        for k, v in val.items():
            res_k = k
            if not res_k.startswith("*") and res_k.endswith('/'):
                # xxx/ equals xxx/*
                res_k = res_k + "*"
            if res_k.startswith('*'):
                suffix = res_k[2:] if res_k.startswith("**") else res_k[1:]
                assert suffix.find('/') < 0 and suffix.find('*') < 0, "If a resource path starts with *, only suffix can be configurated. "
            if res_k.startswith('**.'):
                # **.xxx
                suffix = res_k[3:]
                key = f'^[\\w%.\\-@!\\(\\)\\[\\]\\|\\$/]+\\.{suffix}$'
            elif res_k.startswith('*.'):
                # *.xxx
                suffix = res_k[2:]
                key = f'^[\\w%.\\-@!\\(\\)\\[\\]\\|\\$]+\\.{suffix}$'
            elif res_k.endswith("/**"):
                # xx/**
                prefix = res_k[0:-2]
                while prefix.startswith('/'):
                    prefix = prefix[1:]
                assert prefix.find("*") < 0, "You can only config a * or ** at the start or end of a path."
                key = f'^{prefix}([\\w%.\\-@!\\(\\)\\[\\]\\|\\$/]+)$'
            elif res_k.endswith("/*"):
                # xx/*
                prefix = res_k[0:-1]
                while prefix.startswith('/'):
                    prefix = prefix[1:]
                assert prefix.find("*") < 0, "You can only config a * or ** at the start or end of a path."
                key = f'^{prefix}([\\w%.\\-@!\\(\\)\\[\\]\\|\\$]+)$'

            if v.endswith(os.path.sep):
                val = v
            else:
                val = v + os.path.sep
            self._res_conf.append((key, val))

    def map_controller(self, ctrl: ControllerFunction):
        url = ctrl.url
        regexp = ctrl.regexp
        method = ctrl.method
        _logger.debug(
            f"map url {url}|{regexp} with method::{method}, headers::{ctrl.headers} and params::{ctrl.params} to function {ctrl.func}. ")
        assert method is None or method == "" or method.upper() in self.HTTP_METHODS
        _method = method.upper() if method is not None and method != "" else "_"
        if regexp:
            self.put_to_method_regexp_mapping(_method, regexp, ctrl)
        else:
            _url = remove_url_first_slash(url)

            path_pattern, path_names = get_path_reg_pattern(_url)
            if path_pattern is None:
                self.put_to_method_url_mapping(_method, _url, ctrl)
            else:
                self.put_to_path_val_url_mapping(_method, path_pattern, ctrl, path_names)

    def _res_(self, fpath: str):
        # fpath = os.path.join(res_dir, path.replace(res_regx, ""))
        # _logger.debug(f"static file. {path} :: {fpath}")
        fext = os.path.splitext(fpath)[1]
        ext = fext.lower()
        if ext in (".html", ".htm", ".xhtml"):
            content_type = "text/html"
        elif ext == ".xml":
            content_type = "text/xml"
        elif ext == ".css":
            content_type = "text/css"
        elif ext in (".jpg", ".jpeg"):
            content_type = "image/jpeg"
        elif ext == ".png":
            content_type = "image/png"
        elif ext == ".webp":
            content_type = "image/webp"
        elif ext == ".js":
            content_type = "text/javascript"
        elif ext == ".pdf":
            content_type = "application/pdf"
        elif ext == ".mp4":
            content_type = "video/mp4"
        elif ext == ".mp3":
            content_type = "audio/mp3"
        else:
            content_type = "application/octet-stream"

        return StaticFile(fpath, content_type)

    def get_url_controllers(self, path: str = "", method: str = "") -> List[Tuple[ControllerFunction, Dict, List]]:
        # explicitly url matching
        if path in self.method_url_mapping[method]:
            return [(ctrl, {}, ()) for ctrl in self.method_url_mapping[method][path]]
        elif path in self.method_url_mapping["_"]:
            return [(ctrl, {}, ()) for ctrl in self.method_url_mapping["_"][path]]

        # url with path value matching
        path_val_res = self.__try_get_from_path_val(path, method)
        if path_val_res is None:
            path_val_res = self.__try_get_from_path_val(path, "_")
        if path_val_res is not None:
            return path_val_res

        # regexp
        regexp_res = self.__try_get_ctrl_from_regexp(path, method)
        if regexp_res is None:
            regexp_res = self.__try_get_ctrl_from_regexp(path, "_")
        if regexp_res is not None:
            return regexp_res
        # static files
        for k, v in self.res_conf:
            match_static_path_conf = re.match(k, path)
            _logger.debug(f"{path} macth static file conf {k} ? {match_static_path_conf}")
            if match_static_path_conf:
                if match_static_path_conf.groups():
                    fpath = f"{v}{match_static_path_conf.group(1)}"
                else:
                    fpath = f"{v}{path}"

                def static_fun():
                    return self._res_(fpath)
                return [(ControllerFunction(func=static_fun), {}, ())]
        return []

    def __try_get_ctrl_from_regexp(self, path, method):
        for regex, ctrls in self.method_regexp_mapping[method].items():
            m = re.match(regex, f"/{path}") or re.match(regex, path)
            _logger.debug(
                f"regexp::pattern::[{regex}] => path::[{path}] match? {m is not None}")
            if m:
                res = []
                grps = tuple([unquote(v) for v in m.groups()])
                for ctrl in ctrls:
                    res.append((ctrl, [], grps))
                return res
        return None

    def __try_get_from_path_val(self, path, method):
        for patterns, val in self.path_val_url_mapping[method].items():
            m = re.match(patterns, path)
            _logger.debug(
                f"url with path value::pattern::[{patterns}] => path::[{path}] match? {m is not None}")
            if m:
                res = []
                for ctrl_fun, path_names in val:
                    path_values = {}
                    for idx in range(len(path_names)):
                        key = unquote(path_names[idx])
                        path_values[key] = unquote(m.groups()[idx])
                    res.append((ctrl_fun, path_values, ()))
                return res
        return None

    def map_filter(self, filter_conf: Dict[str, Any]):
        # {"path": p, "url_pattern": r, "func": filter_fun}
        path = filter_conf["path"] if "path" in filter_conf else ""
        regexp = filter_conf["url_pattern"]
        filter_fun = filter_conf["func"]
        if path:
            regexp = get_path_reg_pattern(path)[0]
            if not regexp:
                regexp = f"^{path}$"
        _logger.debug(
            f"[path: {path}] map url regexp {regexp} to function: {filter_fun}")
        self.filter_mapping[regexp] = filter_fun

    def get_matched_filters(self, path):
        return self._get_matched_filters(remove_url_first_slash(path)) + self._get_matched_filters(path)

    def _get_matched_filters(self, path):
        available_filters = []
        for regexp, val in self.filter_mapping.items():
            m = re.match(regexp, path)
            _logger.debug(
                f"filter:: [{regexp}], path:: [{path}] match? {m is not None}")
            if m:
                available_filters.append(val)
        return available_filters

    def map_websocket_handler(self, handler: WebsocketHandlerClass):
        url = handler.url
        regexp = handler.regexp
        _logger.debug(
            f"map url {url}|{regexp} to controller class {handler.cls}")
        if regexp:
            self.ws_regx_mapping[regexp] = handler
        else:
            url = remove_url_first_slash(url)
            path_pattern, path_names = get_path_reg_pattern(url)
            if path_pattern is None:
                self.ws_mapping[url] = handler
            else:
                self.ws_path_val_mapping[path_pattern] = (handler, path_names)

    def get_websocket_handler(self, path):
        # explicitly mapping
        if path in self.ws_mapping:
            return self.ws_mapping[path], {}, ()

        # path value mapping
        handler, path_vals = self.__try_get_ws_handler_from_path_val(path)
        if handler is not None:
            return handler, path_vals, ()
        # regexp mapping
        return self.__try_get_ws_hanlder_from_regexp(path)

    def __try_get_ws_hanlder_from_regexp(self, path):
        for regex, handler in self.ws_regx_mapping.items():
            m = re.match(regex, f"/{path}") or re.match(regex, path)
            _logger.debug(
                f"regexp::pattern::[{regex}] => path::[{path}] match? {m is not None}")
            if m:
                return handler, {}, tuple([unquote(v) for v in m.groups()])
        return None, {}, ()

    def __try_get_ws_handler_from_path_val(self, path):
        for patterns, val in self.ws_path_val_mapping.items():
            m = re.match(patterns, path)
            _logger.debug(
                f"websocket endpoint with path value::pattern::[{patterns}] => path::[{path}] match? {m is not None}")
            if m:
                handler, path_names = val
                path_values = {}
                for idx in range(len(path_names)):
                    key = unquote(path_names[idx])
                    path_values[key] = unquote(m.groups()[idx])
                return handler, path_values
        return None, {}

    def map_error_page(self, code: str, error_page_fun: Callable):
        if not code:
            c = "_"
        else:
            c = str(code).lower()
        self.error_page_mapping[c] = error_page_fun

    def _default_error_page(self, code: int, message: str = "", explain: str = ""):
        return json.dumps({
            "code": code,
            "message": message,
            "explain": explain
        })

    def error_page(self, code: int, message: str = "", explain: str = ""):
        c = str(code)
        func = None
        if c in self.error_page_mapping:
            func = self.error_page_mapping[c]
        elif code > 200:
            c0x = c[0:2] + "x"
            if c0x in self.error_page_mapping:
                func = self.error_page_mapping[c0x]
            elif "_" in self.error_page_mapping:
                func = self.error_page_mapping["_"]

        if not func:
            func = self._default_error_page
        _logger.debug(f"error page function:: {func}")

        co = code
        msg = message
        exp = explain

        args_def = get_function_args(func, None)
        kwargs_def = get_function_kwargs(func, None)

        args = []
        for n, t in args_def:
            _logger.debug(f"set value to error_page function -> {n}")
            if co is not None:
                if t is None or t == int:
                    args.append(co)
                    co = None
                    continue
            if msg is not None:
                if t is None or t == str:
                    args.append(msg)
                    msg = None
                    continue
            if exp is not None:
                if t is None or t == str:
                    args.append(exp)
                    exp = None
                    continue
            args.append(None)

        kwargs = {}
        for n, v, t in kwargs_def:
            if co is not None:
                if (t is None and isinstance(v, int)) or t == int:
                    kwargs[n] = co
                    co = None
                    continue
            if msg is not None:
                if (t is None and isinstance(v, str)) or t == str:
                    kwargs[n] = msg
                    msg = None
                    continue
            if exp is not None:
                if (t is None and isinstance(v, str)) or t == str:
                    kwargs[n] = exp
                    exp = None
                    continue
            kwargs[n] = v

        if args and kwargs:
            return func(*args, **kwargs)
        elif args:
            return func(*args)
        elif kwargs:
            return func(**kwargs)
        else:
            return func()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def start_async(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass


class HTTPServer(TCPServer, RoutingServer):

    allow_reuse_address = 1    # Seems to make sense in testing environment

    _default_max_workers = 50

    def server_bind(self):
        """Override server_bind to store the server name."""
        TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

    def __init__(self, addr, res_conf={}, max_workers: int = None):
        TCPServer.__init__(self, addr, SocketServerStreamRequestHandlerWraper)
        RoutingServer.__init__(self, res_conf)
        self.max_workers = max_workers or self._default_max_workers
        self.threadpool: ThreadPoolExecutor = ThreadPoolExecutor(
            thread_name_prefix="ReqThread",
            max_workers=self.max_workers)

    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)

    # override
    def process_request(self, request, client_address):
        self.threadpool.submit(
            self.process_request_thread, request, client_address)

    def server_close(self):
        super().server_close()
        self.threadpool.shutdown(True)

    def start(self):
        self.serve_forever()

    async def start_async(self):
        self.start()

    def _shutdown(self) -> None:
        _logger.debug("shutdown http server in a seperate thread..")
        super().shutdown()

    def shutdown(self) -> None:
        threading.Thread(target=self._shutdown, daemon=False).start()


class CoroutineHTTPServer(RoutingServer):

    def __init__(self, host: str = '', port: int = 9090, ssl: SSLContext = None, res_conf={}) -> None:
        RoutingServer.__init__(self, res_conf)
        self.host: str = host
        self.port: int = port
        self.ssl: SSLContext = ssl
        self.server: Server = None
        self.__thread_local = threading.local()

    async def callback(self, reader: StreamReader, writer: StreamWriter):
        handler = HttpProtocolHandler(reader, writer, routing_conf=self)
        await handler.handle_request()
        _logger.debug("Connection ends, close the writer.")
        writer.close()

    async def start_async(self):
        self.server = await asyncio.start_server(
            self.callback, host=self.host, port=self.port, ssl=self.ssl)
        async with self.server:
            try:
                await self.server.serve_forever()
            except asyncio.exceptions.CancelledError:
                _logger.debug(
                    "Some requests are lost for the reason that the server is shutted down.")
            finally:
                await self.server.wait_closed()

    def _get_event_loop(self) -> asyncio.AbstractEventLoop:
        if not hasattr(self.__thread_local, "event_loop"):
            try:
                self.__thread_local.event_loop = asyncio.new_event_loop()
            except:
                self.__thread_local.event_loop = asyncio.get_event_loop()
        return self.__thread_local.event_loop

    def start(self):
        self._get_event_loop().run_until_complete(self.start_async())

    def _shutdown(self):
        _logger.debug("Try to shutdown server.")
        self.server.close()
        loop = self.server.get_loop()
        loop.call_soon_threadsafe(loop.stop)

    def shutdown(self):
        wait_time = 3
        while wait_time:
            sleep(1)
            _logger.debug(f"couting to shutdown: {wait_time}")
            wait_time = wait_time - 1
            if wait_time == 0:
                _logger.debug("shutdown server....")
                self._shutdown()


class SimpleDispatcherHttpServer:
    """Dispatcher Http server"""

    def map_filter(self, filter_conf):
        self.server.map_filter(filter_conf)

    def map_controller(self, ctrl: ControllerFunction):
        self.server.map_controller(ctrl)

    def map_websocket_handler(self, handler: WebsocketHandlerClass):
        self.server.map_websocket_handler(handler)

    def map_error_page(self, code, func):
        self.server.map_error_page(code, func)

    def __init__(self,
                 host: Tuple[str, int] = ('', 9090),
                 ssl: bool = False,
                 ssl_protocol: int = PROTOCOL_TLS_SERVER,
                 ssl_check_hostname: bool = False,
                 keyfile: str = "",
                 certfile: str = "",
                 keypass: str = "",
                 ssl_context: SSLContext = None,
                 resources: Dict[str, str] = {},
                 prefer_corountine=False,
                 max_workers: int = None):
        self.host = host
        self.__ready = False

        self.ssl = ssl

        if ssl:
            if ssl_context:
                self.ssl_ctx = ssl_context
            else:
                assert keyfile and certfile, "keyfile and certfile should be provided. "
                ssl_ctx = SSLContext(protocol=ssl_protocol)
                ssl_ctx.check_hostname = ssl_check_hostname
                ssl_ctx.load_cert_chain(
                    certfile=certfile, keyfile=keyfile, password=keypass)
                self.ssl_ctx = ssl_ctx
        else:
            self.ssl_ctx = None

        if prefer_corountine:
            _logger.info(
                f"Start server in corouting mode, listen to port: {self.host[1]}")
            self.server = CoroutineHTTPServer(
                self.host[0], self.host[1], self.ssl_ctx, resources)
        else:
            _logger.info(
                f"Start server in threading mixed mode, listen to port {self.host[1]}")
            self.server = HTTPServer(
                self.host, resources, max_workers=max_workers)
            if self.ssl_ctx:
                self.server.socket = self.ssl_ctx.wrap_socket(
                    self.server.socket, server_side=True)

    @property
    def ready(self):
        return self.__ready

    def resources(self, res={}):
        self.server.res_conf = res

    def start(self):
        try:
            self.__ready = True
            self.server.start()
        except:
            self.__ready = False
            raise

    async def start_async(self):
        try:
            self.__ready = True
            await self.server.start_async()
        except:
            self.__ready = False
            raise

    def shutdown(self):
        # shutdown it in a seperate thread.
        self.server.shutdown()


class WSGIProxy(RoutingServer):

    def __init__(self, res_conf):
        super().__init__(res_conf=res_conf)

    def app_proxy(self, environment, start_response):
        return asyncio.run(self.async_app_proxy(environment, start_response))

    async def async_app_proxy(self, environment, start_response):
        request_handler = WSGIRequestHandler(self, environment, start_response)
        return await request_handler.handle_request()
