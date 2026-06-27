import sys
import asyncio
import httpx
import httpx_sse
import json
from urllib.parse import urljoin

async def proxy(sse_url):
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(None)) as client:
            async with httpx_sse.aconnect_sse(client, "GET", sse_url) as event_source:
                post_url = None
                
                async def read_stdin_and_post():
                    loop = asyncio.get_event_loop()
                    while True:
                        line = await loop.run_in_executor(None, sys.stdin.readline)
                        if not line:
                            break
                        line = line.strip()
                        if not line:
                            continue
                        while not post_url:
                            await asyncio.sleep(0.1)
                        try:
                            await client.post(post_url, content=line, headers={"Content-Type": "application/json"})
                        except Exception as e:
                            sys.stderr.write(f"Post error: {e}\n")

                stdin_task = asyncio.create_task(read_stdin_and_post())
                
                async for event in event_source.aiter_sse():
                    if event.event == "endpoint":
                        post_url = urljoin(sse_url, event.data)
                    elif event.event == "message":
                        sys.stdout.write(event.data + "\n")
                        sys.stdout.flush()
                
                stdin_task.cancel()
    except Exception as e:
        sys.stderr.write(f"Proxy error: {e}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    asyncio.run(proxy(sys.argv[1]))
