#!/usr/bin/env python3
"""
Test script for the simple ATS service (without spaCy)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ats_service_simple import AtsServiceSimple

def test_simple_ats_service():
    """Test the simple ATS service with sample data"""
    
    # Sample resume text
    resume_text = """
    SOFTWARE ENGINEER
    
    EXPERIENCE
    Senior Software Engineer | TechCorp | 2020-2023
    - Developed and maintained Python-based web applications using Django and Flask
    - Implemented REST APIs and microservices architecture
    - Used PostgreSQL and Redis for data storage and caching
    - Deployed applications using Docker and AWS (EC2, S3, Lambda)
    - Collaborated with cross-functional teams using Agile methodologies
    
    Software Developer | StartupXYZ | 2018-2020
    - Built frontend applications using React and JavaScript
    - Worked with Node.js and Express for backend development
    - Integrated third-party APIs and payment systems
    - Used Git for version control and CI/CD pipelines
    
    EDUCATION
    Bachelor of Science in Computer Science | University of Technology | 2018
    
    SKILLS
    Programming: Python, JavaScript, SQL, HTML, CSS
    Frameworks: Django, Flask, React, Node.js, Express
    Databases: PostgreSQL, Redis, MySQL
    Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
    Tools: Git, Jenkins, JIRA, Agile/Scrum
    """
    
    # Sample job description
    job_description = """
    Senior Software Engineer
    
    We are looking for a Senior Software Engineer to join our team. You will be responsible for developing scalable web applications and APIs.
    
    Requirements:
    - 5+ years of experience in software development
    - Strong proficiency in Python and JavaScript
    - Experience with Django, Flask, or similar frameworks
    - Knowledge of PostgreSQL and Redis
    - Experience with AWS cloud services
    - Familiarity with Docker and containerization
    - Experience with REST APIs and microservices
    - Strong problem-solving and communication skills
    
    Preferred:
    - Experience with React or similar frontend frameworks
    - Knowledge of Kubernetes and orchestration
    - Experience with CI/CD pipelines
    - Understanding of Agile methodologies
    - Experience with payment system integrations
    """
    
    # Initialize ATS service
    print("Initializing Simple ATS service...")
    ats_service = AtsServiceSimple()
    
    # Compute ATS score
    print("Computing ATS score...")
    result = ats_service.compute_ats_score(resume_text, job_description, "Senior Software Engineer")
    
    # Display results
    print("\n" + "="*50)
    print("SIMPLE ATS SCORE RESULTS")
    print("="*50)
    
    print(f"Overall Score: {result.overall_score}%")
    print(f"Keyword Score: {result.keyword_score}%")
    print(f"Semantic Score: {result.semantic_score}%")
    print(f"Format Score: {result.format_score}%")
    print(f"Experience Score: {result.experience_score}%")
    print(f"Confidence: {result.confidence}%")
    
    print("\n" + "-"*30)
    print("KEYWORD ANALYSIS")
    print("-"*30)
    
    print("Required Keywords:")
    print(f"  Matched: {result.keyword_analysis['required']['matched']}")
    print(f"  Missing: {result.keyword_analysis['required']['missing']}")
    print(f"  Score: {result.keyword_analysis['required']['score']}%")
    
    print("\nPreferred Keywords:")
    print(f"  Matched: {result.keyword_analysis['preferred']['matched']}")
    print(f"  Missing: {result.keyword_analysis['preferred']['missing']}")
    print(f"  Score: {result.keyword_analysis['preferred']['score']}%")
    
    print("\n" + "-"*30)
    print("SEMANTIC ANALYSIS")
    print("-"*30)
    
    print(f"Job Title Match: {result.semantic_analysis['job_title_match']}%")
    print(f"Industry Alignment: {result.semantic_analysis['industry_alignment']}%")
    print(f"Experience Level: {result.semantic_analysis['experience_level']}%")
    print(f"Responsibility Match: {result.semantic_analysis['responsibility_match']}%")
    
    print("\n" + "-"*30)
    print("FORMAT ANALYSIS")
    print("-"*30)
    
    print(f"Structure Score: {result.format_analysis['structure_score']}%")
    print(f"Readability Score: {result.format_analysis['readability_score']}%")
    print(f"Keyword Density: {result.format_analysis['keyword_density']}%")
    print(f"Section Completeness: {result.format_analysis['section_completeness']}%")
    
    print("\n" + "-"*30)
    print("IMPROVEMENT SUGGESTIONS")
    print("-"*30)
    
    if result.improvements['critical']:
        print("Critical Improvements:")
        for suggestion in result.improvements['critical']:
            print(f"  • {suggestion}")
    
    if result.improvements['important']:
        print("\nImportant Improvements:")
        for suggestion in result.improvements['important']:
            print(f"  • {suggestion}")
    
    if result.improvements['optional']:
        print("\nOptional Improvements:")
        for suggestion in result.improvements['optional']:
            print(f"  • {suggestion}")
    
    print("\n" + "="*50)
    print("Simple ATS service test completed successfully!")
    print("="*50)

if __name__ == "__main__":
    test_simple_ats_service()
