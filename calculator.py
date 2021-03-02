"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
def index(*args) -> str:
    return '''
<h1>Simple calcualtor.</h1>
Usage:<br>
http://localhost:8080/[command]/[num1]/[num2]<br>
where commands are:<br>
    -add<br>
    -divide<br>
    -multiply<br>
    -subtract<br>
and num1 and num2 are integers'''

def add(*args) -> str:
    """ Returns a STRING with the sum of the arguments """
    return str(args[0] + args[1]) 

def subtract(*args) -> str:
    """ Returns a STRING with the difference of the arguments """
    return str(args[0]-args[1]) 

def multiply(*args) -> str:
    """ Returns a STRING with the multiplication of the arguments """
    return str(args[0] * args[1]) 

def divide(*args) -> str:
    """ Returns a STRING with the division of the arguments """
    return str(args[0]/args[1]) 

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    print('Resolving path')
    func_dict = {'add': add,
                'multiply': multiply,
                'subtract': subtract,
                'divide': divide,
                '': index }

    try:
        func_str, *args = path.strip('/').split('/')
        args = args or []
        func = func_dict[func_str]
        args = int(args[0]),int(args[1])
    except KeyError:
        raise NameError
    except IndexError:
        if func_str != '':
            raise NameError
    return func, args
import traceback
def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    import pprint
    #pprint.pprint(environ)
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found, wrong link format</h1>"
        print(traceback.format_exc())
    except ZeroDivisionError:
        status = '500 Internal Server Error'
        body = ' <h1> Tried to divide by zero...</h1>'
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def main():
        print('Starting server at 8080.')
        from wsgiref.simple_server import make_server
        srv = make_server('localhost', 8080, application)
        srv.serve_forever()

# start the WSGI server at http://localhost:8080 
if __name__ == '__main__':
    main()


