# SWGoH - Помощник по гильдии

## Сайт

* Импорт складов игроков с swgoh.gg
* Ведение нескольких гильдий одновременно
* Просмотр прогресса прокачки
* Отчет о готовности отрядов задаваемых администратором


# Установка

Требуется Python3, PostgreSQL, nginx, uwsgi

```bash
# Ставим гит, питон и postgres
sudo apt-get install git python3 python3-venv postgresql postgresql-contrib nginx

# Подтягиваем код
git clone https://github.com/dmitryU/swgoh-manager.git
cd swgoh-manager

# Создаём виртуальное окружение и ставим зависимости
python3.6 -m venv venv
source ./venv/bin/activate
# На данный момент есть проблема установки телеграм бота, так как отсутсвтует репозитрий django-telegrambot
pip install -r requerements.txt
```

Создать конфиг uwsgi для запуска stand-alone - файл /etc/uwsgi/swgoh.ini:
```
[uwsgi]
chdir = /path/to/swgoh-manager/
venv = DJANGO_SETTINGS_MODULE=swgoh.settings
virtualenv = /path/to/swgoh-manager/venv/
plugins = python
module = swgoh.wsgi
master = true
processes = 5
socket = /path/to/swgoh-manager/swgoh.socket
chmod-socket = 664
;daemonize = /path/to/swgoh-manager/uwsgi-swgoh.log
uid = www-data
gid = www-data
```

В конфиге nginx следует прописать доступ к проекту через uwsgi:
```
# the upstream component nginx needs to connect to
upstream django {
    server unix:///path/to/swgoh-manager/swgoh.socket;
}
server {
    listen 80;
    server_name swgoh.example.com;

    access_log /var/log/nginx/access-swgoh.log;
    error_log  /var/log/nginx/error-swgoh.log;

    # max upload size
    client_max_body_size 75M;

    # Django media
    location /media  {
        alias /path/to/swgoh-manager/media;
    }

    location /static {
        alias /path/to/swgoh-manager/static;
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     uwsgi_params;
    }
}
```

Добавить автозапуск uwsgi, например через systemd:
```bash
systemctl enable uwsgi@swgoh
systemctl start uwsgi@swgoh
```

# Автообновление складов с swgoh.gg

Для обновления данных по игрокам, гильдиям предусмотрена команда update_guilds (требуется использовать venv, см. установку):
```bash
./manage.py update_guilds
```

Чтобы обновление выполнялось автоматически по расписанию, можно использовать systemd.
Создать службу обновления, файл /etc/systemd/system/update_guilds.service:
```
[Unit]
Description=Обновление активных гильдий из SWGOH.GG

[Service]
WorkingDirectory=/path/to/swgoh-manager/
ExecStart=/path/to/swgoh-manager/venv/bin/python /path/to/swgoh-manager/manage.py update_guilds
User=www-data
Group=www-data
Restart=no
```

Далее создать таймер обновления в файле /etc/systemd/system/update_guilds.timer:
```
[Unit]
Description=Ежедневное обновление гильдий из SWGOH.GG

[Timer]
OnCalendar=*-*-* 1:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

И, наконец, разрешить выполнение службы обновления:
```bash
systemctl enable update_guilds.timer
systemctl start update_guilds.timer
```

Обновление будет происходить каждый день в час ночи.
