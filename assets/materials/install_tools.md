[Вернуться][main]

---

# Установка инструментов

## kubectl

kubectl, позволяет выполнять команды для кластеров Kubernetes. С помощью kubectl можно разворачивать приложения, проверять ресурсы кластера и управлять ими, а также просматривать логи. Дополнительную информацию, включая полный список операций kubectl, можно найти в [документации](https://kubernetes.io/docs/reference/kubectl/) по kubectl.

kubectl можно установить на различные платформы [Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux), [macOS](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos) и [Windows](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows).

## kind

kind позволяет запустить Kubernetes на локальной машине. Для работы этого инструмента необходимо, чтобы были установлены Docker или Podman.

На странице [быстрого запуска](https://kind.sigs.k8s.io/docs/user/quick-start/) kind показано,
что нужно сделать, чтобы начать работу с kind.

## minikube

Как и kind, minikube - это инструмент, позволяющий запускать Kubernetes локально. minikube запускает локальный кластер Kubernetes на локальной машине, чтобы протестировать Kubernetes или для ежедневной разработки.

[Руководство](https://minikube.sigs.k8s.io/docs/start/) по установке minikube.
Основные [команды](minikube.md) minikube.

## kubeadm

Можно использовать kubeadm для создания и управления кластерами Kubernetes. Он выполняет действия, необходимые для создания минимально жизнеспособного, безопасного кластера и его запуска в удобной для пользователя форме.

В [руководстве](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) kubeadm можно почитать, как установить kubeadm.

---

[Вернуться][main]


[main]: ../../README.md "содержание"
