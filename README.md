# billmate

### Easy way to track your split bill

## Tailwind
- npm init
- npm install -D tailwindcss
- npx tailwindcss init
- npx tailwindcss -i ./src/input.css -o ./src/output.css --watch

## Daisy UI
- npm i -D daisyui@latest

## assets build
- npm run tw-watch

## migration
- pdm run manage.py makemigrations base --empty
- pdm run manage.py migrate base zero (zero)
- pdm run manage.py migrate base <migration_name> (1 step migration)

## Debug port
- sudo lsof -i -P -n | grep <port number>
- sudo lsof -i :80
- sudo systemctl stop apache2

## NPM Dependencies Prod
- npm install --production
- wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash (install node js package manager)
- source ~/.bashrc
- nvm install 20.11.1
- nvm use 20.11.1
- npx tailwindcss -i ./src/base/static/base/style.css -o ./src/base/static/base/output.css --minify (Production Mode)
- Manual Handling (Move the output.css to static)

## Debug Postgres
- psql -U postgres -d postgres

## Load Testing
- npx autocannon https://django-2.mashanz.com/accounts/login/?next=/ -p 100 -c 100 -d 10


## Debug Nginx:
- adding for check the web running
```
ports:
    - 8000:8000
```