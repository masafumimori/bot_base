# Crypto Trading Bot Template

This project provides a base template for developing a cryptocurrency trading bot using Python. It utilizes the [CCXT library](https://github.com/ccxt/ccxt) for interacting with cryptocurrency exchanges, [Loguru](https://github.com/Delgan/loguru) for logging, and supports sending notifications through various notifiers like Gmail, Discord, and LINE. The project is set up to run in a Docker container.

## Project Structure

The project consists of the following files:

- `logger.py`: A custom Logger class that uses the Loguru library for logging and supports sending notifications through various notifiers.
- `notifier.py`: A collection of notifier classes for sending notifications via Gmail, Discord, and LINE.
- `exchange_base.py`: Provides a base abstraction for interacting with an exchange through the CCXT library.
- `Dockerfile`: Docker configuration file for setting up the Python environment and installing dependencies.
- `requirements.txt`: A list of Python packages required for the project.
- `docker-compose.yml`: Docker Compose configuration file for running the project in a container.
- `start.sh`: A shell script to build and run the Docker container.

## Usage

1. Install Docker and Docker Compose on your machine, if you haven't already.

2. Clone the project repository:

```bash
git clone https://github.com/masafumimori/bot_base
```

or Press Use this template button at the top right on this page.

3. Set up the necessary environment variables in a `.env` file in the project root directory:

```txt
GMAIL_USERNAME=<your_gmail_username>
GMAIL_PASSWORD=<your_app_password>
NOFITY_TO=<email_address_to_receive_notifications>
DISCORD_WEBHOOK_URL=<your_discord_webhook_url> # if you want to notify to Discord
LINE_NOTIFY_TOKEN=<your_line_notify_token> # if you want to notify to LINE
API_KEY=<your_exchange_api_key>
API_SECRET=<your_exchange_api_secret>
```

4. Build and run the Docker container using the `start.sh` script:

```bash
chmod +x start.sh
./start.sh
# start.sh` builds and runs Docker container and then starts bash session in the container
```

5. Inside the container, you can import and use the provided classes to build your custom trading bot:

```python
from logger import Logger
from exchange_base import ExchangeBase

logger = Logger.instance()
exchange = ExchangeBase('binance')

balance = exchange.fetch_balance()
logger.info(f"Balance: {balance}")
```

## Contributing

Contributions are welcome! Please submit a pull request or create an issue to discuss any changes or improvements.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).
