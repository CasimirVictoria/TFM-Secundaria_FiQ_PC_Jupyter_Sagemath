import asyncio
import json
import httpx
import websockets
import uuid

async def test():
    kernel_name = "sagemath"
    code = "print(factor(2^64 - 1))"
    
    # Start kernel
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://127.0.0.1:8888/api/kernels", json={"name": kernel_name})
        kernel_id = resp.json()["id"]
        print(f"Kernel started: {kernel_id}")
        
        try:
            ws_url = f"ws://127.0.0.1:8888/api/kernels/{kernel_id}/channels"
            async with websockets.connect(ws_url) as ws:
                msg_id = str(uuid.uuid4())
                execute_msg = {
                    "header": {"msg_id": msg_id, "username": "test", "session": str(uuid.uuid4()), "msg_type": "execute_request", "version": "5.3"},
                    "parent_header": {}, "metadata": {},
                    "content": {"code": code, "silent": False},
                    "channel": "shell"
                }
                await ws.send(json.dumps(execute_msg))
                
                while True:
                    msg = json.loads(await ws.recv())
                    if msg["header"]["msg_type"] == "stream":
                        print(f"Output: {msg['content']['text']}")
                    if msg["header"]["msg_type"] == "execute_reply":
                        break
        finally:
            await client.delete(f"http://127.0.0.1:8888/api/kernels/{kernel_id}")
            print("Kernel stopped.")

asyncio.run(test())
