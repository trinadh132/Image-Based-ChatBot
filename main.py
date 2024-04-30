from openai import OpenAI
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from mangum import Mangum

openai = OpenAI(
    api_key="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"
)

app = FastAPI()
handler = Mangum(app)

templates = Jinja2Templates(directory='templates')


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


chat_log = [{'role': 'system',
             'content': 'You are CAPSTONE(a helpful chatbot).'
             }]

chat_responses = []


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):

    chat_log.append({'role': 'user', 'content': user_input})
    chat_responses.append(user_input)

    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=chat_log,
        temperature=0.6
    )

    respons = openai.images.generate(
        prompt=user_input,
        n=1,
        size="512x512"
    )

    image_url = respons.data[0].url

    bot_response = response.choices[0].message.content
    chat_log.append({'role': 'assistant', 'content': bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses, "image_url": image_url})




@app.get("/image", response_class=HTMLResponse)
async def image_page(request: Request):
    return templates.TemplateResponse("image.html", {"request": request})


@app.post("/image", response_class=HTMLResponse)
async def create_image(request: Request, user_input: Annotated[str, Form()]):

    response = openai.images.generate(
        prompt=user_input,
        n=1,
        size="512x512"
    )

    image_url = response.data[0].url

    return templates.TemplateResponse("image.html", {"request": request, "image_url": image_url})
