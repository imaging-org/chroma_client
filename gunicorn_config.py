import os


port = os.getenv("CONTAINER_PORT", "5646")
bind = f'0.0.0.0:{port}'
backlog = 2048

workers = 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

spew = False

daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
