
__long_description__ = """\

▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██████╗▒▒██╗▒██████╗████████╗▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██╔══██╗███║██╔════╝╚══██╔══╝▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██║▒▒██║╚██║██║▒▒▒▒▒▒▒▒██║▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██║▒▒██║▒██║██║▒▒▒▒▒▒▒▒██║▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██████╔╝▒██║╚██████╗▒▒▒██║▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒╚═════╝▒▒╚═╝▒╚═════╝▒▒▒╚═╝▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒

    d1ct
    Another earth-shattering invention
    UltrafunkAmsterdam (c) 2021

    d1ct is a hybrid object/mapping. In contrast to some other attempts
    from several projects, this one is json serializable, subclassable, metaclassable,
    attribute-accessible, **unpackable, interchangable with dict and back.

    Oh minor detail: it is recursive, and autocomplete in your interactive shell works
    in 95% of the cases, even if it's list-nested.

    version 1.0.5
        - added the capability to not only accept dict-like mappings, but also lists of objects
          which will be returned as a list of d1ct-objects \
"""

__description__ = "dict implementation supporting attribute access, recursion, json, hashable, subclass, metaclass"
__version__ = "1.0.5"

from collections.abc import Sequence, Mapping

class d1ct(dict):

    def __new__(cls, *a, **kw):
        if hasattr(a, '__len__'):
            if len(a) > 0:
                if isinstance(a[0], (list, tuple)):
                    return [D1ct(_) for _ in a[0]]
        return super().__new__(cls)

    def __init__(self, *a, **kw):
        """
        One of the only data types in python which is:
         - directly inherited from dict
         - accessible by attribute.
         - This works also for all corner cases.
         - json.dumps json.reads
         - vars() works on it!
         - autocomplete works even if the objects comes from a list
         - best of all, it works recursively. So all inner dicts will become addicts too.
           How great this addict is, is TBD
           when code breaks, alwasys  first try commenting this out and try normal dicts.
           as this implementation might have effects which i did not notice yet.

        Parameters
        ----------
        *a
        **kw
        """

        super(D1ct, self).__init__(*a, **kw)
        object.__setattr__(self, "__dict__", self)
        for k, v in self.items():
            if isinstance(v, Mapping):
                setattr(self, k, D1ct(**v))
            elif isinstance(v, Sequence) and not isinstance(v, (str, bytes)):
                try:
                    try:
                        setattr(self, k, [D1ct(**i) for i in v])
                    except:
                        setattr(self, k, v.__class__([D1ct(i) for i in v]))
                except Exception as e:
                    # traceback.print_exc()
                    pass
            else:
                setattr(self, k, v)

    def __call__(self, *args, **kwargs):
        return self.__class__(*args, **kwargs)

    def __getitem__(self, key):
        return super(D1ct, self).__getitem__(key)

    def __setitem__(self, key, value):
        super(D1ct, self).__setitem__(key, value)
        super(D1ct, self).__setattr__(key, value)

    def __getattr__(self, attr):
        try:
            return getattr(super(D1ct, self), attr)
        except AttributeError:
            try:
                return self[attr]
            except KeyError:
                raise AttributeError(
                    f"{self.__class__.__name__} " f"has no attribute: {attr}"
                )

    def __setattr__(self, attr, val):
        try:
            super(D1ct, self).__setattr__(attr, val)
            super(D1ct, self).__setitem__(attr, val)
        except KeyError:
            raise AttributeError(
                f"{self.__class__.__name__} " f"has no attribute: {attr}"
            )

    def update(self, *a, **kw):
        """
        like dict.update()
        """
        d = {}
        if len(a) > 0:
            a = a[0]
            d.update(a)
            if isinstance(a, (str, bytes)):
                pass
        if kw:
            d.update(kw)
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = D1ct(v)
            elif isinstance(v, (list, set, tuple, frozenset)):
                d[k] = [D1ct(i) for i in v]
        super(D1ct, self).update(d)

    def __dir__(self):
        return object.__dir__(self) + list(super(D1ct, self).keys())



d1ct.__module__ = None
d1ct.__doc__ = __description__
d1ct.__version__ = __version__
D1ct = d1ct
import sys
sys.modules[__name__] = d1ct
