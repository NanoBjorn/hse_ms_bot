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

2. Run server in debug mode
    ```bash
    HSE_BOT_DEBUG=1 \
    MS_CLIENT_ID=<client_id> \
    MS_CLIENT_SECRET=<client_secret> \
    python src/main.py
    ```
   
   Server will run on https://0.0.0.0:8000 with adhoc certificate

### In docker

*Generally for deployment*

1. Fill .env file
    ```bash
    cp .env.sample .env
    ```
   and fill it manually
   
2. `docker-compose build`
3. `docker-compose up`

   This will run server in `backend` service and `nginx` on 80 port with proxying to `backend`. 
