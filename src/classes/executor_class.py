import os
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
)  # for exponential backoff
import copy
from typing import List, Dict, Set


class Module():
    def send(self, query):
        pass


    
class GPT(Module):
    def __init__(self, prompt="", model="gpt-3.5-turbo"):
        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.prompt = prompt
        self.model = model
         
    @retry(wait=wait_fixed(30), stop=stop_after_attempt(2))
    def send(self,context:str, answers:List[str]=[],max_tokens=350):
        prompt = copy.deepcopy(self.prompt)
        prompt.append({
            "role": "user",
            "content": context
            })
        for answer in answers:
            prompt.append({
                "role": "assistant",
                "content": answer
                })
        response = self.client.chat.completions.create(
            model=self.model,
            messages=prompt,
            temperature=0.0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content

