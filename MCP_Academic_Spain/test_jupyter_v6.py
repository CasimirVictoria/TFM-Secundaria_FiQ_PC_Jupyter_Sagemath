import asyncio
import json
import httpx
import websockets
import uuid

async def test():
    base_url = "http://127.0.0.1:8888"
    ws_base = "ws://127.0.0.1:8888"
    client = httpx.AsyncClient(follow_redirects=True)
    resp = await client.get(f"{base_url}/lab")
    xsrf = client.cookies.get("_xsrf")
    headers = {"X-XSRFToken": xsrf} if xsrf else {}
    resp = await client.post(f"{base_url}/api/kernels", json={"name": "sagemath"}, headers=headers)
    kernel_id = resp.json()["id"]
    print(f"Kernel {kernel_id} started.")
    await asyncio.sleep(2)
    try:
        # Provem d'afegir el token a la query string i capçaleres
        ws_url = f"{ws_base}/api/kernels/{kernel_id}/channels"
        if xsrf: ws_url += f"?_xsrf={xsrf}"
        
        ws_headers = {"Origin": base_url}
        print(f"Connecting to {ws_url}...")
        async with websockets.connect(ws_url, additional_headers=ws_headers, open_timeout=10.0) as ws:
            print("Connected!")
            msg_id = str(uuid.uuid4())
            execute_msg = {
                "header": {"msg_id": msg_id, "username": "test", "session": str(uuid.uuid4()), "msg_type": "execute_request", "version": "5.3"},
                "parent_header": {}, "metadata": {},
                "content": {"code": "print(factor(2^64 - 1))", "silent": False},
                "channel": "shell"
            }
            await ws.send(json.dumps(execute_msg))
            msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=15))
            while msg["header"]["msg_type"] != "execute_reply":
                if msg["header"]["msg_type"] == "stream":
                    print(f"Output: {msg['content']['text']}")
                msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=15))
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await client.delete(f"{base_url}/api/kernels/{kernel_id}", headers=headers)
        print("Kernel stopped.")

asyncio.run(test())
