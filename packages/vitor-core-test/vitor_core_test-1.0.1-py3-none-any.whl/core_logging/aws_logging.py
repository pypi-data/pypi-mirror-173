import logging

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

# Level  Numeric value
# CRITICAL  50
# ERROR  40
# WARNING  30
# INFO 20
# DEBUG 10
# NOTSET 0


def log_message(self, message):
    LogMessage = f"requestId: {self.requestId} environment: {self.environment} apiId: {self.apiId} path: {self.path}, {message}"
    return LogMessage

class Logger:
    def __init__(self, level, name, event):
        self.level = level
        self.name = name
        self.requestId = ''
        self.environment = ''
        self.apiId = ''
        self.path = ''
        if 'requestContext' in event:
            if 'requestId' in event['requestContext']:
                self.requestId = event['requestContext']['requestId']
            if 'stage' in event['requestContext']:
                self.environment = event['requestContext']['stage']
            if 'apiId' in event['requestContext']:
                self.apiId = event['requestContext']['apiId']
            if 'path' in event['requestContext']:
                self.path = event['requestContext']['path']
        logFormat = f"%(asctime)s %(levelname)s: %(name)s: %(message)s"
        logging.basicConfig(format=logFormat, level=level)
        self.logger = logging.getLogger(name)
    def info(self, message):
        self.logger.info(log_message(self, message))
    def debug(self, message):
        self.logger.debug(log_message(self, message))
    def warning(self, message):
        self.logger.warning(log_message(self, message))
    def error(self, message):
        self.logger.error(log_message(self, message))
    def critical(self, message):
        self.logger.critical(log_message(self, message))
