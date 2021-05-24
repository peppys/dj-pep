from sanic import Sanic
from sanic.response import json

from api.taskhandlers import task_handlers_router
from api.webhooks import webhooks_router

app = Sanic(name='dj-pep-api')
app.config.RESPONSE_TIMEOUT = 300


@app.get('/')
async def alive(request):
    return json({'service': app.name})


app.blueprint(task_handlers_router)
app.blueprint(webhooks_router)
