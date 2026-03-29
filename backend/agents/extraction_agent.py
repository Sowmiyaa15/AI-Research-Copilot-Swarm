import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtractionAgent:
    """
    Analyzes research paper abstracts and extracts key information.
    Uses NLP techniques to identify methods, findings, and problem domains.
    """
    
    def __init__(self):
        self.method_keywords = [
            'algorithm', 'approach', 'method', 'technique', 'framework',
            'model', 'architecture', 'system', 'strategy', 'mechanism'
        ]
        self.finding_keywords = [
            'achieve', 'demonstrate', 'show', 'result', 'improve', 'outperform',
            'find', 'discover', 'reveal', 'indicate', 'suggest', 'prove'
        ]
        self.problem_keywords = [
            'problem', 'challenge', 'issue', 'task', 'question', 'limitation',
            'difficulty', 'obstacle', 'address', 'solve', 'tackle'
        ]
    
    def process(self, retrieval_data):
        """
        Extract knowledge from research papers.
        
        Args:
            retrieval_data (dict): Output from retrieval agent containing papers
            
        Returns:
            dict: Structured JSON with extracted knowledge
        """
        try:
            papers = retrieval_data.get('papers', [])
            logger.info(f"Starting extraction for {len(papers)} papers")
            
            if not papers:
                logger.warning("No papers to extract from")
                return self._empty_response()
            
            extracted_knowledge = []
            
            for paper in papers:
                try:
                    knowledge = self._extract_from_paper(paper)
                    extracted_knowledge.append(knowledge)
                    logger.debug(f"Extracted knowledge from: {paper.get('title', 'Unknown')[:50]}")
                except Exception as e:
                    logger.error(f"Failed to extract from paper: {str(e)}")
                    continue
            
            logger.info(f"Successfully extracted knowledge from {len(extracted_knowledge)} papers")
            
            return {
                'agent': 'Extraction Agent',
                'status': 'completed',
                'extracted_knowledge': extracted_knowledge,
                'papers_analyzed': len(extracted_knowledge),
                'message': f"Extracted knowledge from {len(extracted_knowledge)} papers"
            }
            
        except Exception as e:
            logger.error(f"Extraction agent error: {str(e)}")
            return {
                'agent': 'Extraction Agent',
                'status': 'error',
                'extracted_knowledge': [],
                'papers_analyzed': 0,
                'message': f"Error during extraction: {str(e)}"
            }
    
    def _extract_from_paper(self, paper):
        """Extract key information from a single paper."""
        abstract = paper.get('abstract', '')
        title = paper.get('title', 'Unknown')
        
        # Extract methods used
        methods = self._extract_methods(abstract)
        
        # Extract key findings
        key_findings = self._extract_findings(abstract)
        
        # Extract problem domain
        problem_domain = self._extract_problem_domain(abstract, title)
        
        return {
            'paper_title': title,
            'methods': methods,
            'key_findings': key_findings,
            'problem_domain': problem_domain
        }
    
    def _extract_methods(self, text):
        """Extract methods and techniques from abstract."""
        sentences = self._split_sentences(text)
        method_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in self.method_keywords):
                # Extract the core method description
                method_sentences.append(sentence.strip())
        
        if method_sentences:
            # Return the most relevant method sentence
            return self._summarize_methods(method_sentences)
        
        return "Methods not explicitly stated in abstract"
    
    def _extract_findings(self, text):
        """Extract key findings and results from abstract."""
        sentences = self._split_sentences(text)
        finding_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in self.finding_keywords):
                finding_sentences.append(sentence.strip())
        
        if finding_sentences:
            return self._summarize_findings(finding_sentences)
        
        return "Key findings not explicitly stated in abstract"
    
    def _extract_problem_domain(self, text, title):
        """Extract the problem domain being addressed."""
        # Check title first for domain indicators
        title_lower = title.lower()
        
        # Common research domains
        domains = {
            'computer vision': ['vision', 'image', 'visual', 'detection', 'segmentation'],
            'natural language processing': ['nlp', 'language', 'text', 'translation', 'sentiment'],
            'machine learning': ['learning', 'classification', 'prediction', 'training'],
            'robotics': ['robot', 'autonomous', 'navigation', 'manipulation'],
            'optimization': ['optimization', 'optimize', 'efficient', 'performance'],
            'data science': ['data', 'analysis', 'mining', 'analytics'],
            'security': ['security', 'privacy', 'attack', 'defense', 'encryption']
        }
        
        # Check for domain matches
        for domain, keywords in domains.items():
            if any(kw in title_lower for kw in keywords):
                return domain
        
        # Extract problem from abstract
        sentences = self._split_sentences(text)
        for sentence in sentences[:3]:  # Check first 3 sentences
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in self.problem_keywords):
                # Extract problem description
                problem = self._extract_problem_statement(sentence)
                if problem:
                    return problem
        
        return "General research domain"
    
    def _split_sentences(self, text):
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 20]
    
    def _summarize_methods(self, method_sentences):
        """Create readable summary of methods."""
        if not method_sentences:
            return "Methods not specified"
        
        # Take the most informative sentence (usually the longest with method keywords)
        best_sentence = max(method_sentences, key=lambda s: sum(
            1 for kw in self.method_keywords if kw in s.lower()
        ))
        
        # Clean and truncate if too long
        summary = best_sentence[:200] + '...' if len(best_sentence) > 200 else best_sentence
        return summary
    
    def _summarize_findings(self, finding_sentences):
        """Create readable summary of findings."""
        if not finding_sentences:
            return "Findings not specified"
        
        # Take the most informative sentence
        best_sentence = max(finding_sentences, key=lambda s: sum(
            1 for kw in self.finding_keywords if kw in s.lower()
        ))
        
        # Clean and truncate if too long
        summary = best_sentence[:200] + '...' if len(best_sentence) > 200 else best_sentence
        return summary
    
    def _extract_problem_statement(self, sentence):
        """Extract concise problem statement from sentence."""
        # Look for problem-related phrases
        sentence_lower = sentence.lower()
        
        for keyword in self.problem_keywords:
            if keyword in sentence_lower:
                # Extract the phrase around the keyword
                words = sentence.split()
                for i, word in enumerate(words):
                    if keyword in word.lower():
                        # Get context around the keyword
                        start = max(0, i - 3)
                        end = min(len(words), i + 8)
                        problem = ' '.join(words[start:end])
                        return problem[:150]
        
        return None
    
    def _empty_response(self):
        """Return empty response structure."""
        return {
            'agent': 'Extraction Agent',
            'status': 'completed',
            'extracted_knowledge': [],
            'papers_analyzed': 0,
            'message': 'No papers available for extraction'
        }
