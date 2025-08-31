#!/usr/bin/env python3
"""
Test script to demonstrate the ATS keyword extraction issue with the German job posting.
"""

from app.services.ats_service import AtsService

def test_german_job_posting():
    """Test the ATS keyword extraction with the German job posting."""
    
    # The German job posting from the user
    german_job_description = """
    Willkommen bei Giffits Herzlich willkommen bei Giffits dem Ort, wo wir mit Leidenschaft daran arbeiten, unsere Kunden mit hochwertigen Werbeartikeln zu begeistern und ihnen den Weg dorthin so unkompliziert wie möglich zu gestalten. Von Vertrieb über IT-Entwicklung bis hin zum Webdesign setzen wir alles daran, dieses Ziel zu verwirklichen. In diesem Prozess entstehen bei uns die faszinierendsten interdisziplinären Projekte. Um unseren Kunden eine erstklassige Beratung zu bieten, brauchen wir genau deine Expertise und Unterstützung Fühlst du dich bereit, Teil einer Erfolgsgeschichte im E-Commerce zu sein Dann zögere nicht und bewirb dich bei uns lass uns gemeinsam Großes erreichen Ziel der Stelle Du möchtest nicht nur Code schreiben, sondern echte Mehrwerte schaffen Als Fullstack Software Engineer (m/w/d) unterstützt du unser Entwicklungsteam dabei, unsere Webshop- und internen Systeme zukunftsfähig zu gestalten mit modernsten Technologien, durchdachten Architekturen und einem klaren Fokus auf Benutzerfreundlichkeit und Skalierbarkeit. Was erwartet dich Du entwickelst neue Funktionen für unseren Webshop und interne Systeme und bringst deine Ideen aktiv ein. Du verbesserst bestehende Anwendungen in enger Zusammenarbeit mit Marketing, internen Stakeholdern und anderen Entwicklern. Du hilfst dabei, unsere Legacy-Systeme weiterzuentwickeln oder abzulösen und bringst moderne Ansätze ein. Du gestaltest unsere Softwarelandschaft aktiv mit, indem du dich in Themen wie Microservices, Cloud-Architekturen oder serverlose Anwendungen einarbeitest. Du schreibst sauberen, wartbaren Code, erstellst Dokumentationen und stellst mit Tests sowie automatisierten Deployments eine hohe Qualität sicher. Was bringst du mit Du hast mehrjährige Erfahrung in der Softwareentwicklung und ein starkes Verständnis moderner Technologien. Du hast praktische Erfahrung mit Node.js und modernen Frontend-Frameworks wie Vue.js oder vergleichbar. Du bewegst dich sicher in SQL- und NoSQL-Datenbanken und legst Wert auf sauberen, wartbaren Code, der auch im Team gut verständlich ist Du arbeitest gerne agil, verstehst CI/CD-Prozesse und hast keine Scheu vor Legacy-Code. Du hast Lust, dich in Microservices, Cloud-Technologien und serverlose Architekturen einzuarbeiten. Gehaltsspanne 60.000 - 75.000 Was bieten wir dir Flexible und familienfreundliche Arbeitszeiten Die Möglichkeit bis zu 180 Tage / Jahr aus dem EU- Ausland zu arbeiten 27 Tage Urlaub Heiligabend und Silvester bekommst du von uns frei Firmenevents exklusive Mitarbeiterrabatte warten auf dich Ansprechpartner Wir freuen uns auf deine Unterlagen inkl. Gehaltsvorstellungen Jana Streich HR Manager Recruiting Employer BrandingJana.Streichgiffits.de das Giffits-Team Datenschutz ist uns wichtig, bitte beachte daher, dass wir im Bewerber-Management mit unserem Dienstleister Personio zusammenarbeiten. Für weitere Informationen, schaue dir bitte unsere Datenschutzerklärung an (www.giffits.de/datenschutz.htm). Über uns Giffits ist eines der größten Werbeartikelportale Europas. Heute betreuen wir mit bis zu 100 Mitarbeitern mehr als 40.000 Kunden. Neben unserem Gespür für Service, Innovation und Qualität basiert der Erfolg vor allem auf einem sorgfältig zusammengestellten Team. In unserem Hamburger Büro oder Remote arbeiten erfahrene Experten Seite an Seite mit engagierten Neueinsteigern. Wir wollen neue Maßstäbe in der Werbeartikelbranche setzen. Neugierig geworden Wir freuen uns auf deine Bewerbung Show more Show less Seniority level Mid-Senior level Employment type Full-time Job function Information Technology Industries Wholesale Import and Export.
    """
    
    print("Testing ATS Keyword Extraction with German Job Posting")
    print("=" * 60)
    
    # Create ATS service
    ats = AtsService()
    
    print(f"spaCy available: {ats.nlp is not None}")
    if ats.nlp:
        print(f"spaCy model: {ats.nlp.meta.get('name', 'Unknown')}")
    
    print("\nCurrent Keyword Extraction Results:")
    print("-" * 40)
    
    # Test different categories
    categories = ['required', 'preferred', 'industry', 'soft']
    
    for category in categories:
        keywords = ats.extract_keywords(german_job_description, category)
        print(f"\n{category.upper()} keywords ({len(keywords)}):")
        print(f"  {', '.join(keywords)}")
    
    print("\n" + "=" * 60)
    print("ANALYSIS OF THE PROBLEM")
    print("=" * 60)
    
    print("""
PROBLEM IDENTIFIED:
The ATS is extracting irrelevant keywords that are NOT in the job description:

❌ WRONG KEYWORDS EXTRACTED:
- 'r' (not in the text)
- 'compound' (not in the text) 
- 'nft' (not in the text)
- 'pandas' (not in the text)
- 'typescript' (not in the text)

✅ CORRECT KEYWORDS THAT SHOULD BE EXTRACTED:
- 'node.js' (mentioned in the text)
- 'vue.js' (mentioned in the text)
- 'sql' (mentioned in the text)
- 'nosql' (mentioned in the text)
- 'microservices' (mentioned in the text)
- 'cloud' (mentioned in the text)
- 'agile' (mentioned in the text)
- 'ci/cd' (mentioned in the text)

ROOT CAUSE:
The keyword extraction is matching partial strings incorrectly. For example:
- 'r' is being matched from 'remote' or other words containing 'r'
- 'compound' might be matched from 'component' or similar words
- 'nft' might be matched from 'not' or other words
- 'pandas' might be matched from 'and' or similar patterns

SOLUTION NEEDED:
1. Improve the matching logic to be more precise
2. Add better filtering for false positives
3. Use exact word boundaries for matching
4. Add a minimum word length requirement
5. Implement better context checking
    """)

def demonstrate_solution():
    """Demonstrate how the improved keyword extraction should work."""
    
    print("\n" + "=" * 60)
    print("PROPOSED SOLUTION")
    print("=" * 60)
    
    print("""
1. IMPROVE MATCHING LOGIC:
   - Use word boundaries (\\b) in regex patterns
   - Require exact word matches, not substring matches
   - Add minimum word length (3+ characters)
   - Check for word context

2. ADD BETTER FILTERING:
   - Filter out single letters ('r', 'a', 'i', etc.)
   - Filter out common words that might cause false matches
   - Add a whitelist of valid technical terms
   - Implement confidence scoring

3. IMPLEMENT CONTEXT CHECKING:
   - Check if the matched word is actually a technical term
   - Verify the word appears in a technical context
   - Use spaCy's part-of-speech tagging to identify technical nouns

4. ADD VALIDATION:
   - Cross-reference with known skill databases
   - Use industry-specific terminology
   - Implement manual review for edge cases
    """)

if __name__ == "__main__":
    test_german_job_posting()
    demonstrate_solution()
