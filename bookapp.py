from bookdb import BookDB
import traceback

DB = BookDB()


def book(book_id):
    info = DB.title_info(book_id)
    if info is None:
        raise NameError
    response_body = f"<h1>{info['title']}</h1>\n" + \
        f"<p><b>Author</b>: {info['author']}<br>" + \
        f"<b>Publisher</b>: {info['publisher']}<br>" + \
        f"<b>ISBN</b>: {info['isbn']}<br>" + \
        f"<a href='/'>Back to the list</a></p>"
    return response_body


def books():
    response_body = ["<h2>My Bookshelf</h2>", "<ul>"]
    for title in DB.titles():
        response_body.append(f"<li><a href=/book/{title['id']}>{title['title']}</a></li>")
    response_body.append("</ul>")
    return '\n'.join(response_body)


def resolve_path(path):
    funcs = {
        '': books,
        'book': book,
    }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get("PATH_INFO", None)
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
        print(traceback.format_exc())
    finally:
        headers.append(("Content-length", str(len(body))))
        start_response(status, headers)
        return [body.encode()]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
