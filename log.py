


import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s][%(filename)s%(process)d]:*<%(message)s>*"
    )
fh.setFormatter(fh_formatter)
logger.addHandler(fh)