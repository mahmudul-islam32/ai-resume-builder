import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Try to import spacy, but make it optional
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("Warning: spaCy not available. Using fallback NLP methods.")

@dataclass
class AtsScoreResult:
    overall_score: float
    keyword_score: float
    semantic_score: float
    format_score: float
    experience_score: float
    keyword_analysis: Dict
    semantic_analysis: Dict
    format_analysis: Dict
    experience_analysis: Dict
    suggestions: List[str]
    improvements: Dict
    confidence: float

class AtsService:
    def __init__(self):
        # Professional ATS Keywords Database
        self.technical_skills = {
            'programming': [
                'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala',
                'typescript', 'html', 'css', 'sql', 'r', 'matlab', 'sas', 'stata', 'vba', 'powershell', 'bash'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'asp.net',
                'jquery', 'bootstrap', 'tailwind', 'material-ui', 'redux', 'vuex', 'next.js', 'nuxt.js', 'nestjs'
            ],
            'web3': [
                'web3', 'blockchain', 'ethereum', 'bitcoin', 'solidity', 'smart contract', 'defi', 'nft',
                'metamask', 'hardhat', 'truffle', 'ganache', 'ipfs', 'polygon', 'binance smart chain', 'bsc',
                'layer 2', 'rollup', 'optimism', 'arbitrum', 'uniswap', 'aave', 'compound', 'chainlink'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sql server', 'sqlite',
                'dynamodb', 'firebase', 'cassandra', 'neo4j', 'influxdb', 'couchdb', 'graphql', 'nosql'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'heroku', 'digitalocean', 'linode', 'vultr', 'cloudflare',
                'ec2', 's3', 'lambda', 'rds', 'dynamodb', 'cloudfront', 'route53', 'cloud'
            ],
            'devops': [
                'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions', 'travis ci', 'circleci',
                'terraform', 'ansible', 'chef', 'puppet', 'prometheus', 'grafana', 'elk stack', 'ci/cd'
            ],
            'data': [
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'spark', 'hadoop',
                'kafka', 'airflow', 'dbt', 'snowflake', 'databricks', 'tableau', 'power bi', 'looker'
            ]
        }
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking', 'creativity',
            'adaptability', 'time management', 'organization', 'attention to detail', 'analytical skills',
            'project management', 'collaboration', 'mentoring', 'presentation skills', 'negotiation',
            'customer service', 'sales', 'marketing', 'research', 'writing', 'public speaking',
            'agile', 'fast-paced', 'startup', 'remote', 'flexible'
        ]
        
        self.industry_keywords = {
            'software development': ['agile', 'scrum', 'sdlc', 'api', 'microservices', 'full stack', 'frontend', 'backend'],
            'data science': ['machine learning', 'ai', 'statistics', 'data analysis', 'predictive modeling', 'nlp', 'computer vision'],
            'finance': ['financial modeling', 'risk management', 'portfolio management', 'trading', 'compliance', 'audit'],
            'marketing': ['digital marketing', 'seo', 'sem', 'social media', 'content marketing', 'email marketing', 'analytics'],
            'healthcare': ['patient care', 'clinical', 'medical', 'healthcare', 'pharmaceutical', 'fda', 'hipaa'],
            'education': ['curriculum', 'teaching', 'instructional design', 'assessment', 'student', 'academic']
        }
        
        # Try to load spaCy model for advanced NLP
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
        else:
            print("Warning: spaCy not available. Using fallback NLP methods.")

    def extract_keywords(self, text: str, category: str) -> List[str]:
        """Extract keywords from text based on category using spaCy if available."""
        if self.nlp:
            return self.extract_keywords_spacy(text, category)
        else:
            return self.extract_keywords_fallback(text, category)

    def extract_keywords_fallback(self, text: str, category: str) -> List[str]:
        """Fallback keyword extraction if spaCy is not available."""
        normalized = re.sub(r'[^\w\s]', ' ', text.lower())
        words = [w for w in normalized.split() if len(w) > 2]
        
        keywords = []
        
        if category == 'required':
            keywords = [skill for skill_list in self.technical_skills.values() 
                       for skill in skill_list if skill.lower() in normalized]
        elif category == 'preferred':
            keywords = ([skill for skill_list in self.technical_skills.values() 
                        for skill in skill_list if skill.lower() in normalized] + 
                       [skill for skill in self.soft_skills if skill.lower() in normalized])
        elif category == 'industry':
            keywords = [term for term_list in self.industry_keywords.values() 
                       for term in term_list if term.lower() in normalized]
        elif category == 'soft':
            keywords = [skill for skill in self.soft_skills if skill.lower() in normalized]
        
        return list(set(keywords))

    def extract_keywords_spacy(self, text: str, category: str) -> List[str]:
        """Extract keywords using spaCy for advanced NLP analysis with better filtering."""
        if not self.nlp:
            return self.extract_keywords_fallback(text, category)
        
        doc = self.nlp(text.lower())
        keywords = []
        
        # Common words to filter out (too generic)
        common_words = {
            'experience', 'years', 'work', 'job', 'position', 'role', 'team', 'company', 
            'project', 'development', 'system', 'application', 'service', 'platform',
            'data', 'user', 'client', 'customer', 'business', 'product', 'solution',
            'technology', 'tool', 'framework', 'library', 'language', 'database',
            'api', 'web', 'mobile', 'cloud', 'server', 'client', 'frontend', 'backend',
            'full', 'stack', 'end', 'to', 'end', 'real', 'time', 'high', 'frequency',
            'scalable', 'robust', 'efficient', 'optimized', 'performance', 'quality',
            'testing', 'deployment', 'production', 'environment', 'infrastructure',
            'architecture', 'design', 'pattern', 'methodology', 'process', 'workflow',
            'collaboration', 'communication', 'leadership', 'management', 'mentoring',
            'code', 'review', 'version', 'control', 'git', 'repository', 'branch',
            'merge', 'commit', 'push', 'pull', 'request', 'issue', 'bug', 'feature',
            'requirement', 'specification', 'documentation', 'testing', 'unit', 'integration',
            'automation', 'ci', 'cd', 'pipeline', 'build', 'deploy', 'monitor', 'log',
            'error', 'exception', 'debug', 'troubleshoot', 'maintain', 'support',
            'upgrade', 'migrate', 'refactor', 'optimize', 'improve', 'enhance',
            'implement', 'develop', 'create', 'build', 'design', 'architect', 'plan',
            'analyze', 'research', 'investigate', 'evaluate', 'assess', 'review',
            'recommend', 'suggest', 'propose', 'present', 'demonstrate', 'show',
            'explain', 'document', 'write', 'read', 'understand', 'learn', 'study',
            'train', 'teach', 'mentor', 'guide', 'help', 'assist', 'support',
            'collaborate', 'work', 'coordinate', 'organize', 'manage', 'lead',
            'supervise', 'oversee', 'direct', 'control', 'monitor', 'track',
            'measure', 'evaluate', 'assess', 'analyze', 'review', 'examine',
            'investigate', 'research', 'explore', 'discover', 'identify', 'find',
            'locate', 'search', 'query', 'filter', 'sort', 'organize', 'arrange',
            'structure', 'format', 'style', 'layout', 'design', 'appearance',
            'interface', 'user', 'experience', 'usability', 'accessibility',
            'responsive', 'adaptive', 'flexible', 'dynamic', 'interactive',
            'reactive', 'proactive', 'predictive', 'intelligent', 'smart',
            'automated', 'manual', 'automatic', 'semi', 'fully', 'partially',
            'completely', 'entirely', 'wholly', 'totally', 'absolutely',
            'relatively', 'comparatively', 'similarly', 'differently',
            'uniquely', 'specially', 'particularly', 'especially',
            'specifically', 'explicitly', 'implicitly', 'directly',
            'indirectly', 'explicitly', 'implicitly', 'clearly',
            'obviously', 'apparently', 'seemingly', 'supposedly',
            'allegedly', 'reportedly', 'purportedly', 'ostensibly',
            'superficially', 'outwardly', 'externally', 'internally',
            'inherently', 'intrinsically', 'naturally', 'organically',
            'artificially', 'synthetically', 'manually', 'automatically',
            'mechanically', 'electronically', 'digitally', 'virtually',
            'physically', 'materially', 'substantially', 'significantly',
            'considerably', 'notably', 'remarkably', 'exceptionally',
            'extraordinarily', 'unusually', 'uncommonly', 'rarely',
            'seldom', 'occasionally', 'sometimes', 'often', 'frequently',
            'regularly', 'consistently', 'constantly', 'continuously',
            'persistently', 'repeatedly', 'recurrently', 'cyclically',
            'periodically', 'intermittently', 'sporadically', 'randomly',
            'arbitrarily', 'haphazardly', 'chaotically', 'systematically',
            'methodically', 'logically', 'rationally', 'reasonably',
            'sensibly', 'practically', 'realistically', 'feasibly',
            'viably', 'sustainably', 'maintainably', 'manageably',
            'controllably', 'predictably', 'reliably', 'dependably',
            'trustworthy', 'credible', 'believable', 'convincing',
            'persuasive', 'compelling', 'attractive', 'appealing',
            'desirable', 'valuable', 'beneficial', 'advantageous',
            'profitable', 'lucrative', 'rewarding', 'satisfying',
            'fulfilling', 'gratifying', 'pleasing', 'enjoyable',
            'pleasant', 'comfortable', 'convenient', 'accessible',
            'available', 'obtainable', 'attainable', 'achievable',
            'reachable', 'accessible', 'approachable', 'manageable',
            'handleable', 'controllable', 'manageable', 'treatable',
            'solvable', 'resolvable', 'fixable', 'repairable',
            'recoverable', 'restorable', 'reversible', 'undoable',
            'changeable', 'modifiable', 'adjustable', 'adaptable',
            'flexible', 'versatile', 'multipurpose', 'general',
            'universal', 'comprehensive', 'complete', 'thorough',
            'detailed', 'specific', 'precise', 'accurate', 'exact',
            'correct', 'right', 'proper', 'appropriate', 'suitable',
            'fitting', 'matching', 'compatible', 'consistent',
            'coherent', 'logical', 'rational', 'reasonable', 'sensible'
        }
        
        # Extract technical terms with better filtering
        technical_terms = []
        for token in doc:
            # Skip common words and short terms
            if (token.text.lower() in common_words or 
                len(token.text) < 3 or 
                token.is_stop or 
                token.is_punct or 
                token.is_space):
                continue
                
            # Focus on technical terms, proper nouns, and compound terms
            if (token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and 
                not token.is_stop and 
                len(token.text) > 2):
                technical_terms.append(token.text.lower())
        
        # Extract noun phrases with filtering
        noun_phrases = []
        for chunk in doc.noun_chunks:
            # Filter out generic phrases
            phrase = chunk.text.lower()
            if (len(phrase) > 2 and 
                not any(word in common_words for word in phrase.split()) and
                not phrase.startswith(('the ', 'a ', 'an ')) and
                len(phrase.split()) <= 4):  # Limit to 4 words max
                noun_phrases.append(phrase)
        
        # Extract named entities (organizations, technologies, etc.)
        entities = []
        for ent in doc.ents:
            if (ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'PERSON'] and 
                len(ent.text) > 2 and
                ent.text.lower() not in common_words):
                entities.append(ent.text.lower())
        
        # Combine all terms
        all_terms = technical_terms + noun_phrases + entities
        
        # Filter based on category with more specific matching using word boundaries
        if category == 'required':
            # Focus on exact technical skill matches with word boundaries
            keywords = []
            for term in all_terms:
                # Check if term matches any technical skill exactly or as substring
                for skill_list in self.technical_skills.values():
                    for skill in skill_list:
                        # Use word boundary matching to prevent false positives
                        if self._exact_word_match(term, skill):
                            keywords.append(skill.lower())  # Use the standardized skill name
                            break
                
                # Special case: if we find "nestjs", also add "node.js"
                if 'nestjs' in term.lower() and 'node.js' not in keywords:
                    keywords.append('node.js')
        elif category == 'preferred':
            # Include both technical and soft skills
            keywords = []
            for term in all_terms:
                # Technical skills
                for skill_list in self.technical_skills.values():
                    for skill in skill_list:
                        if self._exact_word_match(term, skill):
                            keywords.append(skill.lower())
                            break
                
                # Soft skills
                for skill in self.soft_skills:
                    if self._exact_word_match(term, skill):
                        keywords.append(skill.lower())
                        break
        elif category == 'industry':
            # Industry-specific terms
            keywords = []
            for term in all_terms:
                for term_list in self.industry_keywords.values():
                    for industry_term in term_list:
                        if self._exact_word_match(term, industry_term):
                            keywords.append(industry_term.lower())
                            break
        elif category == 'soft':
            # Soft skills only
            keywords = []
            for term in all_terms:
                for skill in self.soft_skills:
                    if self._exact_word_match(term, skill):
                        keywords.append(skill.lower())
                        break
        
        # Remove duplicates and sort
        return sorted(list(set(keywords)))

    def _exact_word_match(self, term: str, skill: str) -> bool:
        """
        Check if a term exactly matches a skill using word boundaries.
        This prevents false matches like 'r' matching 'remote'.
        
        Args:
            term: The term found in the text
            skill: The skill from the database
            
        Returns:
            True if there's an exact word match, False otherwise
        """
        term_lower = term.lower()
        skill_lower = skill.lower()
        
        # Skip single letter matches to prevent false positives
        if len(skill_lower) <= 1:
            return False
            
        # Check for exact word match using word boundaries
        import re
        
        # Pattern 1: skill is a complete word in the term
        pattern1 = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern1, term_lower):
            return True
            
        # Pattern 2: term is a complete word in the skill
        pattern2 = r'\b' + re.escape(term_lower) + r'\b'
        if re.search(pattern2, skill_lower):
            return True
            
        # Pattern 3: exact match (for multi-word skills)
        if term_lower == skill_lower:
            return True
            
        # Pattern 4: skill is part of a compound term (e.g., "vue.js" in "vue.js framework")
        if skill_lower in term_lower and len(skill_lower) > 2:
            # Make sure it's not just a partial match
            parts = term_lower.split()
            for part in parts:
                if skill_lower in part and len(part) - len(skill_lower) <= 2:
                    return True
                    
        return False

    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts using TF-IDF and cosine similarity."""
        if not text1 or not text2:
            return 0.0
        
        try:
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            # Fallback to simple word overlap
            words1 = set(re.findall(r'\b\w+\b', text1.lower()))
            words2 = set(re.findall(r'\b\w+\b', text2.lower()))
            if not words1 or not words2:
                return 0.0
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            return len(intersection) / len(union) if union else 0.0

    def detect_experience_level(self, resume_text: str) -> float:
        """Detect experience level from resume text."""
        text = resume_text.lower()
        
        # Look for years of experience
        years_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        match = re.search(years_pattern, text)
        
        if match:
            years = int(match.group(1))
            if years >= 10:
                return 100.0
            elif years >= 7:
                return 85.0
            elif years >= 5:
                return 70.0
            elif years >= 3:
                return 55.0
            elif years >= 1:
                return 40.0
        
        # Fallback: look for experience indicators
        if any(word in text for word in ['senior', 'lead', 'manager', 'director']):
            return 80.0
        elif any(word in text for word in ['mid-level', 'intermediate', 'experienced']):
            return 60.0
        elif any(word in text for word in ['junior', 'entry-level', 'graduate']):
            return 30.0
        
        return 25.0

    def analyze_format(self, resume_text: str) -> Dict:
        """Analyze resume format and structure."""
        lines = resume_text.split('\n')
        sections = ['experience', 'education', 'skills', 'summary', 'objective']
        
        # Structure score
        structure_score = sum(20 for section in sections if section in resume_text.lower())
        
        # Readability score
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        if avg_line_length > 80:
            readability_score = 60.0
        elif avg_line_length > 60:
            readability_score = 80.0
        else:
            readability_score = 100.0
        
        # Keyword density
        words = len(resume_text.split())
        technical_words = sum(1 for skill_list in self.technical_skills.values() 
                             for skill in skill_list if skill.lower() in resume_text.lower())
        keyword_density = min(100.0, (technical_words / words) * 1000) if words > 0 else 0.0
        
        # Section completeness
        has_experience = bool(re.search(r'experience|work|employment', resume_text, re.I))
        has_education = bool(re.search(r'education|degree|university|college', resume_text, re.I))
        has_skills = bool(re.search(r'skills|technologies|tools', resume_text, re.I))
        has_contact = bool(re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', resume_text, re.I))
        
        section_completeness = sum([has_experience, has_education, has_skills, has_contact]) * 25.0
        
        return {
            'structure_score': structure_score,
            'readability_score': readability_score,
            'keyword_density': keyword_density,
            'section_completeness': section_completeness
        }

    def generate_suggestions(self, resume_text: str, job_description: str, 
                           keyword_analysis: Dict, semantic_analysis: Dict, 
                           format_analysis: Dict) -> Tuple[List[str], Dict]:
        """Generate actionable suggestions for resume improvement."""
        suggestions = []
        critical = []
        important = []
        optional = []
        
        # Critical improvements
        if keyword_analysis['required']['missing']:
            missing_required = keyword_analysis['required']['missing'][:5]
            critical.append(f"Add missing required skills: {', '.join(missing_required)}")
        
        if semantic_analysis['job_title_match'] < 50:
            critical.append("Update job titles to better match the target position")
        
        if format_analysis['section_completeness'] < 75:
            critical.append("Add missing resume sections (Experience, Education, Skills, Contact)")
        
        # Important improvements
        if keyword_analysis['preferred']['missing']:
            missing_preferred = keyword_analysis['preferred']['missing'][:3]
            important.append(f"Consider adding preferred skills: {', '.join(missing_preferred)}")
        
        if format_analysis['keyword_density'] < 2:
            important.append("Increase keyword density by adding more relevant technical terms")
        
        if semantic_analysis['experience_level'] < 50:
            important.append("Highlight relevant experience and quantify achievements")
        
        # Optional improvements
        if keyword_analysis['soft_skills']['missing']:
            missing_soft = keyword_analysis['soft_skills']['missing'][:3]
            optional.append(f"Add soft skills: {', '.join(missing_soft)}")
        
        if format_analysis['readability_score'] < 80:
            optional.append("Improve readability by using shorter, more concise bullet points")
        
        suggestions = critical + important + optional
        
        return suggestions, {
            'critical': critical,
            'important': important,
            'optional': optional
        }

    def compute_ats_score(self, resume_text: str, job_description: str, 
                         job_title: str = "") -> AtsScoreResult:
        """Compute comprehensive ATS score using professional algorithms."""
        
        # Keyword Analysis
        required_keywords = self.extract_keywords(job_description, 'required')
        preferred_keywords = self.extract_keywords(job_description, 'preferred')
        industry_keywords = self.extract_keywords(job_description, 'industry')
        soft_skills = self.extract_keywords(job_description, 'soft')
        
        keyword_analysis = {
            'required': {
                'matched': [k for k in required_keywords if k.lower() in resume_text.lower()],
                'missing': [k for k in required_keywords if k.lower() not in resume_text.lower()],
                'score': 0.0
            },
            'preferred': {
                'matched': [k for k in preferred_keywords if k.lower() in resume_text.lower()],
                'missing': [k for k in preferred_keywords if k.lower() not in resume_text.lower()],
                'score': 0.0
            },
            'industry': {
                'matched': [k for k in industry_keywords if k.lower() in resume_text.lower()],
                'missing': [k for k in industry_keywords if k.lower() not in resume_text.lower()],
                'score': 0.0
            },
            'soft_skills': {
                'matched': [k for k in soft_skills if k.lower() in resume_text.lower()],
                'missing': [k for k in soft_skills if k.lower() not in resume_text.lower()],
                'score': 0.0
            }
        }
        
        # Calculate keyword scores
        keyword_analysis['required']['score'] = (
            (len(keyword_analysis['required']['matched']) / len(required_keywords)) * 100 
            if required_keywords else 100.0
        )
        keyword_analysis['preferred']['score'] = (
            (len(keyword_analysis['preferred']['matched']) / len(preferred_keywords)) * 100 
            if preferred_keywords else 100.0
        )
        keyword_analysis['industry']['score'] = (
            (len(keyword_analysis['industry']['matched']) / len(industry_keywords)) * 100 
            if industry_keywords else 100.0
        )
        keyword_analysis['soft_skills']['score'] = (
            (len(keyword_analysis['soft_skills']['matched']) / len(soft_skills)) * 100 
            if soft_skills else 100.0
        )
        
        # Semantic Analysis
        semantic_analysis = {
            'job_title_match': self.calculate_semantic_similarity(resume_text, job_title) * 100,
            'industry_alignment': keyword_analysis['industry']['score'],
            'experience_level': self.detect_experience_level(resume_text),
            'responsibility_match': self.calculate_semantic_similarity(resume_text, job_description) * 100
        }
        
        # Format Analysis
        format_analysis = self.analyze_format(resume_text)
        
        # Experience Analysis
        experience_analysis = {
            'years_of_experience': self.detect_experience_level(resume_text),
            'relevant_experience': semantic_analysis['responsibility_match'],
            'project_match': self.calculate_semantic_similarity(resume_text, job_description) * 100,
            'achievement_alignment': semantic_analysis['responsibility_match']
        }
        
        # Calculate component scores
        keyword_score = (
            keyword_analysis['required']['score'] * 0.5 + 
            keyword_analysis['preferred']['score'] * 0.3 + 
            keyword_analysis['industry']['score'] * 0.2
        )
        
        semantic_score = (
            semantic_analysis['job_title_match'] * 0.3 + 
            semantic_analysis['industry_alignment'] * 0.3 + 
            semantic_analysis['experience_level'] * 0.2 + 
            semantic_analysis['responsibility_match'] * 0.2
        )
        
        format_score = (
            format_analysis['structure_score'] * 0.3 + 
            format_analysis['readability_score'] * 0.3 + 
            format_analysis['keyword_density'] * 0.2 + 
            format_analysis['section_completeness'] * 0.2
        )
        
        experience_score = (
            experience_analysis['relevant_experience'] * 0.4 + 
            experience_analysis['project_match'] * 0.3 + 
            experience_analysis['achievement_alignment'] * 0.3
        )
        
        # Overall score (weighted average)
        overall_score = (
            keyword_score * 0.35 + 
            semantic_score * 0.25 + 
            format_score * 0.20 + 
            experience_score * 0.20
        )
        
        # Generate suggestions
        suggestions, improvements = self.generate_suggestions(
            resume_text, job_description, keyword_analysis, semantic_analysis, format_analysis
        )
        
        # Calculate confidence based on data quality
        confidence = min(100.0, 
            (len(resume_text) / 1000) * 30 + 
            (len(job_description) / 1000) * 30 + 
            (len(keyword_analysis['required']['matched']) + len(keyword_analysis['preferred']['matched'])) * 2
        )
        
        return AtsScoreResult(
            overall_score=round(overall_score, 1),
            keyword_score=round(keyword_score, 1),
            semantic_score=round(semantic_score, 1),
            format_score=round(format_score, 1),
            experience_score=round(experience_score, 1),
            keyword_analysis=keyword_analysis,
            semantic_analysis=semantic_analysis,
            format_analysis=format_analysis,
            experience_analysis=experience_analysis,
            suggestions=suggestions,
            improvements=improvements,
            confidence=round(confidence, 1)
        )
