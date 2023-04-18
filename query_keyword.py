# coding=utf-8
import openai

def query_keyword(question):
    prompt = f"""
    {question}
    ===========
    이 질문에 맞는 검색어를 2개 나열해줘.  ','를 구분자로
    """

    openai.api_key="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"
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
