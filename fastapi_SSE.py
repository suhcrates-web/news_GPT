from fastapi import FastAPI, Depends, Request, HTTPException
from starlette.responses import StreamingResponse
from typing import Optional
from pydantic import BaseModel
import time
import openai
from question_to_answer import question_text_to_answer
from query_keyword import query_keyword
from key_to_text import key_to_text
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
app = FastAPI()

origins = [
    "http://localhost:5232"  # This is the origin of your client, change it if needed
]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class Input(BaseModel):
#     data: str

# @app.get('/donga/test')
# async def index_brod():
#     # FastAPI does not have a built-in support for templating like Flask. 
#     # So you might want to use a different service to serve your HTML and JS.
#     pass

# @app.post('/set_data')
# async def set_data(input: Input, request: Request):
#     print('shit 1')
#     request.state.data = input.data
#     print(request.state.data)
#     return ''

@app.get('/stream')
async def stream(data):
    # print('shit 2')
    # data = getattr(request.state, 'data', '')
    print(data)

    async def event_stream():
        # for _ in range(10):
            # await asyncio.sleep(1)
            # yield f"data: shit\n\n"

        #질문
        back1 = f"#질문 : {data} <br><br>#키워드:"
        yield f"data: {back1}\n\n"
        await asyncio.sleep(0)

        #키워드
        key_word = query_keyword(data)
        back2 = f"{key_word}<br><br>#추천기사:"
        yield f"data: {back2}\n\n"
        await asyncio.sleep(0)

        #기사검색
        text0, result_list = key_to_text(key_word)
        article_list = ''
        for url0, tit0 in result_list:
            article_list += f'<a href="{url0}">{tit0}</a><br>'
        back3 = article_list+"<br>#답:"
        yield f"data: {back3}\n\n"
        await asyncio.sleep(0)

        #답
        prompt = f"""{text0}\n\n위 내용들을 바탕으로 대답해줘.\n{data}
            """
        print(prompt)
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        print("herererererererer")
        
        answer =f"{completion['choices'][0]['message']['content']} <br>================================="
        print(answer)
        yield f"data: {answer}\n\n"
        await asyncio.sleep(0)
        yield f"data: end\n\n"
        await asyncio.sleep(0)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == '__main__':
    uvicorn.run(app, port=8001, host='0.0.0.0')