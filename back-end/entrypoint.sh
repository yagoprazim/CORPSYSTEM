#!/bin/bash
set -e

# Função para verificar se o MySQL está disponível
function wait_for_mysql() {
  echo "Waiting for MySQL..."
  while ! python -c "import MySQLdb; MySQLdb.connect(host='mysql-db', user='root', passwd='root', db='corpsystem')" >/dev/null 2>&1; do
    echo "Waiting for MySQL connection..."
    sleep 1
  done
  echo "MySQL is up - executing command"
}

# Executa a função de espera
wait_for_mysql

# Executa as migrações
python manage.py migrate --noinput

# Cria o superusuário se ele não existir
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')" | python manage.py shell

# Executa o comando especificado no CMD do Dockerfile
exec "$@"
