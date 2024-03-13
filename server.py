from json import dumps
from os.path import basename

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urljoin, unquote

from search_engine import SearchEngine


CORPUS_PATH = "/course/small_wiki/"


def title(path: str) -> str:
    filename = basename(unquote(path))
    return filename[:filename.find(" - Wikipedia")]


def handler(search_engine: SearchEngine,
            corpus_path: str) -> SimpleHTTPRequestHandler:
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, directory="/", **kwargs)

        def do_GET(self) -> None:
            if self.path.startswith("/query"):
                query_string = self.path[len("/query?"):]
                s = parse_qs(query_string, keep_blank_values=True)["s"][0]
                if not s:
                    self.send("application/json", {"items": []})
                else:
                    result = [
                        {"url": path, "title": title(path)}
                        for path in search_engine.search(s)
                    ]
                    self.send("application/json", {"items": result})
            elif self.path == "/" or self.path == "/index.html":
                self.path = "/home/index.html"
                super().do_GET()
            elif self.path.startswith(corpus_path):
                # Redirect to en.wikipedia.org
                self.send_response(301)
                self.send_header("Location", urljoin(
                    "https://en.wikipedia.org/wiki/", title(self.path)
                ))
                self.end_headers()

        def send(self, content_type: str, data: str):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(dumps(data).encode("utf-8"))

        def log_message(self, format, *args) -> None:
            # Silence log messages
            return None

    return Handler


def main():
    engine = SearchEngine(CORPUS_PATH)

    # Create an HTTPServer listening on port 8000
    with HTTPServer(("", 8000), handler(engine, CORPUS_PATH)) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
