#!/usr/bin/env python3
import asyncio
import json
import os
import uuid
import logging
import httpx
import websockets
from typing import List, Dict, Any, Optional
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

# Configuració
JUPYTER_URL = "http://127.0.0.1:8888"
JUPYTER_WS = "ws://127.0.0.1:8888"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jupyter-tfm-mcp")

server = Server("jupyter-tfm-mcp")

class JupyterClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = httpx.AsyncClient(follow_redirects=True)
        self.xsrf_token = None

    async def ensure_xsrf(self):
        if not self.xsrf_token:
            try:
                resp = await self.client.get(f"{self.base_url}/lab")
                if "_xsrf" in self.client.cookies:
                    self.xsrf_token = self.client.cookies["_xsrf"]
                    logger.info(f"XSRF token obtained: {self.xsrf_token}")
                else:
                    match = resp.text.split('_xsrf=')
                    if len(match) > 1:
                        self.xsrf_token = match[1].split('"')[0].split("'")[0]
            except Exception as e:
                logger.error(f"Error obtaining XSRF: {e}")

    async def post(self, path, json_data=None):
        await self.ensure_xsrf()
        headers = {"X-XSRFToken": self.xsrf_token} if self.xsrf_token else {}
        return await self.client.post(f"{self.base_url}{path}", json=json_data, headers=headers)

    async def delete(self, path):
        await self.ensure_xsrf()
        headers = {"X-XSRFToken": self.xsrf_token} if self.xsrf_token else {}
        return await self.client.delete(f"{self.base_url}{path}", headers=headers)

    async def get(self, path):
        return await self.client.get(f"{self.base_url}{path}")

j_client = JupyterClient(JUPYTER_URL)

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="run_code",
            description="Executa codi en un kernel de Jupyter (python3, sagemath, ir).",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Codi a executar"},
                    "kernel": {"type": "string", "description": "Nom del kernel", "default": "python3"}
                },
                "required": ["code"]
            }
        ),
        types.Tool(
            name="list_kernels",
            description="Llista els kernels disponibles i els actius.",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="list_files",
            description="Llista els fitxers en el directori de treball de Jupyter.",
            inputSchema={
                "type": "object", 
                "properties": {
                    "path": {"type": "string", "description": "Camí relatiu", "default": ""}
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    try:
        if name == "list_kernels":
            specs = await j_client.get("/api/kernelspecs")
            active = await j_client.get("/api/kernels")
            result = {"available_specs": specs.json().get("kernelspecs", {}), "active_kernels": active.json()}
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "list_files":
            path = arguments.get("path", "")
            resp = await j_client.get(f"/api/contents/{path}")
            return [types.TextContent(type="text", text=json.dumps(resp.json(), indent=2))]

        elif name == "run_code":
            code = arguments.get("code")
            kernel_name = arguments.get("kernel", "python3")
            
            resp = await j_client.post("/api/kernels", json_data={"name": kernel_name})
            if resp.status_code != 201:
                return [types.TextContent(type="text", text=f"Error iniciant kernel ({resp.status_code}): {resp.text}")]
            
            kernel_id = resp.json()["id"]
            
            # Donem temps al kernel per inicialitzar-se (SageMath pot ser lent)
            wait_time = 10 if kernel_name == "sagemath" else 2
            await asyncio.sleep(wait_time)
            
            try:
                session_id = str(uuid.uuid4())
                ws_url = f"{JUPYTER_WS}/api/kernels/{kernel_id}/channels?session_id={session_id}"
                # Afegim Origin per evitar el bloqueig CSRF de Jupyter
                headers = {"Origin": JUPYTER_URL}
                async with websockets.connect(ws_url, open_timeout=30.0, additional_headers=headers) as ws:
                    msg_id = str(uuid.uuid4())
                    execute_msg = {
                        "header": {
                            "msg_id": msg_id,
                            "username": "antigravity",
                            "session": str(uuid.uuid4()),
                            "msg_type": "execute_request",
                            "version": "5.3"
                        },
                        "parent_header": {},
                        "metadata": {},
                        "content": {"code": code, "silent": False, "store_history": True},
                        "channel": "shell"
                    }
                    await ws.send(json.dumps(execute_msg))
                    
                    outputs = []
                    while True:
                        try:
                            raw_msg = await asyncio.wait_for(ws.recv(), timeout=30.0)
                            msg = json.loads(raw_msg)
                            msg_type = msg["header"]["msg_type"]
                            content = msg["content"]
                            
                            if msg_type in ["execute_result", "display_data"]:
                                data = content.get("data", {})
                                if "text/plain" in data: outputs.append(data["text/plain"])
                                if "text/latex" in data: outputs.append(f"LaTeX: {data['text/latex']}")
                            elif msg_type == "stream":
                                outputs.append(content["text"])
                            elif msg_type == "error":
                                outputs.append(f"ERROR: {content['ename']}: {content['evalue']}")
                            elif msg_type == "execute_reply":
                                break
                        except asyncio.TimeoutError:
                            outputs.append("Error: Temps d'espera esgotat.")
                            break
                    
                    return [types.TextContent(type="text", text="\n".join(outputs))]
            finally:
                await j_client.delete(f"/api/kernels/{kernel_id}")

    except Exception as e:
        return [types.TextContent(type="text", text=f"Excepció: {str(e)}")]

    return [types.TextContent(type="text", text=f"Tool no trobada: {name}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(
            server_name="jupyter-tfm-mcp", server_version="1.0.0",
            capabilities=server.get_capabilities(notification_options=NotificationOptions(), experimental_capabilities={})
        ))

if __name__ == "__main__":
    asyncio.run(main())
