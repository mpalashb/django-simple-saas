import json
import time
from django.conf import settings
import openai

openai.api_key = settings.OPENAI_KEY


def check_proposal(cover_desc, job_desc):

    max_tkn = 200

    # if len(title) < max_len & len(desc) < max_len:
    #     print('yeah')

    prompt = f"""
    Check the job job proposal or cover letter very carefully to analysis the cover letter '{cover_desc}' for this Upwork job '{job_desc}' and share best result.
    Provide me the requested information in JSON format without any hint text or other, making sure to include the following keywords: 'result', 'rating', and 'suggest_cover'. Ensure that all keywords are lowercase and must enclosed within json quotes.

    1. Set the 'rating' keyword to a value between 1 and 100 to indicate the rating of the proposal or cover letter for that job.
    2. Set the 'result' keyword to one of the following options: 'good', 'moderate', or 'bad' to describe of the proposal or cover letter for that job.
    3. Now suggested a cover letter within a few lines and set it as the value for the 'suggest_cover' keyword.

    Must follow the structure and response accordingly, and make sure the entire response fits within the maximum token limit of {max_tkn}.
    """
    # print(prompt)
    # prompt = f"""
    # Carefully analyze the job proposal or cover letter '{cover_desc}' for the Upwork job '{job_desc}' and provide the result.

    # Provide the requested information in JSON format, ensuring that all keywords ('result', 'rating', and 'suggest_cover') are lowercase and enclosed within quotes. This format will allow us to easily load the text using `json.loads()` in Python.

    # Instructions:
    # 1. Set the 'rating' keyword to a value between 1 and 100 to indicate the quality of the proposal or cover letter for the job.
    # 2. Set the 'result' keyword to one of the following options: 'good', 'moderate', 'bad', to describe the quality of the proposal or cover letter. Assign a value of 0 to 40 for bad, 40 to 70 moderate and 70 to 100 is good 'rating'.
    # 3. Suggest a concise cover letter within a few lines and set it as the value for the 'suggest_cover' keyword.

    # Adhere to the provided structure and respond accordingly,
    # ensuring that the entire response fits within the maximum token limit of {max_tkn} and
    # any blank results should be enclosed within empty json quotes.
    # """

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=max_tkn
        )

        res = response.get('choices')[0].get('text')
        print('--------------------------------------------------------------')
        print(res)
        print('--------------------------------------------------------------')
        a_res = {}
        try:
            # '''-------------------------------------'''
            # time.sleep(2)
            # '''-------------------------------------'''
            js_loads = json.loads(res)
            # print('json loads')
            # print(js_loads)
            # print('json loads')

            items = {}
            result = js_loads.get('result')
            rating = js_loads.get('rating')
            suggest_cover = js_loads.get('suggest_cover')

            items['result'] = result
            items['rating'] = str(rating)
            items['suggest_cover'] = suggest_cover

            a_res = items

        except Exception as js_p:
            print('json.loads error------------------------')
            print(js_p)
            print('json.loads error------------------------')
            a_res = {'msg': 'No result found!'}

        return a_res
    except Exception as p:
        print(p)
        a_res = {'msg': 'Internal API issues!'}

    return a_res


def gen_proposal(title, desc, type_of='normal', client_name=None):

    max_tkn = 200

    # if len(title) < max_len & len(desc) < max_len:
    #     print('yeah')

    prompt = f"""Create a upwork professional job proposal or cover leter for this job. title:'{title}' job description: '{desc}' | """ + \
        f"and everything within in max_tokens of {max_tkn}"

    if type_of == 'short':
        prompt = f"""Create a upwork professional job proposal or cover leter as short as posiable  like 5-7 lines for this job. title:'{title}' job description: '{desc}' | """ + \
            f"and everything within in max_tokens of {max_tkn}"

    if type_of == 'very_short':
        prompt = f"""Create a upwork professional job proposal or cover leter very much short like 2-3 lines as posiable for this job. title:'{title}' job description: '{desc}' | """ + \
            f"and everything within in max_tokens of {max_tkn}"

    if client_name and type_of == 'normal':
        prompt = f"""Create a upwork professional job proposal or cover leter for this job. title:'{title}' job description: '{desc}' and found the client name: '{client_name}' |  """ + \
            f"and everything within in max_tokens of {max_tkn}"

    if client_name and type_of == 'short':
        prompt = f"""Create a upwork professional job proposal or cover leter as short as posiable like 5-7 lines for this job. title:'{title}' job description: '{desc}' and found the client name: '{client_name}' |  """ + \
            f"and everything within in max_tokens of {max_tkn}"
    if client_name and type_of == 'very_short':
        prompt = f"""Create a upwork professional job proposal or cover leter very much short like 2-3 lines as posiable for this job. title:'{title}' job description: '{desc}' and found the client name: '{client_name}' |  """ + \
            f"and everything within in max_tokens of {max_tkn}"

    # print(prompt)

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=max_tkn,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        res = response.get('choices')[0].get('text')
        # res = "We got somethings"
        # res = None

        return res
    except Exception as p:
        print(p)

    return None
