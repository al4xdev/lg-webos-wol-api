# TV & PC Control API

> [!NOTE]
> This is a random personal project shared publicly. It is no longer actively maintained but is published in case it might be useful to someone else!

A lightweight FastAPI application designed to control LG WebOS TVs and wake local PCs using Wake-on-LAN (WoL).

## Features

- **Wake-on-LAN (WoL)**: Power on your TV and configured PCs remotely.
- **LG WebOS Control**: Turn off (standby), turn on screen, and adjust volume using the `pywebostv` library.
- **REST API**: Simple POST endpoints for integration with home automation tools (e.g., Home Assistant, custom widgets, or shortcuts).
- **Dockerized**: Easy to build and deploy as a Docker container.

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/wake-tv` | `POST` | Sends a Wake-on-LAN magic packet to turn on the TV. |
| `/wake-pc` | `POST` | Sends a Wake-on-LAN magic packet to turn on your PC. |
| `/wake-pc-dad` | `POST` | Sends a Wake-on-LAN magic packet to turn on your dad's PC. |
| `/turn-on-tv` | `POST` | Turns on the TV screen and sets volume to 70. Fallbacks to WoL if connection fails. |
| `/turn-off-tv` | `POST` | Puts the TV in standby mode. |
| `/set-volume/{volume}` | `POST` | Adjusts TV volume to the specified percentage (e.g., `/set-volume/30`). |

## Configuration

This application is configured entirely via environment variables. Copy the example template to create your `.env` file:

```bash
cp .env.example .env
```

Open `.env` and fill in the values for your devices:

```env
# TV Configuration
TV_IP=192.168.0.95
TV_MAC=E0:51:63:73:A7:EF
TV_KEY=your_tv_client_key_here

# My PC Configuration
MY_PC_IP=192.168.0.83
MY_PC_MAC=1C:BF:CE:E9:5D:C1

# Dad PC Configuration
DAD_PC_IP=192.168.0.44
DAD_PC_MAC=00:A5:54:56:54:91
```

> [!NOTE]
> The `TV_KEY` is the pairing key registered with your LG WebOS TV. If you don't have one yet, when you first run the server and trigger an endpoint, follow the pairing prompt on your TV screen.

## Installation & Running

### Option 1: Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```

### Option 2: Running via Docker

1. Build the Docker image:
   ```bash
   docker build -t tv-control-api .
   ```

2. Run the container, passing the environment variables:
   ```bash
   docker run -d --name tv-control -p 8080:8080 --env-file .env tv-control-api
   ```

## License

This project is open-source and available under the [MIT License](LICENSE).
