
def add(*args):
    return str(int(args[0]) + int(args[1]))

def subtract(*args):
    return str(int(args[0]) - int(args[1]))

def multiply(*args):
    return str(int(args[0]) * int(args[1]))

def divide(*args):
    return str(int(args[0]) / int(args[1]))

def index():
    page = """
     <html>
    <head>
    <title>Calculator</title>
    </head>
    <body bgcolor="purple" text="Gold">
    <h1>Basic URL Calculator</h1>
    <h2>How this works</h2>
    Simply type a basic math function at the end of the URL, followed by the numbers
      you would like to calculated.
      <br>
      All separated by a slash '/'
    <br>
    <br>
    For example, if you want to multiply two numbers, type multiply/first number/second number and hit enter.
    <br>
    5 times 6 would look like:
    <br>
    <br>
    localhost:8080/multiply/5/6
    <br>
    <br>
    results will be displayed back in the browser.  Sweet, eh?
    <br>
    <br>
    You can repeat this with add, subtract, and divide as well.
    <br>
    <br>
    <h2>Happy Mathing!</h2>
    </body>
    </html>
    """
    return page

def resolve_path(path):
    args = path.strip("/").split("/")
    func_name = args.pop(0)
    func = {
            "add" : add,
            "subtract" : subtract,
            "multiply": multiply,
            "divide": divide,
            "": index
            }.get(func_name)
    return func, args

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]



if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()