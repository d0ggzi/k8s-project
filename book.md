[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/yz4E8r7s)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=13982609&assignment_repo_type=AssignmentRepo)
# Kubernetes

![][img]

Поговорим об основах системы оркестрации кластеров Kubernetes.
Каждый блок семинара содержит справочную информацию об основных возможностях и концепциях Kubernetes.

Научимся:

- Разворачивать контейнерное приложение на кластере.
- Масштабировать развёртывание.
- Обновлять контейнерное приложение новой версией программного обеспечения.
- Отлаживать контейнерное приложение.

## Чем может быть полезен Kubernetes?

В современных веб-сервисах пользователи ожидают, что приложения будут доступны 24 часа в сутки 7 дней в неделю,
а разработчики - что новые версии этих приложений будут разворачиваться несколько раз в день.
Контейнеризация помогает упаковывать программное обеспечение для достижения этих целей,
позволяя выпускать и обновлять приложения без простоев.
Kubernetes помогает убедиться, что приложения в контейнерах запускаются там и тогда, где и когда вы хотите,
и помогает им найти ресурсы и инструменты, необходимые для работы.
Kubernetes - это готовая к производству платформа с открытым исходным кодом,
созданная на основе накопленного опыта Google в области оркестрации контейнеров в сочетании с лучшими идеями сообщества.

## Содержание семинара

### I. [Установка инструментов](assets/materials/install_tools.md)
### II. [Создание кластера Kubernetes](assets/materials/create_k8s_cluster.md)
### III. [Основные команды minikube](assets/materials/minikube.md)
### IIII. [Развёртывание приложения](assets/materials/deploy.md)
### V. [Исследование приложения](assets/materials/view_pods_nodes.md)
### VI. [Expose (публикация) приложения](assets/materials/expose_app.md)
### VII. [Масштабирование приложения](assets/materials/scale_app.md)
### VIII. [Обновление приложения](assets/materials/update_app.md)

## Практика

[ДЗ][homework]

---

[img]: assets/img/img.png

[homework]: assets/materials/homework.md "homework"
