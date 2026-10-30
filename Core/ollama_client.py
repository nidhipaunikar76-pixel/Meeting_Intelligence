import ollama

class LocalLLMClient:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name

    def query_model(self, prompt: str, system_instruction: str = "") -> str:
        """Sends data strings safely to your local running Ollama model layer."""
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = ollama.chat(model=self.model_name, messages=messages)
            return response['message']['content']
        except Exception as e:
            raise RuntimeError(
                f"Could not connect to the local Ollama backend engine: {str(e)}\n"
                f"Please ensure you have run: 'ollama run llama3.2' in a separate terminal window."
            )
