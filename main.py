import os
from dataclasses import dataclass
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pywebostv.connection import WebOSClient
from pywebostv.controls import MediaControl, SystemControl
import wakeonlan

# Load environment variables from .env file for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@dataclass
class TVConfig:
    ip: str = os.getenv("TV_IP", "")
    mac: str = os.getenv("TV_MAC", "")
    key: str = os.getenv("TV_KEY", "")


@dataclass
class MyPCConfig:
    ip: str = os.getenv("MY_PC_IP", "")
    mac: str = os.getenv("MY_PC_MAC", "")


@dataclass
class DadPCConfig:
    ip: str = os.getenv("DAD_PC_IP", "")
    mac: str = os.getenv("DAD_PC_MAC", "")


def get_tv_controls():
    if not TVConfig.ip or not TVConfig.key:
        print("TV_IP or TV_KEY environment variables are not set.")
        return None, None, None

    client = WebOSClient(TVConfig.ip)
    store = {"client_key": TVConfig.key}

    try:
        client.connect()
        for status in client.register(store):
            if status == WebOSClient.REGISTERED:
                print("Connected to TV!")
                system = SystemControl(client)
                media = MediaControl(client)
                return system, media, client
            elif status == WebOSClient.FAILED:
                print("Failed to connect")
                return None, None, None
    except Exception as e:
        print(f"Error connecting: {e}")
        return None, None, None


@app.post("/wake-tv")
async def wake_tv():
    try:
        if not TVConfig.mac or not TVConfig.ip:
            raise ValueError("TV_MAC or TV_IP environment variables are not set.")
        wakeonlan.send_magic_packet(TVConfig.mac, ip_address=TVConfig.ip)
        return {"status": "Power on command sent (WoL)!"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send WoL: {str(e)}"
        )


@app.post("/wake-pc")
async def wake_pc():
    try:
        if not MyPCConfig.mac or not MyPCConfig.ip:
            raise ValueError(
                "MY_PC_MAC or MY_PC_IP environment variables are not set."
            )
        wakeonlan.send_magic_packet(MyPCConfig.mac, ip_address=MyPCConfig.ip)
        return {"status": "Power on command sent (WoL)!"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send WoL: {str(e)}"
        )


@app.post("/wake-pc-dad")
async def wake_pc_dad():
    try:
        if not DadPCConfig.mac or not DadPCConfig.ip:
            raise ValueError(
                "DAD_PC_MAC or DAD_PC_IP environment variables are not set."
            )
        wakeonlan.send_magic_packet(DadPCConfig.mac, ip_address=DadPCConfig.ip)
        return {"status": "Power on command sent (WoL)!"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send WoL: {str(e)}"
        )


@app.post("/turn-on-tv")
async def turn_on_tv():
    try:
        system, media, client = get_tv_controls()
        if system:
            system.screen_on()
            media.set_volume(70)
            client.close()
            return {"status": "TV turned on (screen_on)!"}
        else:
            return await wake_tv()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")


@app.post("/turn-off-tv")
async def turn_off_tv():
    try:
        system, _, client = get_tv_controls()
        if system:
            system.power_off()  # Put in standby
            client.close()
            return {"status": "TV in standby (screen_off)!"}
        else:
            raise HTTPException(
                status_code=500, detail="TV is already turned off or unreachable"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/set-volume/{volume}")
async def set_volume(volume: int):
    try:
        _, media, client = get_tv_controls()
        if media:
            media.set_volume(volume)
            client.close()
            return {"status": f"Volume set to {volume}%"}
        else:
            raise HTTPException(status_code=500, detail="TV is unreachable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)