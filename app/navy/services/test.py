# example of decorator for validation a field before to execute a function
ok = False


def is_ok(f):
    def wrapper(g):
        if g:
            f(g)
        else:
            print("not ok")

    return wrapper


@is_ok
def f(g):
    print("ok")
