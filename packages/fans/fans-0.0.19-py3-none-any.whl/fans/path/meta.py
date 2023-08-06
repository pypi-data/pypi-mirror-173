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
        self.default = default
        self.loaded = False

    def save(self, meta: dict = None):
        self.update({**self, **(meta or {})})
        self.path.save(
            self,
            hint = 'json',
            indent = 2,
            ensure_ascii = False,
        )

    def load(self):
        try:
            self.update(self.path.load(hint = 'json'))
        except:
            self.update(self.default())
            self.save()
        self.loaded = True

    def __getitem__(self, *args, **kwargs):
        if not self.loaded:
            self.load()
        return super().__getitem__(*args, **kwargs)

    def get(self, *args, **kwargs):
        if not self.loaded:
            self.load()
        return super().get(*args, **kwargs)
