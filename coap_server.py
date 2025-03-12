import asyncio
from aiocoap import resource, Context, Message
from aiocoap.numbers.codes import CHANGED

class SensorResource(resource.Resource):
    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        print(f"Received data: {payload}")
        # Respond with a simple confirmation message
        return Message(code=CHANGED, payload=b"Data received")

async def main():
    # Create the resource tree
    root = resource.Site()

    # Add our custom resource at /sensor/data
    root.add_resource(['sensor', 'data'], SensorResource())

    # Create a CoAP server context bound to localhost on port 5683
    await Context.create_server_context(root, bind=('localhost', 5683))

    # Keep the server running indefinitely
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
