from sanic import Sanic
from sanic.response import json

from api.webhooks import webhooks_router

app = Sanic(name='dj-pep-api')


@app.get('/')
async def alive(request):
    return json({'service': app.name})


app.blueprint(webhooks_router)
