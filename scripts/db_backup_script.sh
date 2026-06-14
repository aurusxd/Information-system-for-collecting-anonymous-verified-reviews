#!/bin/bash
cd ..
ENV_FILE=".env"
if [ -f "$ENV_FILE" ]; then
    echo "Чтение файла $ENV_FILE"
    while IFS= read -r line; do
        if [[ "$line" =~ ^\s*#.*$ || -z "$line" ]]; then
            continue
        fi
        key=$(echo "$line" | cut -d '=' -f 1)
        value=$(echo "$line" | cut -d '=' -f 2-)
        value=$(echo "$value" | sed -e "s/^'//" -e "s/'$//" -e 's/^"//' -e 's/"$//' -e 's/^[ \t]*//' -e 's/[ \t]*$//')
        export "$key=$value"
    done < "$ENV_FILE"
    echo "Чтение файла $ENV_FILE завершено"
    if test -d "./backups"; then
        echo "Папка существует"
        cd backups
    else 
        echo "Папки не существует, создаю"
        mkdir backups
        cd backups
    fi
    
else
    echo "Файл $ENV_FILE не найден"
fi



DB_HOST=$DB_HOST  
DB_PORT=$DB_PORT
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD

CONTAINER_NAME=$(docker ps --filter "name=db" --format "{{.Names}}" | grep -E ".*db" | head -n1)

if [ -z "$CONTAINER_NAME" ]; then
    echo "Контейнер с PostgreSQL не найден."
    exit 1
fi

echo "Найден контейнер: $CONTAINER_NAME"
echo "Подключение к БД: $DB_NAME пользователь: $DB_USER"

timestamp=$(date +"%d-%m-%Y")
fileName="db_backup_$timestamp"
docker exec -t $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME > "$fileName.sql"
# pg_dump -U postgres "$DB_NAME" > "$fileName.sql"
echo "dump created"