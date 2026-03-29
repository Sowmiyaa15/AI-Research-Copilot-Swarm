import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GapAgent:
    """
    Identifies research gaps by analyzing methods, limitations, and unexplored areas.
    """
    
    def __init__(self):
        # Common research approaches to check for
        self.standard_approaches = {
            'deep_learning': ['neural network', 'deep learning', 'cnn', 'rnn', 'transformer'],
            'traditional_ml': ['svm', 'random forest', 'decision tree', 'naive bayes'],
            'ensemble': ['ensemble', 'boosting', 'bagging', 'stacking'],
            'transfer_learning': ['transfer learning', 'pre-trained', 'fine-tuning'],
            'reinforcement': ['reinforcement learning', 'q-learning', 'policy gradient'],
            'unsupervised': ['clustering', 'unsupervised', 'autoencoder', 'gan']
        }
        
        # Dataset considerations
        self.dataset_aspects = [
            'benchmark', 'real-world', 'synthetic', 'large-scale', 
            'multi-modal', 'cross-domain', 'imbalanced'
        ]
        
        # Scalability indicators
        self.scalability_keywords = [
            'scale', 'distributed', 'parallel', 'efficiency', 
            'computational cost', 'memory', 'real-time'
        ]
        
        # Limitation keywords
        self.limitation_keywords = [
            'limitation', 'challenge', 'constraint', 'drawback',
            'difficult', 'expensive', 'limited', 'lack'
        ]
    
    def process(self, validation_data):
        """
        Identify research gaps from validation data.
        
        Args:
            validation_data (dict): Output from validation agent
            
        Returns:
            dict: Identified research gaps
        """
        try:
            validation = validation_data.get('validation', {})
            consistent_claims = validation.get('consistent_claims', [])
            conflicting_claims = validation.get('conflicting_claims', [])
            
            logger.info("Starting gap analysis")
            
            research_gaps = []
            
            # Analyze missing approaches
            missing_approaches = self._identify_missing_approaches(consistent_claims)
            research_gaps.extend(missing_approaches)
            
            # Analyze method limitations
            method_limitations = self._identify_method_limitations(consistent_claims, conflicting_claims)
            research_gaps.extend(method_limitations)
            
            # Analyze dataset gaps
            dataset_gaps = self._identify_dataset_gaps(consistent_claims)
            research_gaps.extend(dataset_gaps)
            
            # Analyze scalability issues
            scalability_gaps = self._identify_scalability_gaps(consistent_claims, conflicting_claims)
            research_gaps.extend(scalability_gaps)
            
            # Analyze conflicts as opportunities
            conflict_gaps = self._identify_conflict_opportunities(conflicting_claims)
            research_gaps.extend(conflict_gaps)
            
            # Remove duplicates and limit to most important gaps
            research_gaps = self._prioritize_gaps(research_gaps)
            
            logger.info(f"Gap analysis complete: {len(research_gaps)} gaps identified")
            
            return {
                'agent': 'Gap Analysis Agent',
                'status': 'completed',
                'research_gaps': research_gaps,
                'gap_count': len(research_gaps),
                'message': f"Identified {len(research_gaps)} research gaps and opportunities"
            }
            
        except Exception as e:
            logger.error(f"Gap analysis agent error: {str(e)}")
            return {
                'agent': 'Gap Analysis Agent',
                'status': 'error',
                'research_gaps': [],
                'gap_count': 0,
                'message': f"Error during gap analysis: {str(e)}"
            }
    
    def _identify_missing_approaches(self, consistent_claims):
        """Identify methodological approaches not covered in the research."""
        gaps = []
        
        # Extract mentioned methods from claims
        mentioned_methods = set()
        for claim in consistent_claims:
            methods = claim.get('supporting_methods', [])
            for method in methods:
                method_lower = method.lower()
                for approach_type, keywords in self.standard_approaches.items():
                    if any(kw in method_lower for kw in keywords):
                        mentioned_methods.add(approach_type)
        
        # Identify missing approaches
        all_approaches = set(self.standard_approaches.keys())
        missing = all_approaches - mentioned_methods
        
        if 'ensemble' in missing:
            gaps.append("Ensemble methods combining multiple approaches are underexplored")
        
        if 'transfer_learning' in missing:
            gaps.append("Transfer learning and pre-trained models could be leveraged")
        
        if 'reinforcement' in missing:
            gaps.append("Reinforcement learning approaches have not been investigated")
        
        if 'unsupervised' in missing:
            gaps.append("Unsupervised learning methods remain unexplored")
        
        # If too many traditional methods, suggest modern approaches
        if 'traditional_ml' in mentioned_methods and 'deep_learning' not in mentioned_methods:
            gaps.append("Modern deep learning architectures could provide improvements")
        
        return gaps
    
    def _identify_method_limitations(self, consistent_claims, conflicting_claims):
        """Identify limitations in current methods."""
        gaps = []
        
        # Analyze weakness agreements
        for claim in consistent_claims:
            if claim.get('type') == 'weakness_agreement':
                claim_text = claim.get('claim', '').lower()
                
                if 'data' in claim_text:
                    gaps.append("Data efficiency remains a challenge - methods requiring less training data needed")
                
                if 'interpretability' in claim_text or 'interpret' in claim_text:
                    gaps.append("Interpretability and explainability of models need improvement")
                
                if 'computational' in claim_text or 'complex' in claim_text:
                    gaps.append("Computational efficiency and resource optimization are ongoing concerns")
                
                if 'generalization' in claim_text or 'general' in claim_text:
                    gaps.append("Generalization across different domains and datasets is limited")
        
        # Analyze conflicts as limitations
        for conflict in conflicting_claims:
            if conflict.get('type') == 'performance_conflict':
                gaps.append("Standardized benchmarking and evaluation protocols are needed")
            
            if conflict.get('type') == 'methodological_diversity':
                gaps.append("Unified frameworks combining diverse methodological strengths could be developed")
        
        return gaps
    
    def _identify_dataset_gaps(self, consistent_claims):
        """Identify gaps related to datasets and evaluation."""
        gaps = []
        
        # Check for dataset diversity mentions
        dataset_mentioned = False
        for claim in consistent_claims:
            claim_text = claim.get('claim', '').lower()
            if any(aspect in claim_text for aspect in self.dataset_aspects):
                dataset_mentioned = True
                break
        
        if not dataset_mentioned:
            gaps.append("Evaluation on diverse and real-world datasets is lacking")
        
        # Common dataset gaps
        gaps.append("Cross-domain generalization and multi-modal data integration need exploration")
        gaps.append("Handling of imbalanced and noisy real-world data requires attention")
        
        return gaps
    
    def _identify_scalability_gaps(self, consistent_claims, conflicting_claims):
        """Identify scalability and practical deployment gaps."""
        gaps = []
        
        # Check if scalability is mentioned
        scalability_mentioned = False
        for claim in consistent_claims:
            claim_text = claim.get('claim', '').lower()
            if any(kw in claim_text for kw in self.scalability_keywords):
                scalability_mentioned = True
                break
        
        if not scalability_mentioned:
            gaps.append("Scalability to large-scale real-world applications is not addressed")
        
        # Check for computational concerns in weaknesses
        computational_concerns = False
        for claim in consistent_claims:
            if claim.get('type') == 'weakness_agreement':
                if 'computational' in claim.get('claim', '').lower():
                    computational_concerns = True
                    break
        
        if computational_concerns:
            gaps.append("Lightweight and efficient model architectures for resource-constrained environments needed")
        
        gaps.append("Real-time inference and deployment optimization strategies are underexplored")
        
        return gaps
    
    def _identify_conflict_opportunities(self, conflicting_claims):
        """Identify research opportunities from conflicting claims."""
        gaps = []
        
        for conflict in conflicting_claims:
            conflict_type = conflict.get('type', '')
            
            if conflict_type == 'direct_contradiction':
                gaps.append(f"Conflicting views on {conflict.get('claim', 'methodology')} present opportunity for comparative studies")
            
            if conflict_type == 'performance_conflict':
                gaps.append("Comprehensive comparative analysis with consistent evaluation metrics is needed")
            
            if conflict_type == 'methodological_diversity':
                gaps.append("Hybrid approaches combining strengths of different methodologies could bridge gaps")
        
        return gaps
    
    def _prioritize_gaps(self, gaps):
        """Prioritize and deduplicate research gaps."""
        # Remove duplicates while preserving order
        seen = set()
        unique_gaps = []
        
        for gap in gaps:
            gap_lower = gap.lower()
            # Simple deduplication based on key terms
            key_terms = set(gap_lower.split()[:5])  # First 5 words as key
            key = frozenset(key_terms)
            
            if key not in seen:
                seen.add(key)
                unique_gaps.append(gap)
        
        # Limit to top 10 most important gaps
        return unique_gaps[:10]
