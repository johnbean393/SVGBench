from openai import OpenAI
import base64
import os
import requests
import json

# Class to interact with OpenAI compatible APIs
class LLM:

    # Function to initialize the LLM class
    def __init__(
            self, 
            model: str, 
            endpoint: str,
            api_key: str,
            reasoning_effort: str = None,
            reasoning_max_tokens: int = None,
            max_output_tokens: int = None
    ):
        # Initialize the OpenAI client
        self.client = OpenAI(
            api_key=api_key, 
            base_url=endpoint
        )
        # Set the model
        self.model = model
        # Store reasoning parameters
        self.reasoning_effort = reasoning_effort
        self.reasoning_max_tokens = reasoning_max_tokens
        self.max_output_tokens = max_output_tokens
        # Store endpoint and API key for direct requests when needed
        self.endpoint = endpoint
        self.api_key = api_key

    # Function to generate text from a prompt and an optional image
    def generate_text(
            self, 
            prompt: str, 
            image_path: str = None,
            json_schema: dict = None
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
        # Prepare the request parameters
        request_params = {
            "model": self.model,
            "messages": messages
        }
        # Add structured output if JSON schema is provided
        if json_schema:
            request_params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_response",
                    "schema": json_schema
                }
            }
        # Add max output tokens if specified
        if self.max_output_tokens:
            # Use max_completion_tokens for o-series models, max_tokens for others
            if any(model_name in self.model.lower() for model_name in ['o3', 'o4', 'o1']):
                request_params["max_completion_tokens"] = self.max_output_tokens
            else:
                request_params["max_tokens"] = self.max_output_tokens
        # Add reasoning parameters if specified
        if self.reasoning_effort or self.reasoning_max_tokens:
            reasoning_config = {}
            if self.reasoning_effort:
                reasoning_config["effort"] = self.reasoning_effort
            if self.reasoning_max_tokens:
                reasoning_config["max_tokens"] = self.reasoning_max_tokens
            request_params["reasoning"] = reasoning_config
        # Generate text
        # Use direct HTTP request if reasoning parameters are specified
        if self.reasoning_effort or self.reasoning_max_tokens:
            return self._generate_with_reasoning(request_params)
        else:
            response = self.client.chat.completions.create(**request_params)
            return response.choices[0].message.content
    
    def _generate_with_reasoning(self, request_params):
        """Generate text using direct HTTP request to support reasoning parameters"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                f"{self.endpoint}/chat/completions",
                headers=headers,
                json=request_params,
                timeout=1800
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"Warning: Direct API call failed ({error_msg}). Falling back to OpenAI client without reasoning.")
                # Fallback to OpenAI client without reasoning
                if "reasoning" in request_params:
                    del request_params["reasoning"]
                fallback_response = self.client.chat.completions.create(**request_params)
                return fallback_response.choices[0].message.content
                
        except Exception as e:
            print(f"Warning: Direct API call failed ({e}). Falling back to OpenAI client without reasoning.")
            # Fallback to OpenAI client without reasoning
            if "reasoning" in request_params:
                del request_params["reasoning"]
            fallback_response = self.client.chat.completions.create(**request_params)
            return fallback_response.choices[0].message.content
    
# Example usage
if __name__ == "__main__":
    # Get the directory two levels up from the current file
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Load environment variable from .env file in that directory
    from dotenv import load_dotenv
    load_dotenv(os.path.join(parent_dir, '.env'))
    # Get the API key from the environment variable
    api_key = os.getenv("OPENROUTER_API_KEY")
    # Create an instance of the LLM class
    llm = LLM(
        model="google/gemini-2.0-flash-001",
        endpoint="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    # Test image understanding
    print(llm.generate_text(prompt="What is in this image?", image_path="assets/test_image.png"))
    # Test JSON schema
    app_ideas = llm.generate_text(prompt="Generate 3 mobile app ideas.", json_schema={
        "type": "object",
        "properties": {
            "mobile_app_ideas": {"type": "array", "items": {"type": "string"}}
        }
    })
    print(app_ideas)