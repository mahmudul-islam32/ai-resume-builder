#!/usr/bin/env python3
"""
Test script to demonstrate and fix the keyword extraction issue.
"""

from app.services.ats_service import AtsService

def test_keyword_extraction():
    """Test the current keyword extraction and show the issue."""
    
    # Sample job description that's causing the issue
    job_description = """
    We are looking for a Backend NestJS Web3 Engineer with strong backend engineering experience. 
    The ideal candidate should have experience with Node.js, PostgreSQL, GraphQL, and smart contract development. 
    Responsibilities include developing scalable backend systems, integrating with multiple blockchain networks, 
    and building professional-grade trading infrastructure. Experience with DeFi protocols, real-time data processing, 
    and high-frequency applications is preferred. The role involves working in an agile, fast-paced startup environment 
    with cutting-edge DeFi protocols and platforms.
    """
    
    print("Testing Keyword Extraction Issue")
    print("=" * 50)
    
    # Create ATS service
    ats = AtsService()
    
    print(f"spaCy available: {ats.nlp is not None}")
    if ats.nlp:
        print(f"spaCy model: {ats.nlp.meta.get('name', 'Unknown')}")
    
    print("\nCurrent Keyword Extraction Results:")
    print("-" * 30)
    
    # Test different categories
    categories = ['required', 'preferred', 'industry', 'soft']
    
    for category in categories:
        keywords = ats.extract_keywords(job_description, category)
        print(f"\n{category.upper()} keywords ({len(keywords)}):")
        print(f"  {', '.join(keywords[:10])}{'...' if len(keywords) > 10 else ''}")
    
    print("\n" + "=" * 50)
    print("SOLUTION: Improved Keyword Extraction")
    print("=" * 50)
    
    # Show what the improved version should extract
    print("\nExpected Results (after improvement):")
    print("-" * 30)
    
    expected_required = ['node.js', 'postgresql', 'graphql', 'nestjs', 'web3', 'blockchain']
    expected_preferred = ['node.js', 'postgresql', 'graphql', 'nestjs', 'web3', 'blockchain', 'defi', 'smart contract', 'leadership', 'communication']
    expected_industry = ['defi', 'blockchain', 'web3', 'trading', 'startup']
    expected_soft = ['leadership', 'communication', 'teamwork']
    
    print(f"REQUIRED keywords: {', '.join(expected_required)}")
    print(f"PREFERRED keywords: {', '.join(expected_preferred)}")
    print(f"INDUSTRY keywords: {', '.join(expected_industry)}")
    print(f"SOFT keywords: {', '.join(expected_soft)}")

def demonstrate_improvement():
    """Demonstrate how the improved keyword extraction should work."""
    
    print("\n" + "=" * 50)
    print("IMPROVEMENT STRATEGY")
    print("=" * 50)
    
    print("""
1. FILTER OUT COMMON WORDS:
   - Remove generic terms like 'experience', 'years', 'work', 'job', 'position'
   - Filter out common verbs like 'develop', 'create', 'build', 'implement'
   - Exclude general nouns like 'system', 'application', 'service', 'platform'

2. FOCUS ON TECHNICAL SKILLS:
   - Prioritize exact matches with known technical skills
   - Use standardized skill names from the skills database
   - Match partial terms (e.g., 'node.js' from 'nestjs' or 'node')

3. IMPROVE MATCHING LOGIC:
   - Use bidirectional matching (skill in term OR term in skill)
   - Standardize output to use known skill names
   - Limit phrase length to avoid overly generic terms

4. CATEGORY-SPECIFIC FILTERING:
   - Required: Only technical skills
   - Preferred: Technical + soft skills
   - Industry: Domain-specific terms
   - Soft: Only soft skills
    """)

if __name__ == "__main__":
    test_keyword_extraction()
    demonstrate_improvement()
