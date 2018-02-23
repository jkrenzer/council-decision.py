
def _transform(value, cast, default=None):
    if type(cast) is type and type(value) is cast:
        return value
    if cast is not None:
        try:
            value = cast(value)
        except ValueError:
            value = default
    return value
