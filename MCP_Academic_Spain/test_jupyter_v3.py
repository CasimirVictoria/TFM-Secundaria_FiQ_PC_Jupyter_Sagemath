import asyncio
import json
import httpx
import websockets
import uuid

async def test():
    base_url = "http://127.0.0.1:8888"
    client = httpx.AsyncClient(follow_redirects=True)
    
    # Visit /lab to get XSRF
    resp = await client.get(f"{base_url}/lab")
    xsrf = client.cookies.get("_xsrf")
    print(f"XSRF obtained: {xsrf is not None}")
    
    # Start kernel
    headers = {"X-XSRFToken": xsrf} if xsrf else {}
    resp = await client.post(f"{base_url}/api/kernels", json={"name": "sagemath"}, headers=headers)
    if resp.status_code != 201:
        print(f"Error: {resp.status_code} {resp.text}")
        return
        
    kernel_id = resp.json()["id"]
    print(f"Kernel started: {kernel_id}")
    
    try:
        ws_url = f"ws://127.0.0.1:8888/api/kernels/{kernel_id}/channels"
        ws_headers = {"Cookie": f"_xsrf={xsrf}"} if xsrf else {}
        async with websockets.connect(ws_url, extra_headers=ws_headers) as ws:
            msg_id = str(uuid.uuid4())
            execute_msg = {
                "header": {"msg_id": msg_id, "username": "test", "session": str(uuid.uuid4()), "msg_type": "execute_request", "version": "5.3"},
                "parent_header": {}, "metadata": {},
                "content": {"code": "print(factor(2^64 - 1))", "silent": False},
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
        await client.delete(f"{base_url}/api/kernels/{kernel_id}", headers=headers)
        print("Kernel stopped.")

asyncio.run(test())
