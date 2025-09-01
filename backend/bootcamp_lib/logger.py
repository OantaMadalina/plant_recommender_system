from __future__ import annotations


class Logger():
    _instance = None
    _logger = None

    def __new__(cls) -> Logger:
        if not cls._instance:
            import aws_lambda_powertools
            cls._instance = object.__new__(cls)
            cls._logger = aws_lambda_powertools.Logger()

        return cls._instance

    def set_correlation_id(self, correlation_id=None):
        self._logger.set_correlation_id(correlation_id)

    def structure_logs(self, append: bool = False, **kwargs):
        self._logger.structure_logs(append, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        extra = {"type": "FAIL"}
        if "extra" in kwargs:
            kwargs["extra"].update(extra)
        else:
            kwargs["extra"] = extra
        self._logger.exception(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def log(self, msg, *args, **kwargs):
        self._logger.log(msg, *args, **kwargs)
