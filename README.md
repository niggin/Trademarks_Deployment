Trademarks_Deployment
=====================

Apache deployment


Work-in-progress версия будущего проекта <Trademarks_name>

Что необходимо для запуска:
1. Python 2.7
На 3.3 не хотел запускаться драйвер mysql, поэтому ставить обязательно именно 2.7:
https://www.python.org/download/releases/2.7.6
Лично у меня стояла Anaconda, в ней понапихано много полезных пакетов:
http://continuum.io/downloads
2. Django v1.6 или выше
С самого начала все писалось на ней. Ставить версию ниже не вижу никакого смысла, на 1.7 не пробовал, но вряд ли что-то должно упасть.
https://www.djangoproject.com/download/
или
pip install Django==1.6.2
3. MySQL
Используемая СУБД. 
http://dev.mysql.com/downloads/
4. MySQL Connector
Связующее звено между Django и MySQL.
https://dev.mysql.com/downloads/connector/python/1.1.html

Первый запуск:
0. Установите все необходимые пакеты и скачайте содержимое репозитория
1. Создайте в localhost базе mysql схему trademarks
2. Перейдите в командной строке/терминале в папку с содержимым репозитория и выполните команду python manage.py syncdb
3. Вас попросят создать пользователя для доступа к внутренним ресурсам, в теории это можно пропустить
4. После выполните команду python manage.py runserver 80
5. Перейдите в адресной строке браузера по адресу http://localhost или http://127.0.0.1
Если сайт загрузился, значит в этом туториале нет ошибок.

Формат базы данных:
Во-первых, никаких запятых в содержимом полей, особенно в поле перевода. НИКАКИХ. Во-вторых, поля должны разделяться одним и тем же символом. Используйте тот, который не встречается во всем файле. Логично в качестве символа взять запятую :). В-третьих, никакой посторонней информации, только слово, транскрипция и его перевод. Желательно так же поле с языом слова, но в целом не обязательно. Порядок полей в строке тоже не сильно важен. В итоге в идеальном файле все должно быть примерно так:
<word>,<transcription>,<translation>,<lang>\n
Сам файл должен быть в кодировке Unicode или UTF-8.
