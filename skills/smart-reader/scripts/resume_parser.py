#!/usr/bin/env python3
"""
Resume Parser - Specialized CV/Resume extraction
Extracts structured information from resumes
"""

import re
from typing import Dict, List
from document_reader import DocumentReader

class ResumeParser:
    """Parse resumes and extract structured information"""
    
    def __init__(self):
        self.reader = DocumentReader()
    
    def parse(self, file_path: str) -> Dict:
        """Parse resume and extract key information"""
        result = self.reader.read_file(file_path)
        
        if not result['success']:
            return result
        
        text = result['content']
        
        return {
            'success': True,
            'personal_info': self._extract_personal_info(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'skills': self._extract_skills(text),
            'raw_text': text
        }
    
    def _extract_personal_info(self, text: str) -> Dict:
        """Extract name, email, phone, location"""
        info = {}
        
        # Email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            info['email'] = email_match.group(0)
        
        # Phone
        phone_match = re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4}', text)
        if phone_match:
            info['phone'] = phone_match.group(0)
        
        # Name (first line or after specific patterns)
        lines = text.strip().split('\n')
        if lines:
            info['name'] = lines[0].strip()
        
        return info
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience entries"""
        experiences = []
        
        # Pattern: Company - Date
        patterns = [
            r'([A-Z][^\n]+?)\s*[-–]\s*(\w+\s+\d{4})\s*[-–]\s*(\w+\s+\d{4}|Present)',
            r'([A-Z][^\n]+?)\s*\|\s*([^\n]+?)\s*[-–]\s*(\w+\s+\d{4})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            for match in matches:
                experiences.append({
                    'company': match[0].strip() if isinstance(match, tuple) else match.strip(),
                    'date': match[1] if isinstance(match, tuple) and len(match) > 1 else ''
                })
        
        return experiences
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education entries"""
        education = []
        
        # Look for education keywords
        edu_keywords = ['Bachelor', 'Master', 'PhD', 'Degree', 'University', 'College']
        lines = text.split('\n')
        
        for line in lines:
            if any(keyword in line for keyword in edu_keywords):
                education.append(line.strip())
        
        return education
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills section"""
        skills = []
        
        # Look for skills section
        skills_section = re.search(r'(?:Skills|Core Competencies)[\s\S]*?(?=\n\n|\Z)', text, re.IGNORECASE)
        if skills_section:
            skills_text = skills_section.group(0)
            # Extract bullet points
            bullets = re.findall(r'[•\-]\s*([^\n]+)', skills_text)
            skills = [b.strip() for b in bullets]
        
        return skills

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python resume_parser.py <resume_file>")
        return
    
    parser = ResumeParser()
    result = parser.parse(sys.argv[1])
    
    import json
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()
