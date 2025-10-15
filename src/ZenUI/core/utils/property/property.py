def make_getter(name):
    def getter(self):
        return getattr(self, f'_{name}')
    return getter