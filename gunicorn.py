command = "/home/www/env/bin/gunicorn"
pythonpath = "/home/www/site/myvmeste_info"
bind = "127.0.0.1:8001"
workers = 3
user = "www"
limit_request_fields = 32000
limit_request_field_size = 0
rav_env = "DJANGO_STTINGS_MODULE=myvmeste.settings"
