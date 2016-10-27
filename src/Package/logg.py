import logging
import logging.config

class Log:
    logger=0

    @classmethod
    def init(cls):
        logging.config.fileConfig("logger.conf")
        cls.logger = logging.getLogger("example01")

    @classmethod
    def getLogger(cls):
        return cls.logger


