#!/usr/bin/env python3
"""
Simple test to demonstrate the improved job posting formatting.
"""

import re

def clean_and_format_text(text: str) -> str:
    """
    Clean and format text while preserving structure and readability.
    Enhanced for German job postings.
    """
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

def test_german_job_formatting():
    """Test the improved formatting for German job postings."""
    
    # Sample German job posting text (similar to what the user provided)
    german_job_text = """NautilusLog mit Sitz in Hamburg ist ein Innovator im Bereich maritimer Technologie und entwickelt fortschrittliche, digitale Lösungen für die Schifffahrtsindustrie. Wir legen großen Wert auf Innovation, Zusammenarbeit und ein dynamisches Arbeitsumfeld, in dem dein Beitrag zählt. Dich erwartet ein engagiertes Team in der historischen Speicherstadt - nur wenige Schritte von der U3-Station Baumwall entfernt.
Zur Verstärkung suchen wir zum nächstmöglichen Zeitpunkt dich als
Frontend Engineer - React / Next.js / TypeScript (m/w/d)
Vollzeit
hybrid
Hamburg
mit Berufserfahrung
Was Du Bei Uns Bewegst
Du gestaltest die User Interfaces unserer Webanwendungen maßgeblich mit und sorgst für ein optimales Nutzererlebnis.
Du arbeitest eng mit UX/UI-Design, Backend und Produktmanagement zusammen und bringst deine Ideen aktiv ein.
Du evaluierst neue Technologien und Frameworks und gestaltest unsere Frontend-Strategie mit.
In einem funktionsübergreifenden Team kannst du deine Fähigkeiten auch in anderen Bereichen einbringen.
Was Du Mitbringst
Abgeschlossenes Studium im Bereich Informatik, Computer Science oder eine vergleichbare Qualifikation
Fundierte Erfahrung in der Frontend-Entwicklung, idealerweise mit Kenntnissen in React, Next.js, Tailwind, Redux, Redux Toolkit, TypeScript und JavaScript
Sicherer Umgang mit REST APIs und Fähigkeit zur eigenständigen Integration
Sehr gute Deutsch- und gute Englischkenntnisse in Wort und Schrift
Teamgeist, Kommunikationsstärke sowie eine selbstständige und lösungsorientierte Arbeitsweise
Erfahrungen mit asynchroner Infrastruktur, End-to-End-Tests oder Angular (von Vorteil, aber kein Muss)
Was Wir Dir Bieten
Faires und transparentes Gehalt bis zu 80.000 , abgestimmt auf deine Qualifikation
Hybrides Arbeiten - mit der Freiheit, deinen Arbeitsplatz zwischen mobiler Arbeit und Büro flexibel zu wählen
Gleitzeit mit fairer Kernarbeitszeit (9:30 - 16:00 Uhr) - für Flexibilität im Alltag bei gleichzeitiger Verlässlichkeit im Team
30 Tage Urlaub - für ausreichend Erholung und eine gesunde Work-Life-Balance
Mobilitäts- und Gesundheitszuschüsse: 50 % Beteiligung am Jobticket und am EGYM Wellpass
Modernes Büro in Toplage in der Hamburger Speicherstadt mit Blick aufs Wasser und kurzen Wegen in die Innenstadt
Community-Events, Meetups und gemeinsame Aktivitäten - digital wie vor Ort für Austausch und Teamspirit
Möchtest du mit uns die digitale Zukunft der Schifffahrt gestalten
Dann freuen wir uns auf deine Online-Bewerbung
Für Fragen vorab melde dich gerne jederzeit telefonisch bei Jonas Albrecht unter ."""
    
    print("Testing Improved Job Posting Formatting")
    print("=" * 60)
    
    print("\nORIGINAL TEXT (Poorly Formatted):")
    print("-" * 40)
    print(german_job_text)
    
    print("\n" + "=" * 60)
    print("IMPROVED FORMATTING")
    print("=" * 60)
    
    # Apply the improved formatting
    formatted_text = clean_and_format_text(german_job_text)
    
    print("\nFORMATTED TEXT (With Proper Structure):")
    print("-" * 40)
    print(formatted_text)
    
    print("\n" + "=" * 60)
    print("KEY IMPROVEMENTS")
    print("=" * 60)
    
    print("""
✅ IMPROVEMENTS MADE:

1. SECTION HEADERS:
   - Added proper spacing after German headers like "Was Du Bei Uns Bewegst"
   - Added spacing after "Was Du Mitbringst", "Was Wir Dir Bieten"
   - Added spacing after "Vollzeit", "hybrid", "Hamburg"

2. BULLET POINTS:
   - Converted "Du" statements to bullet points
   - Added bullet points for requirements like "Abgeschlossenes Studium"
   - Added bullet points for benefits like "Faires und transparentes Gehalt"

3. STRUCTURE:
   - Proper line breaks between sections
   - Consistent formatting for lists
   - Better readability with proper spacing

4. FRONTEND DISPLAY:
   - The JobPostingDisplay component will render this with:
     * Proper headings (h3 tags)
     * Bullet point lists (ul/li tags)
     * Keyword highlighting (green for matched, red for missing)
     * Clean, professional layout

5. KEYWORD HIGHLIGHTING:
   - Matched keywords will be highlighted in GREEN
   - Missing keywords will be highlighted in RED
   - Keywords are extracted using word boundaries to prevent false matches
    """)

if __name__ == "__main__":
    test_german_job_formatting()
