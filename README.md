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
6. ```bash
    docker-compose up --build --detach
    ```
