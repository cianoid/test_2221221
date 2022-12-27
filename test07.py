nvl = lambda string, replace: replace if string is None else string  # noqa

assert nvl("test", 2) == "test"
assert nvl(None, "notest") == "notest"
