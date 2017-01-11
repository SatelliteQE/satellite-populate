# coding: utf-8
import logging
from copy import deepcopy

import import_string
from nailgun.entity_mixins import Entity
from six import string_types
from six.moves import builtins

try:
    # coloredlogs is optional, used only when installed
    import coloredlogs
except ImportError:
    coloredlogs = None

DICT_RESERVED_KEYS = list(vars(dict).keys())


class SmartDict(dict):
    """
    A Dict which is accessible via attribute dot notation
    """

    def __init__(self, *args, **kwargs):
        """
        :param args: multiple dicts ({}, {}, ..)
        :param kwargs: arbitrary keys='value'

        If ``keyerror=False`` is passed then not found attributes will
        always return None.
        """
        super(SmartDict, self).__init__()
        self['__keyerror'] = kwargs.pop('keyerror', True)
        [self.update(arg) for arg in args if isinstance(arg, dict)]
        self.update(kwargs)

    def __getattr__(self, attr):
        if attr not in DICT_RESERVED_KEYS:
            if self['__keyerror']:
                return self[attr]
            else:
                return self.get(attr)
        return getattr(self, attr)

    def __setattr__(self, key, value):
        if key in DICT_RESERVED_KEYS:
            raise TypeError("You cannot set a reserved name as attribute")
        self.__setitem__(key, value)

    def __copy__(self):
        return self.__class__(self)

    def copy(self):
        return self.__copy__()


def set_logger(verbose):
    """Set logger verbosity used when client is called with -vvvvv"""

    for _logger in list(logging.Logger.manager.loggerDict.values()):  # noqa
        if not isinstance(_logger, logging.Logger):
            continue
        if coloredlogs is not None:
            _logger.propagate = False

            handler = logging.StreamHandler()
            formatter = coloredlogs.ColoredFormatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            _logger.handlers = [handler]
        _logger.setLevel(verbose * 10)


def import_from_string(import_name, *args, **kwars):
    """Try import string and then try builtins"""
    try:
        return import_string(import_name, *args, **kwars)
    except:
        new_import_name = "{0}.{1}".format(builtins.__name__, import_name)
        try:
            return import_string(new_import_name, *args, **kwars)
        except Exception as e:
            raise ImportError(
                "%s cannot be imported, is that installed? error: %s" %
                (import_name, str(e))
            )


def format_result(result):
    """format result to show in logs"""
    if isinstance(result, string_types):
        return result[0: 30]
    elif isinstance(result, (list, tuple, dict)):
        return str(result)[0: 30]
    elif isinstance(result, Entity):
        return "{0}:{1}".format(result.__class__.__name__, result.id)
    else:
        return result


def remove_keys(data, *args, **kwargs):
    """remove keys from dictionary
    d = {'item': 1, 'other': 2, 'keep': 3}
    remove_keys(d, 'item', 'other')
    d -> {'keep': 3}
    deep = True returns a deep copy of data.
    """
    if kwargs.get('deep') is True:
        data = deepcopy(data)

    return {
        k: v for k, v in data.items() if k not in args
    }


def remove_nones(data):
    """remove nones from data"""
    return {
        k: v for k, v in data.items()
        if v is not None
    }
