# spaCy Docker Setup Guide

This guide explains how to set up and use spaCy for advanced Natural Language Processing (NLP) in your AI Resume application using Docker.

## Overview

Your ATS (Applicant Tracking System) service now includes advanced NLP capabilities powered by spaCy, providing:

- **Enhanced Keyword Extraction**: Better identification of technical skills, proper nouns, and named entities
- **Improved Semantic Similarity**: More accurate text similarity using spaCy's word vectors
- **Advanced Text Analysis**: Better experience level detection and format analysis
- **Fallback Support**: Graceful degradation when spaCy is not available

## Docker Setup

### 1. Updated Dockerfile

The main `Dockerfile` now includes:

```dockerfile
# Install spaCy models (medium model for better NLP capabilities)
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_md
```

### 2. spaCy Models

Two spaCy models are installed:

- **`en_core_web_md`** (Medium): Primary model with word vectors for better semantic similarity
- **`en_core_web_sm`** (Small): Fallback model for faster processing

### 3. Running with Docker

```bash
# Build and start all services
docker-compose up --build

# Or build just the backend
docker-compose build backend
docker-compose up backend
```

## ATS Service Enhancements

### 1. Enhanced Keyword Extraction

The ATS service now uses spaCy for better keyword extraction:

```python
def extract_keywords_spacy(self, text: str, category: str) -> List[str]:
    """Extract keywords using spaCy for advanced NLP analysis."""
    doc = self.nlp(text.lower())
    
    # Extract technical terms, proper nouns, and important phrases
    technical_terms = []
    for token in doc:
        if (token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2):
            technical_terms.append(token.text.lower())
    
    # Extract noun phrases
    noun_phrases = [chunk.text.lower() for chunk in doc.noun_chunks]
    
    # Extract named entities
    entities = [ent.text.lower() for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'GPE']]
```

### 2. Improved Semantic Similarity

```python
def calculate_semantic_similarity_spacy(self, text1: str, text2: str) -> float:
    """Calculate semantic similarity using spaCy's built-in similarity."""
    doc1 = self.nlp(text1)
    doc2 = self.nlp(text2)
    similarity = doc1.similarity(doc2)
    return float(similarity)
```

### 3. Advanced Experience Level Detection

```python
def detect_experience_level_spacy(self, resume_text: str) -> float:
    """Detect experience level using spaCy for better text analysis."""
    doc = self.nlp(resume_text.lower())
    
    # Analyze job titles and responsibilities using spaCy
    senior_indicators = ['managed', 'led', 'supervised', 'mentored', 'architected']
    mid_indicators = ['developed', 'implemented', 'created', 'built', 'maintained']
    junior_indicators = ['assisted', 'helped', 'supported', 'learned', 'trained']
```

## Testing spaCy Integration

### 1. Test Script

Run the test script inside the Docker container:

```bash
# Enter the backend container
docker-compose exec backend bash

# Run the spaCy test
python test_spacy_docker.py
```

### 2. Expected Output

```
============================================================
spaCy Docker Integration Test
============================================================
Testing spaCy installation...
✓ spaCy version: 3.7.2
✓ en_core_web_md model loaded successfully
  - Tokens: 8
  - Entities: [('Python', 'PRODUCT')]
  - Noun chunks: ['Python developer', '5 years', 'experience', 'machine learning']

Testing ATS service with spaCy...
spaCy medium model (en_core_web_md) loaded successfully for advanced NLP features
Computing ATS score...
✓ ATS scoring completed successfully!
  - Overall Score: 78.5
  - Keyword Score: 85.2
  - Semantic Score: 82.1
  - Format Score: 75.0
  - Experience Score: 70.0
  - Confidence: 78.9
✓ spaCy model loaded: en_core_web_md
  - Extracted required keywords: ['python', 'javascript', 'react', 'django', 'node.js']...
  - Semantic similarity: 0.823

============================================================
Test Results Summary:
============================================================
spaCy Installation: ✓ PASS
ATS Service: ✓ PASS

🎉 All tests passed! spaCy integration is working correctly.
```

## API Endpoints

### Test ATS Scoring (No Authentication Required)

```bash
curl -X POST "http://localhost:8000/api/v1/ats/test-score" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSoftware Engineer\n\nEXPERIENCE\nSenior Software Engineer at Tech Corp (2020-2023)\n- Developed web applications using Python and JavaScript\n- Led team of 3 developers\n- Improved application performance by 40%\n\nSKILLS\nPython, JavaScript, React, Django, Node.js, SQL, Git",
    "job_description": "We are looking for a Senior Software Engineer with 5+ years of experience in Python and JavaScript. The ideal candidate should have experience with React, Django, and Node.js. Responsibilities include developing web applications, leading development teams, and optimizing application performance.",
    "job_title": "Senior Software Engineer"
  }'
```

### Authenticated ATS Scoring

```bash
curl -X POST "http://localhost:8000/api/v1/ats/score-resume" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "resume_id": 1,
    "job_posting_id": 1
  }'
```

## Performance Considerations

### 1. Model Loading

- **Medium Model (`en_core_web_md`)**: ~40MB, better semantic similarity
- **Small Model (`en_core_web_sm`)**: ~12MB, faster processing
- **Fallback**: Uses TF-IDF and cosine similarity

### 2. Memory Usage

- spaCy models are loaded once when the service starts
- Each text processing operation uses additional memory
- Consider monitoring memory usage in production

### 3. Processing Speed

- spaCy processing is slower than simple regex matching
- The service includes fallback methods for better performance
- Consider caching results for repeated analyses

## Troubleshooting

### 1. spaCy Model Not Found

If you see warnings about spaCy models not being found:

```bash
# Inside the Docker container
docker-compose exec backend bash

# Install models manually
python -m spacy download en_core_web_md
python -m spacy download en_core_web_sm
```

### 2. Memory Issues

If you encounter memory issues:

```bash
# Use the simple Dockerfile instead
docker-compose -f docker-compose.yml up backend
```

### 3. Performance Issues

For better performance in production:

1. Use the small model only: `en_core_web_sm`
2. Implement caching for repeated analyses
3. Consider using async processing for large volumes

## Configuration

### Environment Variables

No additional environment variables are required for spaCy. The service automatically:

1. Detects if spaCy is available
2. Loads the best available model
3. Falls back to simpler methods if needed

### Customization

To customize spaCy behavior, modify the ATS service:

```python
# In ats_service.py
class AtsService:
    def __init__(self):
        # Customize spaCy pipeline
        if SPACY_AVAILABLE:
            self.nlp = spacy.load("en_core_web_md", disable=['ner'])  # Disable NER for speed
```

## Benefits of spaCy Integration

1. **Better Keyword Extraction**: Identifies technical terms, proper nouns, and named entities
2. **Improved Semantic Similarity**: Uses word vectors for more accurate text similarity
3. **Enhanced Experience Detection**: Better analysis of job titles and responsibilities
4. **Robust Fallback**: Graceful degradation when spaCy is not available
5. **Professional NLP**: Industry-standard natural language processing

## Next Steps

1. **Test the Integration**: Run the test script to verify everything works
2. **Monitor Performance**: Check memory usage and processing speed
3. **Customize Models**: Add domain-specific vocabulary if needed
4. **Scale Up**: Consider using larger models for production use

For more information about spaCy, visit: https://spacy.io/
