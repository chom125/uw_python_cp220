'''
Sample URLS:
http://localhost:8090/positive/5 ==> True
http://localhost:8090/positive/-5 ==> False
http://localhost:8090/negative/87 ==> False
http://localhost:8090/negative/-53 ==> True
'''

def negative(*args):
    '''
    should return the string 'true' if the first arg is less than 0,
    otherwise should return 'false'
    '''
    if int(args[0]) < 0:
        return 'true'
    else:
        return 'false'

def positive(*args):
    '''
    should return the string 'true' if the first arg is greater than 0,
    otherwise should return 'false'
    '''
    if int(args[0]) > 0:
        return 'true'
    else:
        return 'false'

def resolve_path(path):

    #remove any slashes at the beginning or end, then split by remaining slashes
    args = path.strip("/").split("/")

    #get the function name out of args, and remove it from the args variable
    #now args just holds the arguments, and func_name just has the function name
    func_name = args.pop(0)

    #create a dictionary that maps a word to its corresponding function
    func = {
        "positive" : positive,
        "negative" : negative
    }.get(func_name)

    #return the function and arguments
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
    srv = make_server('localhost', 8090, application)
    srv.serve_forever()