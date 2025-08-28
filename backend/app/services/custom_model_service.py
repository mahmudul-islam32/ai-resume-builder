from typing import Dict, Any, Optional
import json
import asyncio
from abc import ABC, abstractmethod


class CustomModelInterface(ABC):
    """Abstract base class for custom model implementations."""
    
    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using the custom model."""
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the model is available and ready to use."""
        pass


class CustomModelService:
    """Service for integrating custom models for cover letter generation."""
    
    def __init__(self, model_interface: CustomModelInterface):
        self.model = model_interface
    
    async def generate_cover_letter(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_title: str,
        applicant_name: str,
        additional_info: Optional[str] = None,
        **model_kwargs
    ) -> str:
        """
        Generate a personalized cover letter using custom model.
        
        Args:
            resume_content: Resume text
            job_description: Job posting description
            company_name: Company name
            job_title: Job title
            applicant_name: Applicant's name
            additional_info: Additional information to include
            **model_kwargs: Additional parameters for the custom model
            
        Returns:
            Generated cover letter text
        """
        
        if not await self.model.is_available():
            raise Exception("Custom model is not available")
        
        prompt = self._build_cover_letter_prompt(
            resume_content, job_description, company_name, 
            job_title, applicant_name, additional_info
        )
        
        try:
            response = await self.model.generate_text(prompt, **model_kwargs)
            return response.strip()
        except Exception as e:
            raise Exception(f"Custom model error: {str(e)}")
    
    async def generate_customized_cover_letter(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_title: str,
        applicant_name: str,
        customization: dict,
        **model_kwargs
    ) -> str:
        """
        Generate a customized cover letter using custom model.
        
        Args:
            resume_content: Resume text
            job_description: Job posting description
            company_name: Company name
            job_title: Job title
            applicant_name: Applicant's name
            customization: Dictionary containing customization options
            **model_kwargs: Additional parameters for the custom model
            
        Returns:
            Generated cover letter text
        """
        
        if not await self.model.is_available():
            raise Exception("Custom model is not available")
        
        prompt = self._build_customized_cover_letter_prompt(
            resume_content, job_description, company_name,
            job_title, applicant_name, customization
        )
        
        try:
            response = await self.model.generate_text(prompt, **model_kwargs)
            return response.strip()
        except Exception as e:
            raise Exception(f"Custom model error: {str(e)}")
    
    def _build_cover_letter_prompt(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_title: str,
        applicant_name: str,
        additional_info: Optional[str] = None
    ) -> str:
        """Build the prompt for cover letter generation."""
        
        return f"""
        You are an expert cover letter writer. Create a compelling, personalized cover letter based on the following information:

        APPLICANT NAME: {applicant_name}
        JOB TITLE: {job_title}
        COMPANY: {company_name}

        RESUME CONTENT:
        {resume_content}

        JOB DESCRIPTION:
        {job_description}

        ADDITIONAL INFORMATION:
        {additional_info or "None provided"}

        Create a professional cover letter that:
        - Is addressed to the hiring manager
        - Shows enthusiasm for the specific role and company
        - Highlights relevant experience from the resume
        - Demonstrates knowledge of the company/role
        - Is concise (3-4 paragraphs)
        - Has a professional tone
        - Includes a strong opening and closing

        Return only the cover letter text, properly formatted.
        """
    
    def _build_customized_cover_letter_prompt(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_title: str,
        applicant_name: str,
        customization: dict
    ) -> str:
        """Build the prompt for customized cover letter generation."""
        
        tone = customization.get('tone', 'professional')
        focus_areas = customization.get('focus_areas', [])
        custom_instructions = customization.get('custom_instructions', '')
        include_salary = customization.get('include_salary_expectations', False)
        include_availability = customization.get('include_availability', False)
        include_portfolio = customization.get('include_portfolio_link', False)
        
        # Build focus areas instruction
        focus_instruction = ""
        if focus_areas:
            focus_instruction = f"\n\nFOCUS ON THESE AREAS: {', '.join(focus_areas)}"
        
        # Build additional requirements
        additional_requirements = []
        if include_salary:
            additional_requirements.append("Include salary expectations")
        if include_availability:
            additional_requirements.append("Include availability information")
        if include_portfolio:
            additional_requirements.append("Include portfolio/work samples link")
        
        additional_instruction = ""
        if additional_requirements:
            additional_instruction = f"\n\nADDITIONAL REQUIREMENTS: {', '.join(additional_requirements)}"
        
        return f"""
        You are an expert cover letter writer. Create a compelling, personalized cover letter based on the following information:

        APPLICANT NAME: {applicant_name}
        JOB TITLE: {job_title}
        COMPANY: {company_name}

        RESUME CONTENT:
        {resume_content}

        JOB DESCRIPTION:
        {job_description}

        WRITING TONE: {tone.upper()}
        {focus_instruction}
        {additional_instruction}

        CUSTOM INSTRUCTIONS:
        {custom_instructions or "None provided"}

        Create a professional cover letter that:
        - Is addressed to the hiring manager
        - Shows enthusiasm for the specific role and company
        - Highlights relevant experience from the resume
        - Demonstrates knowledge of the company/role
        - Is concise (3-4 paragraphs)
        - Has a {tone} tone
        - Includes a strong opening and closing
        - Follows all the specified focus areas and requirements

        Return only the cover letter text, properly formatted.
        """


# Example implementations for different model types

class HuggingFaceModel(CustomModelInterface):
    """Example implementation for Hugging Face models."""
    
    def __init__(self, model_name: str, api_token: Optional[str] = None):
        self.model_name = model_name
        self.api_token = api_token
        self._client = None
    
    async def is_available(self) -> bool:
        """Check if the model is available."""
        try:
            # Add your model availability check here
            return True
        except Exception:
            return False
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Hugging Face model."""
        try:
            # Add your Hugging Face API call here
            # Example:
            # from transformers import pipeline
            # generator = pipeline('text-generation', model=self.model_name)
            # response = generator(prompt, max_length=500, **kwargs)
            # return response[0]['generated_text']
            
            # Placeholder implementation
            return f"[Generated by {self.model_name}]: {prompt[:100]}..."
            
        except Exception as e:
            raise Exception(f"Hugging Face model error: {str(e)}")


class LocalLLMModel(CustomModelInterface):
    """Example implementation for local LLM models (e.g., Ollama, llama.cpp)."""
    
    def __init__(self, model_path: str, api_url: str = "http://localhost:11434"):
        self.model_path = model_path
        self.api_url = api_url
    
    async def is_available(self) -> bool:
        """Check if the local model is available."""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}/api/tags") as response:
                    return response.status == 200
        except Exception:
            return False
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using local LLM model."""
        try:
            import aiohttp
            import json
            
            payload = {
                "model": self.model_path,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('response', '')
                    else:
                        raise Exception(f"API request failed: {response.status}")
                        
        except Exception as e:
            raise Exception(f"Local LLM model error: {str(e)}")


class AnthropicModel(CustomModelInterface):
    """Example implementation for Anthropic Claude models."""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key
        self.model = model
    
    async def is_available(self) -> bool:
        """Check if the Anthropic model is available."""
        return bool(self.api_key)
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Anthropic Claude model."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 2000),
                temperature=kwargs.get('temperature', 0.7),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            raise Exception(f"Anthropic model error: {str(e)}")
