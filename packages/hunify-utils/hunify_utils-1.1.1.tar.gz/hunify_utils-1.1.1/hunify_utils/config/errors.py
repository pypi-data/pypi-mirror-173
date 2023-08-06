class ConfigError(Exception):
    pass


class FormatError(ConfigError):
    pass


class WriteError(ConfigError):
    pass


class ReadError(ConfigError):
    pass


class ParseError(ConfigError):
    pass
