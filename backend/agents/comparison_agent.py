import logging
from collections import Counter
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComparisonAgent:
    """
    Compares research methods across multiple papers.
    Analyzes strengths, weaknesses, and performance differences.
    """
    
    def __init__(self):
        # Performance indicators
        self.positive_indicators = [
            'outperform', 'improve', 'better', 'superior', 'achieve', 'effective',
            'efficient', 'accurate', 'robust', 'state-of-the-art', 'novel', 'significant'
        ]
        self.negative_indicators = [
            'limitation', 'challenge', 'difficult', 'complex', 'expensive',
            'slow', 'limited', 'constraint', 'drawback', 'issue'
        ]
        
        # Common method categories
        self.method_categories = {
            'deep_learning': ['neural', 'deep learning', 'cnn', 'rnn', 'transformer', 'lstm'],
            'machine_learning': ['svm', 'random forest', 'decision tree', 'regression', 'classification'],
            'optimization': ['gradient', 'optimization', 'genetic algorithm', 'evolutionary'],
            'statistical': ['bayesian', 'statistical', 'probabilistic', 'markov'],
            'hybrid': ['hybrid', 'ensemble', 'combination', 'integrated']
        }
    
    def process(self, extraction_data):
        """
        Compare research methods across papers.
        
        Args:
            extraction_data (dict): Output from extraction agent
            
        Returns:
            dict: Method comparison with strengths, weaknesses, and best performing
        """
        try:
            extracted_knowledge = extraction_data.get('extracted_knowledge', [])
            logger.info(f"Starting comparison for {len(extracted_knowledge)} papers")
            
            if not extracted_knowledge:
                logger.warning("No extracted knowledge to compare")
                return self._empty_response()
            
            # Extract and categorize methods
            methods_data = self._extract_methods_data(extracted_knowledge)
            
            # Analyze strengths and weaknesses
            strengths = self._analyze_strengths(methods_data, extracted_knowledge)
            weaknesses = self._analyze_weaknesses(methods_data, extracted_knowledge)
            
            # Determine best performing method
            best_performing = self._determine_best_performing(methods_data, extracted_knowledge)
            
            # Get unique methods list
            methods_list = list(methods_data.keys())
            
            logger.info(f"Comparison complete: {len(methods_list)} unique methods identified")
            
            return {
                'agent': 'Comparison Agent',
                'status': 'completed',
                'method_comparison': {
                    'methods': methods_list,
                    'strengths': strengths,
                    'weaknesses': weaknesses,
                    'best_performing': best_performing
                },
                'total_methods': len(methods_list),
                'message': f"Compared {len(methods_list)} methods across {len(extracted_knowledge)} papers"
            }
            
        except Exception as e:
            logger.error(f"Comparison agent error: {str(e)}")
            return {
                'agent': 'Comparison Agent',
                'status': 'error',
                'method_comparison': {
                    'methods': [],
                    'strengths': [],
                    'weaknesses': [],
                    'best_performing': ''
                },
                'total_methods': 0,
                'message': f"Error during comparison: {str(e)}"
            }
    
    def _extract_methods_data(self, extracted_knowledge):
        """Extract and categorize methods from papers."""
        methods_data = {}
        
        for paper in extracted_knowledge:
            method_text = paper.get('methods', '').lower()
            
            if not method_text or 'not' in method_text:
                continue
            
            # Categorize the method
            category = self._categorize_method(method_text)
            
            if category not in methods_data:
                methods_data[category] = {
                    'count': 0,
                    'papers': [],
                    'descriptions': []
                }
            
            methods_data[category]['count'] += 1
            methods_data[category]['papers'].append(paper.get('paper_title', 'Unknown'))
            methods_data[category]['descriptions'].append(method_text)
        
        return methods_data
    
    def _categorize_method(self, method_text):
        """Categorize method based on keywords."""
        for category, keywords in self.method_categories.items():
            if any(keyword in method_text for keyword in keywords):
                return category.replace('_', ' ').title()
        
        # Extract key method terms if no category matches
        method_words = method_text.split()
        for word in method_words:
            if word in ['algorithm', 'approach', 'method', 'technique', 'framework', 'model']:
                idx = method_words.index(word)
                if idx > 0:
                    return f"{method_words[idx-1].title()} {word.title()}"
        
        return "General Approach"
    
    def _analyze_strengths(self, methods_data, extracted_knowledge):
        """Analyze strengths of different methods."""
        strengths = []
        
        for method, data in methods_data.items():
            method_strengths = []
            
            # Check frequency (popular methods)
            if data['count'] > 1:
                method_strengths.append(f"Widely adopted ({data['count']} papers)")
            
            # Analyze findings for positive indicators
            for paper in extracted_knowledge:
                if any(paper.get('paper_title', '') in p for p in data['papers']):
                    findings = paper.get('key_findings', '').lower()
                    
                    positive_count = sum(1 for indicator in self.positive_indicators 
                                       if indicator in findings)
                    
                    if positive_count >= 2:
                        method_strengths.append("Demonstrates strong performance results")
                        break
            
            # Add method-specific strengths
            if 'deep learning' in method.lower():
                method_strengths.append("Handles complex patterns and large datasets")
            elif 'optimization' in method.lower():
                method_strengths.append("Efficient resource utilization")
            elif 'statistical' in method.lower():
                method_strengths.append("Provides theoretical guarantees")
            elif 'hybrid' in method.lower():
                method_strengths.append("Combines multiple approaches for robustness")
            
            if method_strengths:
                strengths.append({
                    'method': method,
                    'strengths': method_strengths[:3]  # Top 3 strengths
                })
        
        return strengths
    
    def _analyze_weaknesses(self, methods_data, extracted_knowledge):
        """Analyze weaknesses of different methods."""
        weaknesses = []
        
        for method, data in methods_data.items():
            method_weaknesses = []
            
            # Analyze findings for negative indicators
            for paper in extracted_knowledge:
                if any(paper.get('paper_title', '') in p for p in data['papers']):
                    findings = paper.get('key_findings', '').lower()
                    methods_text = paper.get('methods', '').lower()
                    
                    negative_count = sum(1 for indicator in self.negative_indicators 
                                       if indicator in findings or indicator in methods_text)
                    
                    if negative_count >= 1:
                        method_weaknesses.append("May have computational or practical limitations")
                        break
            
            # Add method-specific weaknesses
            if 'deep learning' in method.lower():
                method_weaknesses.append("Requires large amounts of training data")
                method_weaknesses.append("Limited interpretability")
            elif 'optimization' in method.lower():
                method_weaknesses.append("May converge to local optima")
            elif 'statistical' in method.lower():
                method_weaknesses.append("Strong assumptions about data distribution")
            elif 'machine learning' in method.lower() and 'deep' not in method.lower():
                method_weaknesses.append("May not capture complex non-linear patterns")
            
            if method_weaknesses:
                weaknesses.append({
                    'method': method,
                    'weaknesses': method_weaknesses[:3]  # Top 3 weaknesses
                })
        
        return weaknesses
    
    def _determine_best_performing(self, methods_data, extracted_knowledge):
        """Determine the best performing method based on findings."""
        method_scores = {}
        
        for method, data in methods_data.items():
            score = 0
            
            # Score based on frequency
            score += data['count'] * 10
            
            # Score based on positive indicators in findings
            for paper in extracted_knowledge:
                if any(paper.get('paper_title', '') in p for p in data['papers']):
                    findings = paper.get('key_findings', '').lower()
                    
                    # Count positive indicators
                    positive_count = sum(1 for indicator in self.positive_indicators 
                                       if indicator in findings)
                    score += positive_count * 5
                    
                    # Bonus for state-of-the-art mentions
                    if 'state-of-the-art' in findings or 'sota' in findings:
                        score += 20
            
            method_scores[method] = score
        
        if not method_scores:
            return "Insufficient data for comparison"
        
        # Get best performing method
        best_method = max(method_scores, key=method_scores.get)
        best_score = method_scores[best_method]
        
        if best_score > 30:
            return f"{best_method} (high confidence)"
        elif best_score > 15:
            return f"{best_method} (moderate confidence)"
        else:
            return f"{best_method} (low confidence - limited data)"
    
    def _empty_response(self):
        """Return empty response structure."""
        return {
            'agent': 'Comparison Agent',
            'status': 'completed',
            'method_comparison': {
                'methods': [],
                'strengths': [],
                'weaknesses': [],
                'best_performing': 'No methods to compare'
            },
            'total_methods': 0,
            'message': 'No extracted knowledge available for comparison'
        }
