# Habit_Tracker_Project

Проект для отслеживания привычек с отправкой напоминаний через Telegram.

## Базовый URL

- Локально: `http://127.0.0.1:8000/api/`
- Продакшн: `<указать актуальный домен>/api/`

> Все эндпоинты начинаются с `/api/`.


---


## Где смотреть интерактивную документацию

- **Swagger UI**: `/docs/`
- **Redoc**: `/redoc/`

В этих интерфейсах есть:
- список всех эндпоинтов;
- описание параметров запроса;
- примеры тел запросов и ответов;
- кнопка «Try it out» для тестирования прямо из браузера.

---

## Аутентификация

API использует JWT-аутентификацию.

**Как передавать токен:**

http
Authorization: Bearer <access_token>

## Локальный запуск через Docker Compose

### Предварительные требования

- Установленный Docker
- Установленный Docker Compose

### Шаги запуска

1. Создайте файл `.env` на основе шаблона:

```bash
cp .env.template .env
```

2. Заполните `.env` своими значениями:



3. Запустите все сервисы одной командой:

```bash
docker compose up -d --build
```

5. Проверьте статус контейнеров:

```bash
docker compose ps
```

Должны работать 6 контейнеров: `db`, `redis`, `web`, `celery`, `celery_beat`, `nginx`.

6. Создайте суперпользователя :

```bash
docker compose exec web python manage.py createsuperuser
```

7. Проверьте работу:

- API: `http://localhost/api/`
- Swagger: `http://localhost/swagger/`
- Redoc: `http://localhost/redoc/`
- Админка: `http://localhost/admin/`

### Остановка сервисов

```bash
docker compose down
```

### Полная остановка с удалением данных

```bash
docker compose down -v
```

---

## Настройка CI/CD через GitHub Actions

### Требуемые секреты в GitHub

Перейдите в репозиторий → Settings → Secrets and variables → Actions и добавьте:

| Секрет | Описание |
|--------|----------|
| `DOCKER_HUB_USERNAME` | Логин в Docker Hub |
| `DOCKER_HUB_ACCESS_TOKEN` | Access Token с правами Read & Write |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ для доступа к серверу |
| `SERVER_USER` | Имя пользователя на сервере (например, `test`) |
| `SERVER_HOST` | IP-адрес сервера (например, `158.160.17.35`) |
| `DEPLOY_DIR` | Путь к проекту на сервере (например, `/home/test/Habit_Tracker_Project`) |



## Настройка удалённого сервера

### 1. Создание виртуальной машины в Yandex Cloud

1. Зарегистрируйтесь в Yandex Cloud.
2. Создайте виртуальную машину:
   - ОС: Ubuntu 22.04 LTS
   - Минимальные ресурсы: 2 vCPU, 2 ГБ RAM
   - Назначьте публичный IP-адрес
3. Запомните IP-адрес и логин пользователя.


### 2. Подключение к серверу

```bash
ssh test@<IP-сервера>
```

### 3. Установка Docker и Docker Compose

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
```

Проверьте установку:

```bash
docker --version
docker compose version
```

### 4. Клонирование репозитория на сервер

```bash
cd ~
git clone https://github.com/Mikhail-Z-P/Habit_Tracker_Project.git
cd Habit_Tracker_Project
```

### 5. Настройка `.env` на сервере

```bash
cp .env.template .env
```

Заполните `.env`:
- `ALLOWED_HOSTS` — добавьте IP-адрес сервера (например, `localhost,127.0.0.1,158.160.17.35`)
- `DEBUG=False`
- `DB_PASSWORD` — задайте надёжный пароль
- `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID` — ваши значения

### 6. Настройка SSH-доступа для GitHub Actions

На локальной машине сгенерируйте SSH-ключ:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key
```

Два файла появятся:
- `~/.ssh/deploy_key` — приватный ключ
- `~/.ssh/deploy_key.pub` — публичный ключ

**Публичный ключ** добавьте на сервер:

```bash
cat ~/.ssh/deploy_key.pub | ssh test@<IP-сервера> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**Приватный ключ** добавьте в GitHub Secrets как `SSH_PRIVATE_KEY`:

```bash
cat ~/.ssh/deploy_key
```

Скопируйте вывод целиком (от `-----BEGIN` до `-----END`) и вставьте в GitHub: Settings → Secrets and variables → Actions → New repository secret.


---




