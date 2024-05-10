import logging
import logging as log

log.basicConfig(
    level=log.DEBUG,
    format='%(asctime)s %(levelname)s [%(filename)s: %(lineno)s] %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p',
    handlers=[
        logging.FileHandler('data_layer_logs.log'),
        logging.StreamHandler()
    ]
)