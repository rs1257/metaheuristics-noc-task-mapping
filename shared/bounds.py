def check_bounds_ga(min_, max_):
    def decorator(func):
        def wrapper(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                for i in range(len(child)):
                    if child[i] > max_:
                        child[i] = max_
                    elif child[i] < min_:
                        child[i] = min_
            return offspring
        return wrapper
    return decorator


def check_bounds_pso(min_, max_):
    def decorator(func):
        def wrapper(*args, **kargs):
            part = func(*args, **kargs)
            for p in range(len(part)):
                if part[p] < min_:
                    part[p] = min_
                elif part[p] > max_:
                    part[p] = max_
            return part
        return wrapper
    return decorator
