# coding=utf-8
import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.environ.get('openai_key')
def query_keyword(question):
    prompt = f"""
    {question}
    ===========
    이 질문을 요약하는 단어 3개 나열해줘.  ','를 구분자로
    """
    print(prompt)

    # openai.api_key="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"
    completion =openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

    )
    return completion['choices'][0]['message']['content']



