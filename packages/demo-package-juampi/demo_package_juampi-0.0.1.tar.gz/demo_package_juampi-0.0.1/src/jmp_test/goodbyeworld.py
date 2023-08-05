def say_goodbye(name=None):
    if name is None:
        return "goodbye, World!"
    else:
        return f"goodbye, {name}!"