import PyPDF2
import docx
from typing import Tuple, Dict, Any
import re
import json


async def parse_resume(file_path: str, file_type: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parse resume file and extract content and structured data.
    
    Args:
        file_path: Path to the resume file
        file_type: File extension (pdf or docx)
    
    Returns:
        Tuple of (parsed_content, extracted_data)
    """
    
    if file_type.lower() == 'pdf':
        content = await parse_pdf(file_path)
    elif file_type.lower() == 'docx':
        content = await parse_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Extract structured data
    extracted_data = await extract_resume_data(content)
    
    return content, extracted_data


async def parse_pdf(file_path: str) -> str:
    """Extract text content from PDF file."""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            content = ""
            
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
                
        return content.strip()
    except Exception as e:
        raise Exception(f"Failed to parse PDF: {str(e)}")


async def parse_docx(file_path: str) -> str:
    """Extract text content from DOCX file."""
    try:
        doc = docx.Document(file_path)
        content = ""
        
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
            
        return content.strip()
    except Exception as e:
        raise Exception(f"Failed to parse DOCX: {str(e)}")


async def extract_resume_data(content: str) -> Dict[str, Any]:
    """
    Extract structured data from resume content.
    This is a basic implementation - in production, you'd use more sophisticated NLP.
    """
    
    extracted_data = {
        "contact_info": {},
        "skills": [],
        "experience": [],
        "education": [],
        "keywords": []
    }
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, content)
    if emails:
        extracted_data["contact_info"]["email"] = emails[0]
    
    # Extract phone numbers
    phone_pattern = r'(\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})'
    phones = re.findall(phone_pattern, content)
    if phones:
        extracted_data["contact_info"]["phone"] = phones[0]
    
    # Extract common skills (basic keyword matching)
    common_skills = [
        'python', 'javascript', 'java', 'c++', 'react', 'node.js', 'sql',
        'aws', 'docker', 'kubernetes', 'git', 'machine learning', 'ai',
        'data analysis', 'project management', 'leadership', 'communication'
    ]
    
    content_lower = content.lower()
    found_skills = []
    for skill in common_skills:
        if skill in content_lower:
            found_skills.append(skill)
    
    extracted_data["skills"] = found_skills
    
    # Extract keywords (simple word frequency)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
    word_freq = {}
    for word in words:
        if word not in ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'man', 'put', 'say', 'she', 'too', 'use']:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top keywords
    top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
    extracted_data["keywords"] = [word for word, freq in top_keywords]
    
    return extracted_data
