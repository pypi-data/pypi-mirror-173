from pymedquery.config.logger_object import Logger

log = Logger(__name__)

class NoRecordsFound(Exception):
    log.error('No records were found')


class CommitBounced(Exception):
    log.error('Aiai, your commit did not go through')
