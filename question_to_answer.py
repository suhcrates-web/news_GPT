import openai
from query_keyword import query_keyword
from key_to_text import key_to_text

def question_text_to_answer(question):
    key_word = query_keyword(question)
    text0, result_list = key_to_text(key_word)
    prompt=f"""
    {text0}
    ====================
    위 내용들을 바탕으로 대답해줘.
    {question}
    """
    answer0 = f'키워드: {key_word}\n\n====================\n\n'
    for url0, tit0 in result_list:
        answer0 += f"{tit0}\n{url0}\n"
    answer0+="\n===================\n\n"

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
    answer0+= completion['choices'][0]['message']['content'].replace('위 기사에서는','')
    return answer0.replace('\n','<br>')

# print(question_text_to_answer("현재 금리 상황이 어떤지, 앞으로 투자 방향은 어때야 할지 알려줘"))