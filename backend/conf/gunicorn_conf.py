# pythonpath = '/home/campaign/backend'
bind = '0.0.0.0:8000'
workers = 5
timeout = 120
certfile = '/home/campaign/cert.crt'
keyfile = '/home/campaign/private.key'
# Access log - records incoming HTTP requests
#accesslog = "/var/log/gunicorn/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
#errorlog = "/var/log/gunicorn/gunicorn.error.log"
# Whether to send Django output to the error log
#capture_output = True
# How verbose the Gunicorn error logs should be
# loglevel = "info"