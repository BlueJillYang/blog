import json
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import multiprocessing
import os

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("MAX_WORKERS")
use_max_workers = None
if max_workers_str:
    use_max_workers = int(max_workers_str)
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)

local_host = "172.17.0.1"  # "10.128.0.2"  # "172.17.0.1" # "127.0.0.1"  # "0.0.0.0"
host = os.getenv("HOST", local_host)
port = os.getenv("PORT", "8001")
bind_env = f"{host}:{port}"  # os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if use_max_workers:
        web_concurrency = min(web_concurrency, use_max_workers)
accesslog_var = os.getenv("ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
errorlog_var = os.getenv("ERROR_LOG", "-")
use_errorlog = errorlog_var or None
graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")

# Gunicorn config variables
loglevel = use_loglevel
workers = 2  # web_concurrency
bind = use_bind
worker_tmp_dir = "/home/tax/dev"
if not os.path.exists(worker_tmp_dir):
    os.makedirs(worker_tmp_dir)
accesslog = "/home/tax/dev/access.log"  # use_accesslog
errorlog = "/home/tax/dev/error.log"  # use_errorlog
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'


# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": errorlog,
    "accesslog": accesslog,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "use_max_workers": use_max_workers,
    "host": host,
    "port": port,
}

# acclog = logging.getLogger('gunicorn.access')
# acclog.addHandler(WatchedFileHandler('/home/test/server/log/gunicorn_access.log'))
# acclog.propagate = False
# errlog = logging.getLogger('gunicorn.error')
# errlog.addHandler(WatchedFileHandler('/home/test/server/log/gunicorn_error.log'))
# errlog.propagate = False


