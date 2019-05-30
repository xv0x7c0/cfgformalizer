def clone(func):
    def decorator(self, *args, **kwargs):
        new_self = self.__class__.__new__(self.__class__)
        new_self.statements = self.statements.copy()
        func(new_self, *args, **kwargs)
        return new_self

    return decorator
