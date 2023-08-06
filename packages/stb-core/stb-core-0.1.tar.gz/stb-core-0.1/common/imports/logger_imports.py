import logging

payment_logger = logging.getLogger('payment_logger')
payment_error_logger = logging.getLogger('payment_error_logger')
auth_log = logging.getLogger('auth_log')
auth_error_log = logging.getLogger('auth_error_log')
shop_logs = logging.getLogger('shop_logs')
shop_error_logs = logging.getLogger('shop_error_logs')
product_logs = logging.getLogger('product_logs')
product_error_logs = logging.getLogger('product_error_logs')
django = logging.getLogger('django')