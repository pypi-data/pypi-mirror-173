from typing import Type

from .errors import FormatError, ReadError
from .utils import save_dict_as_json, save_dict_as_ini, load_dict_from_json, load_dict_from_ini, get_file_extension


class ConfigModel:
    __supported_formats = {'json': [save_dict_as_json, load_dict_from_json],
                           'ini': [save_dict_as_ini, load_dict_from_ini], }

    def __str__(self) -> str:
        return str(self.as_dict())

    def __init__(self, **kwargs):
        obj_dict = self.get_dict(self.__class__)
        for k, v in obj_dict.items():
            obj_model = self.__getattribute__(k)
            if v is None:
                self.__setattr__(k, type(v)())
            else:
                if issubclass(obj_model.__class__, ConfigModel):
                    self.__setattr__(k, obj_model.from_dict(v, False))
                else:
                    self.__setattr__(k, v)
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def save(self, file_path: str):
        d = self.as_dict()
        self._save(file_path, d)

    def as_dict(self):
        class_members = self.get_dict(self.__class__)
        obj_members = self.get_dict(self)
        return {**class_members, **obj_members}

    @classmethod
    def load(cls: Type['ConfigModel'], file_path: str, strict_check: bool = False) -> 'ConfigModel':
        if file_path is None:
            raise ReadError(f"Invalid filename: {file_path}")
        file_type = get_file_extension(file_path).lower()
        if file_type not in ConfigModel.__supported_formats.keys():
            raise FormatError(f"Unsupported format")
        fn = ConfigModel.__supported_formats[file_type]
        if fn is not None:
            config_dict: dict = fn[1](file_path)
            if "default" in config_dict.keys():
                config_dict = config_dict["default"]
            obj = cls.from_dict(config_dict, strict_check)
            return obj
        else:
            raise NotImplementedError("No function added")

    @classmethod
    def from_dict(cls, d: dict, strict: bool) -> 'ConfigModel':
        obj = cls()
        for k, v in d.items():
            original_param_type = obj.__getattribute__(k).__class__
            if issubclass(original_param_type, ConfigModel):
                v = original_param_type.from_dict(v, strict)
            else:
                v = obj.__getattribute__(k).__class__(v)
            obj.__setattr__(k, v)
        return obj

    @classmethod
    def create_empty(cls, file_path: str):
        members = cls.get_dict(cls)
        cls._save(file_path, members)

    @classmethod
    def _save(cls, file_path: str, data: dict):
        file_type = get_file_extension(file_path).lower()
        if file_type not in cls.__supported_formats:
            raise FormatError(f"Unsupported format")
        else:
            fn = cls.__supported_formats[file_type]
            if fn is not None and len(fn) == 2:
                fn[0](file_path, data)
            else:
                raise NotImplementedError("No function added")

    @classmethod
    def get_dict(cls, obj):
        res = {}
        for key, value in obj.__dict__.items():
            if key.startswith('_'):
                continue
            if isinstance(value, ConfigModel):
                res[key] = value.as_dict()
            else:
                res[key] = value
        return res
