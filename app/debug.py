"""
Run PROD (render):
docker run -d --name tge-scraper -p 8000:8000 -e RUN_ENV=prod -e LOGGING_LEVEL=info -e DB_URL=postgresql://postgres:qvRrGE9ynq3eY@pse-scraper-db/postgres --network pse-scraper-network krykiet/pse-scraper


Run remote (port 8002)
docker run -d --name tge-scraper -p 8002:8000 -e DB_URL=postgresql://postgres:HSqJrgxyq9eJD@tge-scraper-db/postgres --network tge-scraper-network krykiet/tge-scraper --remote

# SETUP
chmod +x cronjob-scrape.sh
chmod +x cronjob-debug.sh.sh

### Crontab // crontab -e
45 21 * * * /usr/src/tge-scraper/cronjob-scrape.sh
45 9 * * * /usr/src/tge-scraper/cronjob-scrape.sh
15 * * * * /usr/src/tge-scraper/cronjob-debug.sh

# Start CRONJOB
service cron start

# Give permissions
chmod +x cronjob-scrape.sh
chmod +x cronjob-debug.sh.sh

Run DB (remote):
docker run --name tge-scraper-db -e POSTGRES_PASSWORD=HSqJrgxyq9eJD -v tge-scraper-db-data:/var/lib/postgresql/data --network=tge-scraper-network -d postgres

Backup DB
In OVH server: pg version mismatch
# Step 1: Run pg_dump inside the Docker container to create a backup
docker exec -t tge-scraper-db pg_dump -U postgres -F c -b -v -f /var/lib/postgresql/data/backup.dump your_database_name

# Step 2: Copy the backup file from the Docker container to your local machine
docker cp tge-scraper-db:/var/lib/postgresql/data/backup.dump ./backup.dump

# Copy backup file to container
docker cp ./backup.dump tge-scraper-db:/var/lib/postgresql/data/backup.dump

# Create new database
docker exec -t tge-scraper-db psql -U postgres -c 'CREATE DATABASE debug_db;'

#
docker exec -t tge-scraper-db pg_restore -U postgres -d debug_db -v /var/lib/postgresql/data/backup.dump



####

Run local:
docker run --name tge-scraper-test -p 8000:8000 krykiet/tge-scraper --local





Requests:
curl -X 'GET' http://172.20.0.1:8002/tge-rdn/tge-rdn
curl -X 'POST' http://0.0.0.0:8000/tge-rdn/tge-rdn -H 'accept: application/json' -d ''
curl -X 'GET' http://172.20.0.1:8002/tge-rdn/tge-rdn/
"""