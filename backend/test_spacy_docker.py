#!/usr/bin/env python3
"""
Test script to verify spaCy integration in Docker environment.
Run this inside the Docker container to test NLP capabilities.
"""

import sys
import os

def test_spacy_installation():
    """Test if spaCy is properly installed and models are available."""
    print("Testing spaCy installation...")
    
    try:
        import spacy
        print(f"✓ spaCy version: {spacy.__version__}")
    except ImportError as e:
        print(f"✗ spaCy import failed: {e}")
        return False
    
    # Test model loading
    models_to_test = ["en_core_web_md", "en_core_web_sm"]
    
    for model_name in models_to_test:
        try:
            nlp = spacy.load(model_name)
            print(f"✓ {model_name} model loaded successfully")
            
            # Test basic NLP functionality
            doc = nlp("Python developer with 5 years of experience in machine learning.")
            print(f"  - Tokens: {len(doc)}")
            print(f"  - Entities: {[(ent.text, ent.label_) for ent in doc.ents]}")
            print(f"  - Noun chunks: {[chunk.text for chunk in doc.noun_chunks]}")
            
        except OSError as e:
            print(f"✗ {model_name} model not found: {e}")
    
    return True

def test_ats_service():
    """Test the ATS service with spaCy integration."""
    print("\nTesting ATS service with spaCy...")
    
    try:
        from app.services.ats_service import AtsService
        
        # Create ATS service instance
        ats = AtsService()
        
        # Test resume and job description
        resume_text = """John Doe
Software Engineer

EXPERIENCE
Senior Software Engineer at Tech Corp (2020-2023)
- Developed web applications using Python and JavaScript
- Led team of 3 developers
- Improved application performance by 40%
- Managed AWS infrastructure and Docker containers

SKILLS
Python, JavaScript, React, Django, Node.js, SQL, Git, AWS, Docker"""

        job_description = """We are looking for a Senior Software Engineer with 5+ years of experience in Python and JavaScript. The ideal candidate should have experience with React, Django, and Node.js. Responsibilities include developing web applications, leading development teams, and optimizing application performance. Experience with AWS and Docker is preferred."""

        print("Computing ATS score...")
        result = ats.compute_ats_score(resume_text, job_description, 'Senior Software Engineer')
        
        print(f"✓ ATS scoring completed successfully!")
        print(f"  - Overall Score: {result.overall_score}")
        print(f"  - Keyword Score: {result.keyword_score}")
        print(f"  - Semantic Score: {result.semantic_score}")
        print(f"  - Format Score: {result.format_score}")
        print(f"  - Experience Score: {result.experience_score}")
        print(f"  - Confidence: {result.confidence}")
        
        # Test spaCy-specific features
        if ats.nlp:
            print(f"✓ spaCy model loaded: {ats.nlp.meta.get('name', 'Unknown')}")
            
            # Test keyword extraction
            keywords = ats.extract_keywords(job_description, 'required')
            print(f"  - Extracted required keywords: {keywords[:5]}...")
            
            # Test semantic similarity
            similarity = ats.calculate_semantic_similarity(resume_text, job_description)
            print(f"  - Semantic similarity: {similarity:.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ ATS service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("spaCy Docker Integration Test")
    print("=" * 60)
    
    # Test spaCy installation
    spacy_ok = test_spacy_installation()
    
    # Test ATS service
    ats_ok = test_ats_service()
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    print(f"spaCy Installation: {'✓ PASS' if spacy_ok else '✗ FAIL'}")
    print(f"ATS Service: {'✓ PASS' if ats_ok else '✗ FAIL'}")
    
    if spacy_ok and ats_ok:
        print("\n🎉 All tests passed! spaCy integration is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
