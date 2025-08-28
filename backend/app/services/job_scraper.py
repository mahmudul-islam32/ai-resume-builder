import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import re
from urllib.parse import urljoin, urlparse


async def scrape_job_posting(url: str) -> Dict[str, Any]:
    """
    Scrape job posting data from a given URL.
    
    Args:
        url: Job posting URL
        
    Returns:
        Dictionary containing scraped job data
    """
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract job data based on common patterns
        scraped_data = {
            "title": extract_job_title(soup),
            "company": extract_company_name(soup),
            "description": extract_job_description(soup),
            "requirements": extract_requirements(soup),
            "location": extract_location(soup),
            "salary_range": extract_salary(soup),
            "keywords": extract_keywords(soup)
        }
        
        return scraped_data
        
    except Exception as e:
        raise Exception(f"Failed to scrape job posting: {str(e)}")


def extract_job_title(soup: BeautifulSoup) -> str:
    """Extract job title from HTML."""
    
    # Common selectors for job titles
    title_selectors = [
        'h1.jobsearch-JobInfoHeader-title',  # Indeed
        'h1[data-automation-id="jobPostingHeader"]',  # Workday
        'h1.job-title',
        'h1.posting-headline',
        '.job-title h1',
        'h1',
        'title'
    ]
    
    for selector in title_selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            return clean_text(element.get_text(strip=True))
    
    # Fallback to page title
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        # Remove common suffixes
        title = re.sub(r'\s*[-|]\s*(Indeed\.com|LinkedIn|Glassdoor|Monster).*$', '', title, flags=re.IGNORECASE)
        return clean_text(title)
    
    return "Unknown Position"


def extract_company_name(soup: BeautifulSoup) -> str:
    """Extract company name from HTML."""
    
    company_selectors = [
        '[data-testid="inlineHeader-companyName"]',  # Indeed
        '[data-automation-id="jobPostingCompany"]',  # Workday
        '.company-name',
        '.employer-name',
        '.job-company',
        'span.company'
    ]
    
    for selector in company_selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            return clean_text(element.get_text(strip=True))
    
    return "Unknown Company"


def extract_job_description(soup: BeautifulSoup) -> str:
    """Extract job description from HTML with improved formatting preservation."""
    
    description_selectors = [
        '#jobDescriptionText',  # Indeed
        '[data-automation-id="jobPostingDescription"]',  # Workday
        '.job-description',
        '.description',
        '.posting-description',
        '.job-details',
        '.job-description-container',
        '.job-posting-description'
    ]
    
    for selector in description_selectors:
        element = soup.select_one(selector)
        if element:
            return clean_and_format_text(element)
    
    # Fallback: get all paragraph text with better formatting
    paragraphs = soup.find_all(['p', 'div', 'section'])
    if paragraphs:
        description_parts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 10:  # Only include substantial content
                description_parts.append(text)
        
        if description_parts:
            return clean_and_format_text('\n\n'.join(description_parts))
    
    return "No description available"


def extract_requirements(soup: BeautifulSoup) -> Optional[str]:
    """Extract job requirements from HTML with improved formatting."""
    
    # Look for sections that might contain requirements
    requirement_keywords = ['requirements', 'qualifications', 'skills', 'experience', 'what you bring', 'what we expect', 'was du mitbringst']
    
    for keyword in requirement_keywords:
        # Find headers containing the keyword
        headers = soup.find_all(['h2', 'h3', 'h4', 'strong', 'b'], string=re.compile(keyword, re.IGNORECASE))
        
        for header in headers:
            # Get the next sibling elements that might contain the requirements
            content = []
            next_element = header.find_next_sibling()
            
            while next_element and next_element.name not in ['h1', 'h2', 'h3']:
                if next_element.name in ['ul', 'ol']:
                    items = next_element.find_all('li')
                    for item in items:
                        text = item.get_text(strip=True)
                        if text:
                            content.append(f"• {text}")
                elif next_element.name == 'p':
                    text = next_element.get_text(strip=True)
                    if text:
                        content.append(text)
                
                next_element = next_element.find_next_sibling()
            
            if content:
                return clean_and_format_text('\n'.join(content))
    
    return None


def extract_location(soup: BeautifulSoup) -> Optional[str]:
    """Extract job location from HTML."""
    
    location_selectors = [
        '[data-testid="job-location"]',  # Indeed
        '[data-automation-id="jobPostingLocation"]',  # Workday
        '.job-location',
        '.location',
        '.workplace-type'
    ]
    
    for selector in location_selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            return clean_text(element.get_text(strip=True))
    
    return None


def extract_salary(soup: BeautifulSoup) -> Optional[str]:
    """Extract salary information from HTML."""
    
    salary_selectors = [
        '.salary-snippet',
        '.salary',
        '[data-testid="job-salary"]',
        '.compensation'
    ]
    
    for selector in salary_selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            return clean_text(element.get_text(strip=True))
    
    # Look for salary patterns in text
    salary_pattern = r'\$[\d,]+(?:\s*[-–]\s*\$[\d,]+)?(?:\s*(?:per|/)\s*(?:year|hour|month))?'
    all_text = soup.get_text()
    salary_matches = re.findall(salary_pattern, all_text, re.IGNORECASE)
    
    if salary_matches:
        return salary_matches[0]
    
    return None


def extract_keywords(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract relevant keywords from job posting."""
    
    text = soup.get_text().lower()
    
    # Common tech skills and keywords
    tech_skills = [
        'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
        'git', 'github', 'gitlab', 'agile', 'scrum',
        'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch'
    ]
    
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem solving',
        'project management', 'critical thinking', 'creativity'
    ]
    
    found_tech_skills = [skill for skill in tech_skills if skill in text]
    found_soft_skills = [skill for skill in soft_skills if skill in text]
    
    return {
        "tech_skills": found_tech_skills,
        "soft_skills": found_soft_skills,
        "total_keywords": found_tech_skills + found_soft_skills
    }


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,;:()$%/]', '', text)
    
    return text.strip()


def clean_and_format_text(element) -> str:
    """
    Clean and format text while preserving structure and readability.
    Enhanced for German job postings.
    
    Args:
        element: BeautifulSoup element or string
        
    Returns:
        Formatted text string
    """
    if isinstance(element, str):
        text = element
    else:
        # Get text with proper separators
        text = element.get_text(separator='\n', strip=True)
    
    if not text:
        return ""
    
    # Split into lines and clean each line
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Clean the line
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Remove excessive whitespace within the line
        line = re.sub(r'\s+', ' ', line)
        
        # Clean special characters but preserve important ones
        line = re.sub(r'[^\w\s\-.,;:()$%/\n]', '', line)
        
        cleaned_lines.append(line)
    
    # Join lines with proper spacing
    formatted_text = '\n'.join(cleaned_lines)
    
    # Add extra spacing around section headers (lines that end with :)
    formatted_text = re.sub(r'([^:]+:)\n', r'\1\n\n', formatted_text)
    
    # Add spacing around bullet points
    formatted_text = re.sub(r'\n(•|\*|\-)\s*', r'\n\n\1 ', formatted_text)
    
    # Handle German job posting specific formatting
    # Add spacing after common German section headers
    german_headers = [
        r'Was Du Bei Uns Bewegst',
        r'Was Du Mitbringst', 
        r'Was Wir Dir Bieten',
        r'Ansprechpartner',
        r'Über uns',
        r'Ziel der Stelle',
        r'Gehaltsspanne',
        r'Vollzeit',
        r'hybrid',
        r'mit Berufserfahrung'
    ]
    
    for header in german_headers:
        formatted_text = re.sub(f'({header})', r'\1\n', formatted_text, flags=re.IGNORECASE)
    
    # Add bullet points for lines that start with "Du" (common in German job postings)
    formatted_text = re.sub(r'\n(Du [^.]*\.)', r'\n• \1', formatted_text)
    
    # Add bullet points for lines that start with common German patterns
    german_bullet_patterns = [
        r'Abgeschlossenes Studium',
        r'Fundierte Erfahrung',
        r'Sicherer Umgang',
        r'Sehr gute Deutsch',
        r'Teamgeist',
        r'Erfahrungen mit',
        r'Faires und transparentes Gehalt',
        r'Hybrides Arbeiten',
        r'Gleitzeit',
        r'30 Tage Urlaub',
        r'Mobilitäts- und Gesundheitszuschüsse',
        r'Modernes Büro',
        r'Community-Events'
    ]
    
    for pattern in german_bullet_patterns:
        formatted_text = re.sub(f'\\n({pattern})', r'\n• \1', formatted_text, flags=re.IGNORECASE)
    
    # Clean up multiple consecutive newlines
    formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text)
    
    return formatted_text.strip()
