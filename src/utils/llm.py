from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

# Class to interact with the OpenAI API
class LLM:

    def __init__(
            self, 
            model: str, 
            endpoint: str = "https://api.openai.com/v1",
            api_key: str = os.getenv("OPENAI_API_KEY")
    ):
        self.client = OpenAI(
            api_key=api_key, 
            base_url=endpoint
        )
        self.model = model

    def generate_text(
            self, 
            prompt: str, 
            image_path: str = None
    ) -> str:
        # If image_path is provided, add it to the message content
        if image_path:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        else:
            # If no image_path is provided, just use the prompt
            messages = [{"role": "user", "content": prompt}]
        # Generate text
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        # Return the generated text
        return response.choices[0].message.content
    
# Example usage
if __name__ == "__main__":
    # Get the directory two levels up from the current file
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Load environment variable from .env file in that directory
    load_dotenv(os.path.join(parent_dir, '.env'))
    # Get the API key from the environment variable
    api_key = os.getenv("OPENROUTER_API_KEY")
    # Create an instance of the LLM class
    llm = LLM(
        model="google/gemini-2.0-flash-001",
        endpoint="https://ai-proxy.chatwise.app/openrouter/api/v1",
        api_key=api_key
    )
    print(llm.generate_text(prompt="What is in this image?", image_path="assets/test_image.png"))