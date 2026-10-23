from groq import AsyncGroq
from my_genai_package.config import settings

Client=AsyncGroq(api_key=settings.groq_api_key)

async def get_groq_reply(user_message:str)->str:
    completion=await Client.chat.completions.create(
        messages=[
            {
                "role":"user",
                "content":user_message
            }
        ],
        model=settings.model
    )
    return completion.choices[0].message.content