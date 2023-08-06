from typing import Union, Callable


class Meta(dict):
    """
    Usage:

        from fans.path import Path
        meta = Path('meta.json').as_meta(default = lambda: {'foo': 3})
        meta['bar'] = 5
        meta.save({'baz': 8})
    """

    def __init__(self, path: 'fans.Path', default: Callable[[], dict] = lambda: {}):
        self.path = path
        try:
            self.update(path.load())
        except:
            self.update(default())
            self.save()

    def save(self, meta: dict = None):
        self.update({**self, **(meta or {})})
        self.path.save(
            self,
            hint = 'json',
            indent = 2,
            ensure_ascii = False,
        )
