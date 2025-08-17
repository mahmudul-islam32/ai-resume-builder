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
    """Extract job description from HTML."""
    
    description_selectors = [
        '#jobDescriptionText',  # Indeed
        '[data-automation-id="jobPostingDescription"]',  # Workday
        '.job-description',
        '.description',
        '.posting-description',
        '.job-details'
    ]
    
    for selector in description_selectors:
        element = soup.select_one(selector)
        if element:
            return clean_text(element.get_text(separator='\n', strip=True))
    
    # Fallback: get all paragraph text
    paragraphs = soup.find_all('p')
    if paragraphs:
        description = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        if len(description) > 100:  # Only return if substantial content
            return clean_text(description)
    
    return "No description available"


def extract_requirements(soup: BeautifulSoup) -> Optional[str]:
    """Extract job requirements from HTML."""
    
    # Look for sections that might contain requirements
    requirement_keywords = ['requirements', 'qualifications', 'skills', 'experience']
    
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
                    content.extend([item.get_text(strip=True) for item in items])
                elif next_element.name == 'p':
                    text = next_element.get_text(strip=True)
                    if text:
                        content.append(text)
                
                next_element = next_element.find_next_sibling()
            
            if content:
                return clean_text('\n'.join(content))
    
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
