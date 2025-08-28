from typing import Optional
from app.core.config import settings
from app.services.custom_model_service import (
    CustomModelInterface, 
    HuggingFaceModel, 
    LocalLLMModel, 
    AnthropicModel
)


class ModelFactory:
    """Factory for creating model instances based on configuration."""
    
    @staticmethod
    def create_model() -> Optional[CustomModelInterface]:
        """
        Create a model instance based on configuration.
        
        Returns:
            CustomModelInterface instance or None if no model is configured
        """
        
        if not settings.use_custom_model:
            return None
        
        model_type = settings.custom_model_type.lower()
        config = settings.custom_model_config or {}
        
        if model_type == "huggingface":
            return HuggingFaceModel(
                model_name=config.get("model_name", "gpt2"),
                api_token=config.get("api_token")
            )
        
        elif model_type == "local":
            return LocalLLMModel(
                model_path=config.get("model_path", "llama2"),
                api_url=config.get("api_url", "http://localhost:11434")
            )
        
        elif model_type == "anthropic":
            return AnthropicModel(
                api_key=config.get("api_key") or settings.anthropic_api_key,
                model=config.get("model", "claude-3-sonnet-20240229")
            )
        
        elif model_type == "custom":
            # Import your custom model implementation
            from app.services.my_custom_model import MyCustomModel
            return MyCustomModel(
                api_url=config.get("api_url"),
                api_key=config.get("api_key"),
                model_name=config.get("model_name", "my-model")
            )
        
        elif model_type == "huggingface_inference":
            from app.services.my_custom_model import HuggingFaceInferenceModel
            return HuggingFaceInferenceModel(
                model_name=config.get("model_name", "gpt2"),
                api_token=config.get("api_token")
            )
        
        elif model_type == "ollama":
            from app.services.my_custom_model import OllamaModel
            return OllamaModel(
                model_name=config.get("model_name", "llama2"),
                api_url=config.get("api_url", "http://localhost:11434")
            )
        
        elif model_type == "cohere":
            from app.services.my_custom_model import CohereModel
            return CohereModel(
                api_key=config.get("api_key"),
                model=config.get("model", "command")
            )
        
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    @staticmethod
    def get_available_models() -> list:
        """Get list of available model types."""
        return [
            "openai",
            "anthropic", 
            "huggingface",
            "huggingface_inference",
            "ollama",
            "cohere",
            "local",
            "custom"
        ]
    
    @staticmethod
    def validate_config(model_type: str, config: dict) -> bool:
        """
        Validate model configuration.
        
        Args:
            model_type: Type of model
            config: Configuration dictionary
            
        Returns:
            True if configuration is valid
        """
        
        if model_type == "huggingface":
            required_keys = ["model_name"]
            return all(key in config for key in required_keys)
        
        elif model_type == "local":
            required_keys = ["model_path"]
            return all(key in config for key in required_keys)
        
        elif model_type == "anthropic":
            required_keys = ["api_key"]
            return all(key in config for key in required_keys)
        
        elif model_type == "custom":
            # Add validation for your custom model
            return True
        
        else:
            return False
