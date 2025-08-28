from typing import Dict, Any, Tuple, Optional
import json
import re
from app.core.config import settings
from app.services.model_factory import ModelFactory
from app.services.custom_model_service import CustomModelService


class AIService:
    """Service for AI-powered resume tailoring and cover letter generation."""
    
    def __init__(self):
        # Initialize custom model if configured
        self.custom_model_service = None
        if settings.use_custom_model:
            custom_model = ModelFactory.create_model()
            if custom_model:
                self.custom_model_service = CustomModelService(custom_model)
    
    async def tailor_resume(
        self, 
        resume_content: str, 
        job_description: str, 
        job_requirements: str
    ) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
        """
        Tailor resume content to match a specific job posting.
        
        Args:
            resume_content: Original resume text
            job_description: Job posting description
            job_requirements: Job requirements
            
        Returns:
            Tuple of (tailored_content, suggestions, changes_made)
        """
        
        prompt = f"""
        You are an expert resume writer and career coach. Your task is to tailor a resume to better match a specific job posting.

        ORIGINAL RESUME:
        {resume_content}

        JOB DESCRIPTION:
        {job_description}

        JOB REQUIREMENTS:
        {job_requirements}

        Please provide:
        1. A tailored version of the resume that better matches the job posting
        2. Specific suggestions for improvements
        3. A summary of changes made

        Focus on:
        - Highlighting relevant skills and experience
        - Using keywords from the job posting
        - Reordering sections to emphasize most relevant qualifications
        - Suggesting improvements to bullet points
        - Maintaining truthfulness (don't add false information)

        Return your response in the following JSON format:
        {{
            "tailored_content": "The complete tailored resume text",
            "suggestions": {{
                "keyword_additions": ["list of important keywords to add"],
                "section_improvements": ["list of section-specific suggestions"],
                "bullet_point_improvements": ["list of bullet point suggestions"]
            }},
            "changes_made": {{
                "added_keywords": ["keywords that were added"],
                "reordered_sections": ["sections that were reordered"],
                "improved_bullets": ["bullet points that were improved"]
            }}
        }}
        """
        
        try:
            if settings.openai_api_key:
                response = await self._call_openai(prompt)
            else:
                # Fallback for when no API key is provided
                response = await self._mock_tailor_response(resume_content, job_description)
            
            # Parse the JSON response
            parsed_response = json.loads(response)
            
            return (
                parsed_response["tailored_content"],
                parsed_response["suggestions"],
                parsed_response["changes_made"]
            )
            
        except Exception as e:
            print(f"❌ Failed to tailor resume: {str(e)}")
            
            # Check if it's a quota error and use mock response as fallback
            if "insufficient_quota" in str(e) or "quota_exceeded" in str(e):
                print(f"⚠️  API quota exceeded, using mock response as fallback")
                return await self._mock_tailor_response(resume_content, job_description)
            
            raise Exception(f"Failed to tailor resume: {str(e)}")
    
    async def generate_cover_letter(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_title: str,
        applicant_name: str,
        additional_info: Optional[str] = None
    ) -> str:
        """
        Generate a personalized cover letter.
        
        Args:
            resume_content: Resume text
            job_description: Job posting description
            company_name: Company name
            job_title: Job title
            applicant_name: Applicant's name
            additional_info: Additional information to include
            
        Returns:
            Generated cover letter text
        """
        
        prompt = f"""
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
        
        try:
            # Try custom model first if configured
            if self.custom_model_service:
                print(f"🔍 Using custom model for cover letter generation")
                response = await self.custom_model_service.generate_cover_letter(
                    resume_content, job_description, company_name, 
                    job_title, applicant_name, additional_info
                )
            elif settings.openai_api_key:
                response = await self._call_openai(prompt)
            else:
                # Fallback for when no API key is provided
                response = await self._mock_cover_letter_response(
                    applicant_name, job_title, company_name
                )
            
            return response.strip()
            
        except Exception as e:
            print(f"❌ Failed to generate cover letter: {str(e)}")
            
            # Check if it's a quota error and use mock response as fallback
            if "insufficient_quota" in str(e) or "quota_exceeded" in str(e):
                print(f"⚠️  API quota exceeded, using mock response as fallback")
                return await self._mock_cover_letter_response(
                    applicant_name, job_title, company_name
                )
            
            raise Exception(f"Failed to generate cover letter: {str(e)}")
    
    async def generate_customized_cover_letter(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_title: str,
        applicant_name: str,
        customization: dict
    ) -> str:
        """
        Generate a customized cover letter with specific requirements.
        
        Args:
            resume_content: Resume text
            job_description: Job posting description
            company_name: Company name
            job_title: Job title
            applicant_name: Applicant's name
            customization: Dictionary containing customization options
            
        Returns:
            Generated cover letter text
        """
        
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
        
        prompt = f"""
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
        
        try:
            # Try custom model first if configured
            if self.custom_model_service:
                print(f"🔍 Using custom model for customized cover letter generation")
                response = await self.custom_model_service.generate_customized_cover_letter(
                    resume_content, job_description, company_name,
                    job_title, applicant_name, customization
                )
            elif settings.openai_api_key:
                print(f"🔍 Generating customized cover letter with OpenAI API")
                response = await self._call_openai(prompt)
            else:
                print(f"🔍 Generating customized cover letter with mock response (no API key)")
                # Fallback for when no API key is provided
                response = await self._mock_customized_cover_letter_response(
                    applicant_name, job_title, company_name, customization
                )
            
            print(f"✅ Customized cover letter generated successfully")
            return response.strip()
            
        except Exception as e:
            print(f"❌ Failed to generate customized cover letter: {str(e)}")
            raise Exception(f"Failed to generate customized cover letter: {str(e)}")
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        try:
            from openai import AsyncOpenAI
            
            if not settings.openai_api_key:
                raise Exception("OpenAI API key not configured")
            
            print(f"🔍 OpenAI API call - Model: gpt-3.5-turbo-0125, Prompt length: {len(prompt)}")
            
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo-0125",  # Updated to latest 3.5 model
                messages=[
                    {"role": "system", "content": "You are a professional resume writer and career coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            print(f"✅ OpenAI API call successful - Response length: {len(response.choices[0].message.content)}")
            return response.choices[0].message.content
            
        except ImportError:
            print("❌ OpenAI library import error")
            raise Exception("OpenAI library not installed. Please install with: pip install openai>=1.0.0")
        except Exception as e:
            print(f"❌ OpenAI API error: {str(e)}")
            
            # Check if it's a quota error and use mock response as fallback
            if "insufficient_quota" in str(e) or "quota_exceeded" in str(e):
                print(f"⚠️  API quota exceeded, using mock response as fallback")
                return await self._mock_customized_cover_letter_response(
                    "John Doe", "Software Developer", "Tech Company", {}
                )
            
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def _mock_tailor_response(self, resume_content: str, job_description: str) -> str:
        """Mock response for resume tailoring when no API key is available."""
        
        # Extract some keywords from job description for demo
        job_words = re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower())
        keywords = list(set([word for word in job_words if len(word) > 4]))[:5]
        
        mock_response = {
            "tailored_content": f"[TAILORED VERSION]\n\n{resume_content}\n\n[Key skills highlighted: {', '.join(keywords)}]",
            "suggestions": {
                "keyword_additions": keywords,
                "section_improvements": [
                    "Add more specific technical skills",
                    "Quantify achievements with numbers",
                    "Reorder experience section to highlight most relevant roles"
                ],
                "bullet_point_improvements": [
                    "Use action verbs to start bullet points",
                    "Include metrics and results where possible",
                    "Tailor bullet points to match job requirements"
                ]
            },
            "changes_made": {
                "added_keywords": keywords[:3],
                "reordered_sections": ["Technical Skills moved to top"],
                "improved_bullets": ["Enhanced achievement descriptions"]
            }
        }
        
        return json.dumps(mock_response)
    
    async def _mock_cover_letter_response(
        self, applicant_name: str, job_title: str, company_name: str
    ) -> str:
        """Mock response for cover letter generation when no API key is available."""
        
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background in software development and passion for innovative technology solutions, I am excited about the opportunity to contribute to your team.

My experience has equipped me with the technical skills and problem-solving abilities that align perfectly with your requirements. I have successfully worked on various projects that demonstrate my capability to deliver high-quality results while collaborating effectively with cross-functional teams.

I am particularly drawn to {company_name} because of your commitment to innovation and excellence in the industry. I believe my skills and enthusiasm would make me a valuable addition to your team, and I am eager to discuss how I can contribute to your continued success.

Thank you for considering my application. I look forward to hearing from you soon.

Sincerely,
{applicant_name}"""

    async def _mock_customized_cover_letter_response(
        self, applicant_name: str, job_title: str, company_name: str, customization: dict
    ) -> str:
        """Mock response for customized cover letter generation when no API key is available."""
        
        tone = customization.get('tone', 'professional')
        focus_areas = customization.get('focus_areas', [])
        
        # Adjust tone based on customization
        if tone == 'enthusiastic':
            opening = f"I am absolutely thrilled to apply for the {job_title} position at {company_name}!"
        elif tone == 'friendly':
            opening = f"Hi there! I'm excited to apply for the {job_title} role at {company_name}."
        elif tone == 'formal':
            opening = f"I am writing to formally express my interest in the {job_title} position at {company_name}."
        else:  # professional
            opening = f"I am writing to express my strong interest in the {job_title} position at {company_name}."
        
        # Include focus areas if specified
        focus_text = ""
        if focus_areas:
            focus_text = f"\n\nI would like to highlight my experience in: {', '.join(focus_areas)}."
        
        return f"""{opening}

With my background in software development and passion for innovative technology solutions, I am excited about the opportunity to contribute to your team.{focus_text}

My experience has equipped me with the technical skills and problem-solving abilities that align perfectly with your requirements. I have successfully worked on various projects that demonstrate my capability to deliver high-quality results while collaborating effectively with cross-functional teams.

I am particularly drawn to {company_name} because of your commitment to innovation and excellence in the industry. I believe my skills and enthusiasm would make me a valuable addition to your team, and I am eager to discuss how I can contribute to your continued success.

Thank you for considering my application. I look forward to hearing from you soon.

Sincerely,
{applicant_name}"""
