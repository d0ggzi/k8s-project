[Вернуться][main]

---

# Основные команды minikube

minikube - это локальный Kubernetes, сфокусированный на том, чтобы облегчить обучение и разработку для Kubernetes.

Все, что нужно - это Docker (или аналог) или среда виртуальной машины, а Kubernetes - это всего лишь одна команда: `minikube start`.

Минимальные требования по железу:

- 2 процессора или более
- 2 ГБ свободной памяти
- 20 ГБ свободного дискового пространства
- Интернет-соединение
- Менеджер контейнеров или виртуальных машин, например: Docker, QEMU, Hyperkit, Hyper-V, KVM, Parallels, Podman, VirtualBox или VMware Fusion/Workstation

## Установка

Например для Linux на архитектуре x86-64:

```sh
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

## Запуск кластера

Из терминала с правами администратора (но не как root):

```sh
minikube start
```

## Взаимодействие с кластером

Если установлен kubectl, можно использовать его для доступа к кластеру:

```sh
kubectl get po -A
```

В качестве альтернативы, minikube может загрузить соответствующую версию kubectl,
и можно будет использовать его следующим образом:

```sh
minikube kubectl -- get po -A
```

После чего можно облегчить себе жизнь, добавив алиас в конфиг:

```sh
alias kubectl="minikube kubectl --"
```

Первоначально некоторые сервисы, такие как storage-provisioner, могут не находиться в состоянии Running.
Это нормальное состояние при запуске кластера, и оно скоро разрешится.
Чтобы получить дополнительную информацию о состоянии кластера, minikube включает в себя панель Kubernetes Dashboard,
позволяющую легко освоиться в новой среде:

```sh
minikube dashboard
```

После запуска откроется страница в браузере с адресом: http://127.0.0.1:55447/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/workloads?namespace=default

## Управление кластером

Приостановка работы Kubernetes без ущерба для развёрнутых приложений:

```sh
minikube pause
```

Снять с паузы приостановленный инстанс:

```sh
minikube unpause
```

Остановить кластер:

```sh
minikube stop
```

Изменение установленного по умолчанию лимита памяти (требует перезапуска):

```sh
minikube config set memory 9001
```

Просмотр каталога легко устанавливаемых сервисов Kubernetes:

```sh
minikube addons list
```

Создание второго кластера под управлением более старой версии Kubernetes:

```sh
minikube start -p aged --kubernetes-version=v1.16.1
```

Удаление всех кластеров minikube:

```sh
minikube delete --all
```

---

[Вернуться][main]


[main]: ../../README.md "содержание"
