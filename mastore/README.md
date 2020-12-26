
#### Heruko Notes
Github automatic deploy in subsfolder: https://stackoverflow.com/questions/39197334/automated-heroku-deploy-from-subfolder
 
 
#### Digital Ocean

####1.
Adjust in /etc/nginx/sites-enabled/items-rest.conf
with

```
server {
listen 80;
real_ip_header X-Forwarded-For;
set_real_ip_from 127.0.0.1;
server_name localhost;


location / {
include uwsgi_params;
uwsgi_pass unix:/var/www/html/items-rest/socket.sock;
uwsgi_modifier1 30;
}

error_page 404 /404.html;
location = /404.html {
root /usr/share/nginx/html;
}

error_page 500 502 503 504 /50x.html;
location = /50x.html {
root /usr/share/nginx/html;
}
}
```
Delete /etc/nginx/sites-enabled/default.




####2.
systemd service file in  /etc/systemd/system/uwsgi_items_rest.service

```
[Unit]
Description=uWSGI items rest

[Service]
Environment=DATABASE_URL=postgres://<USER>:<Password>@localhost:5432/franzi
ExecStart=/var/www/html/items-rest/venv/bin/uwsgi --emperor /var/www/html/items-rest/uwsgi.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```


Restart all with:

sudo systemctl reload nginx

sudo systemctl restart nginx

sudo systemctl start/restart uwsgi_items_rest
  