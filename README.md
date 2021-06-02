# HSE Microsoft Auth Bot

### Development

1. Setup environment
    ```bash
    git clone git@github.com:NanoBjorn/hse_ms_bot.git
    cd hse_ms_bot
    
    # python3 -m pip install virtualenv
    python3 -m virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
2. Install [docker](https://www.docker.com/get-started)
3. Run postgres locally:
    ```bash
    docker-compose run -p 5432:5432 postgres 
    ```
4. Install [ngrok](https://ngrok.com/download)    
4. Run ngrok locally to publish 8000 port with https
   ```bash
   ngrok http 8000
   ```
5. Fill .env file
    ```bash
    cp .env.sample .env
    ```
   and fill it manually
6. Run main.py in src/server, main_worker.py in src/worker and main_ms.py in src/ms 
   
   Server will run on https://0.0.0.0:8000

### Deployment
1. ```bash
    git clone git@github.com:NanoBjorn/hse_ms_bot.git
    cd hse_ms_bot/
    ```
    
2. Fill .env file
    ```bash
    cp .env.sample .env
    ```
   and fill it manually
   
3. Install [nginx](https://nginx.org/en/download.html)

4. Setup nginx with ./docker/nginx.conf file

5. Install [docker](https://www.docker.com/get-started)

6. Run docker-compose
    ```bash
    docker-compose up --build --detach
    ```

### Adding bot to your chat

1. Find **@hsechatauthbot** bot in Telegram
2. Add **@hsechatauthbot** to your chat
3. Make **@hsechatauthbot** an administrator

### Available commands for administrators

1. `/ignore` - command to add a user to whitelist. Can be used as reply a to a Telegram "new chat member" message or just with the username:
```
/ignore @username
/ignore username
```
2. `/ban` - command to ban a user. Banned user is deleted from all chats that are administered by bot. Can be used as a reply to a message of a banning user or just with the username:
```
/ban @username
/ban username
```