import logging
from collections import defaultdict
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidationAgent:
    """
    Validates consistency of claims across research papers.
    Identifies contradictions and common agreements.
    """
    
    def __init__(self):
        # Claim indicators
        self.assertion_keywords = [
            'demonstrate', 'show', 'prove', 'find', 'reveal', 'indicate',
            'suggest', 'confirm', 'establish', 'achieve', 'outperform'
        ]
        
        # Contradiction indicators
        self.contradiction_keywords = [
            'however', 'but', 'although', 'despite', 'contrary', 'unlike',
            'different', 'disagree', 'challenge', 'question'
        ]
        
        # Agreement indicators
        self.agreement_keywords = [
            'similarly', 'likewise', 'also', 'consistent', 'agree', 'confirm',
            'support', 'align', 'corroborate', 'validate'
        ]
        
        # Performance claim patterns
        self.performance_patterns = [
            r'(\d+)%\s*(improvement|accuracy|precision|recall)',
            r'(better|worse|superior|inferior)\s+than',
            r'(outperform|exceed|surpass)',
            r'state-of-the-art',
            r'(increase|decrease)\s+by\s+(\d+)'
        ]
    
    def process(self, comparison_data):
        """
        Validate consistency of claims across papers.
        
        Args:
            comparison_data (dict): Output from comparison agent
            
        Returns:
            dict: Validation results with consistent/conflicting claims
        """
        try:
            # Get method comparison data
            method_comparison = comparison_data.get('method_comparison', {})
            methods = method_comparison.get('methods', [])
            strengths = method_comparison.get('strengths', [])
            weaknesses = method_comparison.get('weaknesses', [])
            
            logger.info(f"Starting validation for {len(methods)} methods")
            
            if not methods:
                logger.warning("No methods to validate")
                return self._empty_response()
            
            # Analyze claims
            consistent_claims = self._identify_consistent_claims(strengths, weaknesses, methods)
            conflicting_claims = self._identify_conflicting_claims(strengths, weaknesses, methods)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                consistent_claims, 
                conflicting_claims, 
                len(methods)
            )
            
            logger.info(f"Validation complete: {len(consistent_claims)} consistent, "
                       f"{len(conflicting_claims)} conflicting claims")
            
            return {
                'agent': 'Validation Agent',
                'status': 'completed',
                'validation': {
                    'consistent_claims': consistent_claims,
                    'conflicting_claims': conflicting_claims,
                    'confidence_score': confidence_score
                },
                'total_claims_analyzed': len(consistent_claims) + len(conflicting_claims),
                'message': f"Validated claims across {len(methods)} methods"
            }
            
        except Exception as e:
            logger.error(f"Validation agent error: {str(e)}")
            return {
                'agent': 'Validation Agent',
                'status': 'error',
                'validation': {
                    'consistent_claims': [],
                    'conflicting_claims': [],
                    'confidence_score': 'Error'
                },
                'total_claims_analyzed': 0,
                'message': f"Error during validation: {str(e)}"
            }
    
    def _identify_consistent_claims(self, strengths, weaknesses, methods):
        """Identify claims that are consistent across papers."""
        consistent_claims = []
        
        # Analyze strength patterns
        strength_themes = defaultdict(list)
        for strength_data in strengths:
            method = strength_data.get('method', '')
            for strength in strength_data.get('strengths', []):
                # Categorize strength
                theme = self._categorize_claim(strength)
                strength_themes[theme].append({
                    'method': method,
                    'claim': strength
                })
        
        # Find themes mentioned by multiple methods
        for theme, claims in strength_themes.items():
            if len(claims) >= 2:
                methods_list = [c['method'] for c in claims]
                consistent_claims.append({
                    'claim': f"{theme} is a common strength",
                    'supporting_methods': methods_list,
                    'evidence_count': len(claims),
                    'type': 'strength_agreement'
                })
        
        # Analyze weakness patterns
        weakness_themes = defaultdict(list)
        for weakness_data in weaknesses:
            method = weakness_data.get('method', '')
            for weakness in weakness_data.get('weaknesses', []):
                theme = self._categorize_claim(weakness)
                weakness_themes[theme].append({
                    'method': method,
                    'claim': weakness
                })
        
        # Find common weaknesses
        for theme, claims in weakness_themes.items():
            if len(claims) >= 2:
                methods_list = [c['method'] for c in claims]
                consistent_claims.append({
                    'claim': f"{theme} is a recognized limitation",
                    'supporting_methods': methods_list,
                    'evidence_count': len(claims),
                    'type': 'weakness_agreement'
                })
        
        # Add general consistency claims
        if len(methods) >= 3:
            consistent_claims.append({
                'claim': "Multiple research approaches are being actively explored",
                'supporting_methods': methods,
                'evidence_count': len(methods),
                'type': 'general_agreement'
            })
        
        return consistent_claims
    
    def _identify_conflicting_claims(self, strengths, weaknesses, methods):
        """Identify contradictory claims across papers."""
        conflicting_claims = []
        
        # Check for strength-weakness conflicts
        strength_claims = {}
        for strength_data in strengths:
            method = strength_data.get('method', '')
            for strength in strength_data.get('strengths', []):
                theme = self._categorize_claim(strength)
                if theme not in strength_claims:
                    strength_claims[theme] = []
                strength_claims[theme].append(method)
        
        weakness_claims = {}
        for weakness_data in weaknesses:
            method = weakness_data.get('method', '')
            for weakness in weakness_data.get('weaknesses', []):
                theme = self._categorize_claim(weakness)
                if theme not in weakness_claims:
                    weakness_claims[theme] = []
                weakness_claims[theme].append(method)
        
        # Find contradictions
        for theme in strength_claims:
            if theme in weakness_claims:
                conflicting_claims.append({
                    'claim': f"Disagreement on {theme}",
                    'supporting_methods': strength_claims[theme],
                    'opposing_methods': weakness_claims[theme],
                    'type': 'direct_contradiction',
                    'description': f"Some methods cite this as strength, others as weakness"
                })
        
        # Check for performance contradictions
        if len(methods) >= 2:
            # If multiple methods claim to be "best performing"
            high_performance_methods = []
            for strength_data in strengths:
                method = strength_data.get('method', '')
                for strength in strength_data.get('strengths', []):
                    if any(word in strength.lower() for word in ['strong performance', 'outperform', 'state-of-the-art']):
                        high_performance_methods.append(method)
            
            if len(high_performance_methods) >= 2:
                conflicting_claims.append({
                    'claim': "Multiple methods claim superior performance",
                    'supporting_methods': high_performance_methods,
                    'opposing_methods': [],
                    'type': 'performance_conflict',
                    'description': "Different papers may use different benchmarks or metrics"
                })
        
        # Check for methodological conflicts
        if len(methods) >= 3:
            method_types = self._categorize_methods(methods)
            if len(method_types) >= 2:
                conflicting_claims.append({
                    'claim': "Diverse methodological approaches with varying assumptions",
                    'supporting_methods': list(method_types.keys()),
                    'opposing_methods': [],
                    'type': 'methodological_diversity',
                    'description': "Different fundamental approaches may not be directly comparable"
                })
        
        return conflicting_claims
    
    def _categorize_claim(self, claim_text):
        """Categorize a claim into a theme."""
        claim_lower = claim_text.lower()
        
        # Performance themes
        if any(word in claim_lower for word in ['performance', 'accurate', 'efficient', 'effective']):
            return "performance"
        
        # Data themes
        if any(word in claim_lower for word in ['data', 'dataset', 'training']):
            return "data requirements"
        
        # Complexity themes
        if any(word in claim_lower for word in ['complex', 'computational', 'resource']):
            return "computational complexity"
        
        # Interpretability themes
        if any(word in claim_lower for word in ['interpret', 'explain', 'transparent']):
            return "interpretability"
        
        # Scalability themes
        if any(word in claim_lower for word in ['scale', 'large', 'size']):
            return "scalability"
        
        # Robustness themes
        if any(word in claim_lower for word in ['robust', 'stable', 'reliable']):
            return "robustness"
        
        # Generalization themes
        if any(word in claim_lower for word in ['general', 'transfer', 'adapt']):
            return "generalization"
        
        return "general methodology"
    
    def _categorize_methods(self, methods):
        """Categorize methods into types."""
        method_types = defaultdict(list)
        
        for method in methods:
            method_lower = method.lower()
            
            if any(word in method_lower for word in ['deep', 'neural', 'learning']):
                method_types['Deep Learning'].append(method)
            elif any(word in method_lower for word in ['statistical', 'bayesian']):
                method_types['Statistical'].append(method)
            elif any(word in method_lower for word in ['optimization', 'genetic']):
                method_types['Optimization'].append(method)
            else:
                method_types['Other'].append(method)
        
        return method_types
    
    def _calculate_confidence_score(self, consistent_claims, conflicting_claims, num_methods):
        """Calculate confidence score for validation."""
        if num_methods == 0:
            return "Insufficient data"
        
        # Calculate score based on consistency ratio
        total_claims = len(consistent_claims) + len(conflicting_claims)
        
        if total_claims == 0:
            return "Low (insufficient claims)"
        
        consistency_ratio = len(consistent_claims) / total_claims if total_claims > 0 else 0
        
        # Adjust for number of methods
        method_factor = min(num_methods / 5, 1.0)  # Normalize to max of 5 methods
        
        # Calculate final score
        score = consistency_ratio * 0.7 + method_factor * 0.3
        
        if score >= 0.75:
            return f"High ({int(score * 100)}% - strong agreement across papers)"
        elif score >= 0.5:
            return f"Moderate ({int(score * 100)}% - some contradictions present)"
        elif score >= 0.3:
            return f"Low ({int(score * 100)}% - significant contradictions)"
        else:
            return f"Very Low ({int(score * 100)}% - highly conflicting claims)"
    
    def _empty_response(self):
        """Return empty response structure."""
        return {
            'agent': 'Validation Agent',
            'status': 'completed',
            'validation': {
                'consistent_claims': [],
                'conflicting_claims': [],
                'confidence_score': 'No data to validate'
            },
            'total_claims_analyzed': 0,
            'message': 'No comparison data available for validation'
        }
