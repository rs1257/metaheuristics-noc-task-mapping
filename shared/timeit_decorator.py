from timeit import default_timer as timer

times = []
def timeit(method):
    def timed(*args, **kw):
        ts = timer()
        result = method(*args, **kw)
        te = timer()
        difference = (te - ts)
        print('%r  %2.2f seconds' % (method.__name__, difference))
        times.append(difference)
        return result
    return timed
