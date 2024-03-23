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
- sudo systemctl stop apache2 (default ubuntu)

## allowed file
- chmod +x