# spbstu-amml

Пакет для хранения данных и моделей и быстрого их использования

В качестве хранилища используется S3 storage, для достступа и версионирования данных используется репозиторий [spbstu-datahub](https://github.com/Nika-Keks/spbstu-datahub.git)

---
## Модуль spbstuamml

Для загрузки одной из поддерживаемых моделей необходимо установить пакет `spbstu-amml`

```console
$ pip install spbstu-amml 
```

Пример получения модели:

```python
from spbstuamml.models import vgg
model = vgg.vgg16_from_hub(dataset="pneumonia")
model.summary()
```
```console
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 vgg16 (Functional)          (None, 7, 7, 512)         14714688  
...
```

Модель будет загружена один раз и использована в дальнейшем.

Внимание! 
Пакет не тянет за собой библиотеки для машинного обучения, их пользователь должен установить сам.

---
## datahub

Утилита для настройки доступа к удаленному хранилищу

```console
$ python3 -m datahub -h

Datahub utils to manage the data repository configuration

positional arguments:
  {configure}  utils command

options:
  -h, --help   show this help message and exit
```

Для ввода ключей доступа и региона необходимо выполнить команду `configure` и ввести параметры:

```console
$ python3 -m datahub configure
Enter Access Key ID:access-key-id
Enter Secret Access key:secret-access-key
Enter Region:default
```

или ввести параметры в качестве аргументов команды:

```console
$ python3 -m datahub configure \
> --access-key-id "access-key-id" \
> --secret-access-key "secret-access-key" \
> --region "default"
```

все агрументы описаны в help

```console
$ python3 -m datahub configure -h

Configuration commad

options:
  -h, --help            show this help message and exit
  --access-key-id ACCESS_KEY_ID
                        aws access key
  --secret-access-key SECRET_ACCESS_KEY
                        aws secret key
  --region REGION       region. may be depault, central1 or other, see aws documentation
```