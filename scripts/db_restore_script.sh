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
    
else
    echo "Файл $ENV_FILE не найден"
fi

DB_HOST=$DB_HOST  
DB_PORT=$DB_PORT
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
echo $DB_USER

timestamp=$(date +"%d-%m-%Y")
fileName="db_backup_$timestamp"

CONTAINER_NAME=$(docker ps --filter "name=db" --format "{{.Names}}" | grep -E ".*db" | head -n1)

if [ -z "$CONTAINER_NAME" ]; then
    echo "❌ Контейнер с PostgreSQL не найден. Запустите: docker-compose up -d db"
    exit 1
fi

echo "✅ Найден контейнер: $CONTAINER_NAME"
echo "📊 Подключение к БД: $DB_NAME пользователь: $DB_USER"

docker exec -t $CONTAINER_NAME dropdb --force -U $DB_USER $DB_NAME

# docker exec -t -u "$DB_USER" "$CONTAINER_NAME" dropdb --if-exists "$DB_NAME"

# docker exec -t -u "$DB_USER" "$CONTAINER_NAME" createdb "$DB_NAME"
docker exec -t $CONTAINER_NAME createdb -U $DB_USER $DB_NAME

# docker exec -i -u "$DB_USER" "$CONTAINER_NAME" psql "$DB_NAME" < "$fileName.sql"
docker exec -i $CONTAINER_NAME psql -U $DB_USER "$DB_NAME" < "./backups/$fileName.sql"
echo "Done"