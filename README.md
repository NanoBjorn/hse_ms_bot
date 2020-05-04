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
   
2. Run postgres locally:
    ```bash
    docker-compose run -p 5432:5432 postgres 
    ```
3. Run ngrok locally to publish 8000 port with https
   ```bash
   ngrok http 8000
   ```

4. Run server in debug mode
    ```bash
    HSE_BOT_DEBUG=local-ngrok \
    MS_CLIENT_ID=<client id> \
    MS_CLIENT_SECRET=<client secret> \
    TG_BOT_TOKEN=<telegram bot token> \
    HSE_BOT_PG_HOST=localhost \
    python src/main.py
    ```
   
   Server will run on https://0.0.0.0:8000

### In docker

*Generally for deployment*

1. Fill .env file
    ```bash
    cp .env.sample .env
    ```
   and fill it manually
   
2. `docker-compose build`
3. `docker-compose up backend webserver postgres`

   This will run server in `backend` service and `nginx` on 80 port with proxying to `backend`. 
