from openai import OpenAI
import Keys

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=Keys.api_key,
)
