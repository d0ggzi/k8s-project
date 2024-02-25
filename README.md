# TODO App using k8s

---

## Подготовка    

Первым делом я установил `kubectl` и `minikube`. Запустил командой    

```shell
minikube start  
```   

нуу и все, мы готовы начинать!

## Начало

Я решил использовать свой проект с прошлой домашки, так как в нем как раз было 3 сервиса
- PostgreSQL   
- Backend  
- Frontend  

Начал я с БД. Честно скажу, откуда-то стырил `yaml` файл для запуска и вписал свои данные. Но в целом базовое понимание про `pv`, `pvc` и `configmap`'ы у меня появилось. 

Дальше - интереснее: во-первых, надо было собрать dockerfile бэка и фронта и залить на docker-hub. Затем я по инструкции с официальной доки написал `yaml`'ики для backend-deployment и backend-service, запустил их командой

```shell
kubectl apply -f <your-file>.yaml  
``` 

Проделал то же самое для frontend-deployment и frontend-service. Сначала я обрадовался, потому что все вроде как запустилось нормально, но я никак не мог наладить общение между бэком и фронтом. Вот на этом моменте я просидел около 4 часов...     

Оказалось, что я неправильно запускал сервер и думал, что фронтенд увидит бэкенд по внутреннему имени. Вот как было:

```shell
python -m http.server 8081
```

И хотя `curl`, запущенный с фронта, работал, с браузера было никак не достучаться до бэка.

![image_2024-02-23_18-37-14](https://github.com/d0ggzi/todo-project/assets/43131496/57e3d7c0-aa1f-47ab-9395-2ab7e6ca3e2a)

На нашем любимом сайте нашел ту же самую [проблему](https://stackoverflow.com/questions/70307437/kubernetes-frontend-pod-cant-reach-backend-pod) и все встало на свои места. Оказывается сам браузер не воспринимает url, по которому происходит запрос к бэку. Тогда я решил использовать nginx (a.k. reverse proxy). Он поднимает свой веб-сервер и перенаправляет запросы к бэку. После часа развлечений с ранее незнакомой мне технологией, у меня получилось!

## Основная часть

И так, поднимаем все `deployments` и `services` из директории **k8s**. Прописываем в комадной строке
```shell
minikube ip
```
для получения ip, по которому будем ходить. Но ведь нам нужен еще порт! Поэтому пишем
```shell
kubectl get svc
```
Находим сервис frontend. У него прописан тип `LoadBalancer`, а значит мы сможем законнектиться к нему по проброшенному порту. В моем случае это `32701`
![image](https://github.com/d0ggzi/todo-project/assets/43131496/a1fb4a5f-e2e2-4900-9a8f-8eab22110e94)

Готово! Переходим по полученному адресу в браузере `192.168.49.2:32701` и видим наш сайт!

Зарегистрируемся под пользователем **test**

![image](https://github.com/d0ggzi/todo-project/assets/43131496/bdb48d86-abc0-410d-8556-0e750e2dbbfa)

И создадим пару задачек - удостоверимся, что все работает

![image](https://github.com/d0ggzi/todo-project/assets/43131496/04af36e6-f368-47fd-a9ec-50e996b31505)

Все работает отлично, но... О нет! Мы нашли ошибку в `Dockerfile backend`'a. Оказалось, что мы используем версию 3.10, когда в `pyproject.toml` указано 3.11^ (допустим). Присвоим метку v1 существующему поду

```shell
kubectl get pods -l tier=backend
kubectl label pods "backend-699d7ccb4d-dtbw8" version=v1
kubectl describe pods "backend-699d7ccb4d-dtbw8" 
```

![image](https://github.com/d0ggzi/todo-project/assets/43131496/889f30d6-3f4b-4502-903e-1c5e8182ae24)

А также создадим реплики нашего приложения перед тем, как заливать новую версию
```shell
kubectl scale deployments/backend --replicas=3
```
Второй вариант - прописать в `backend-deployment` параметр `replicas: <your-replicas-number>`. Так сделал я. Кстати k8s распределяет нагрузку между репликами, в чем я лично удостоверился, посмотрев логи разных реплик

![image_2024-02-25_13-18-00](https://github.com/d0ggzi/todo-project/assets/43131496/ecd717eb-4f1b-4f93-933c-ce0a3650393a)

В это время фиксим ошибку и заливаем новую версию на dockerhub с label v2. Теперь мы готовы обновляться
```shell
kubectl set image deployments/backend todo=dggz1/todo-backend:v2
```

Фух, все прошло успешно!

## Концовочка

Почистим за собой

```shell
kubectl delete deployments postgres frontend backend
kubectl delete svc postgres frontend todo
```

А еще можно почистить 
```shell
kubectl delete pv --all 
kubectl delete pvc --all 
```

И в конце концов
```shell
minikube stop
```

