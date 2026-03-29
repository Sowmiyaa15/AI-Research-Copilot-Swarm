import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OutputAgent:
    """
    Combines outputs from all agents into a structured, frontend-ready format.
    Ensures clean presentation and proper formatting.
    """
    
    def __init__(self):
        self.timestamp = None
    
    def process(self, all_agent_data):
        """
        Combine and structure all agent outputs.
        
        Args:
            all_agent_data (dict): Dictionary containing outputs from all agents
            
        Returns:
            dict: Structured output ready for frontend display
        """
        try:
            self.timestamp = datetime.now().isoformat()
            logger.info("Starting output aggregation and formatting")
            
            # Extract data from each agent
            retrieval_data = all_agent_data.get('retrieval', {})
            extraction_data = all_agent_data.get('extraction', {})
            comparison_data = all_agent_data.get('comparison', {})
            validation_data = all_agent_data.get('validation', {})
            gap_data = all_agent_data.get('gap_analysis', {})
            ideation_data = all_agent_data.get('ideation', {})
            
            # Format each section
            formatted_output = {
                'retrieved_papers': self._format_retrieved_papers(retrieval_data),
                'extracted_knowledge': self._format_extracted_knowledge(extraction_data),
                'method_comparison': self._format_method_comparison(comparison_data),
                'validation': self._format_validation(validation_data),
                'research_gaps': self._format_research_gaps(gap_data),
                'research_ideas': self._format_research_ideas(ideation_data),
                'summary': self._generate_summary(all_agent_data),
                'metadata': self._generate_metadata(all_agent_data)
            }
            
            logger.info("Output aggregation complete")
            
            return {
                'agent': 'Output Agent',
                'status': 'completed',
                'output': formatted_output,
                'message': 'Successfully compiled comprehensive research analysis',
                'timestamp': self.timestamp
            }
            
        except Exception as e:
            logger.error(f"Output agent error: {str(e)}")
            return {
                'agent': 'Output Agent',
                'status': 'error',
                'output': {},
                'message': f"Error during output generation: {str(e)}",
                'timestamp': datetime.now().isoformat()
            }
    
    def _format_retrieved_papers(self, retrieval_data):
        """Format retrieved papers for display."""
        papers = retrieval_data.get('papers', [])
        
        formatted_papers = []
        for i, paper in enumerate(papers, 1):
            formatted_papers.append({
                'id': i,
                'title': self._clean_text(paper.get('title', 'Unknown')),
                'authors': self._clean_text(paper.get('authors', 'Unknown')),
                'abstract': self._truncate_text(paper.get('abstract', ''), 300),
                'url': paper.get('url', '#'),
                'source': 'arXiv'
            })
        
        return {
            'total_papers': len(formatted_papers),
            'papers': formatted_papers,
            'query': retrieval_data.get('query', ''),
            'status': retrieval_data.get('status', 'unknown')
        }
    
    def _format_extracted_knowledge(self, extraction_data):
        """Format extracted knowledge for display."""
        knowledge = extraction_data.get('extracted_knowledge', [])
        
        formatted_knowledge = []
        for item in knowledge:
            formatted_knowledge.append({
                'paper_title': self._clean_text(item.get('paper_title', 'Unknown')),
                'methods': self._clean_text(item.get('methods', 'Not specified')),
                'key_findings': self._clean_text(item.get('key_findings', 'Not specified')),
                'problem_domain': self._clean_text(item.get('problem_domain', 'General'))
            })
        
        return {
            'total_analyzed': len(formatted_knowledge),
            'knowledge_items': formatted_knowledge,
            'status': extraction_data.get('status', 'unknown')
        }
    
    def _format_method_comparison(self, comparison_data):
        """Format method comparison for display."""
        method_comp = comparison_data.get('method_comparison', {})
        
        return {
            'methods': method_comp.get('methods', []),
            'total_methods': len(method_comp.get('methods', [])),
            'strengths': self._format_strengths_weaknesses(method_comp.get('strengths', [])),
            'weaknesses': self._format_strengths_weaknesses(method_comp.get('weaknesses', [])),
            'best_performing': method_comp.get('best_performing', 'Not determined'),
            'status': comparison_data.get('status', 'unknown')
        }
    
    def _format_strengths_weaknesses(self, items):
        """Format strengths or weaknesses list."""
        formatted = []
        for item in items:
            method = item.get('method', 'Unknown')
            points = item.get('strengths', item.get('weaknesses', []))
            
            formatted.append({
                'method': method,
                'points': [self._clean_text(p) for p in points]
            })
        
        return formatted
    
    def _format_validation(self, validation_data):
        """Format validation results for display."""
        validation = validation_data.get('validation', {})
        
        consistent = validation.get('consistent_claims', [])
        conflicting = validation.get('conflicting_claims', [])
        
        return {
            'confidence_score': validation.get('confidence_score', 'Unknown'),
            'consistent_claims': self._format_claims(consistent),
            'conflicting_claims': self._format_conflicts(conflicting),
            'total_consistent': len(consistent),
            'total_conflicting': len(conflicting),
            'status': validation_data.get('status', 'unknown')
        }
    
    def _format_claims(self, claims):
        """Format consistent claims."""
        formatted = []
        for claim in claims:
            formatted.append({
                'claim': self._clean_text(claim.get('claim', '')),
                'supporting_methods': claim.get('supporting_methods', []),
                'evidence_count': claim.get('evidence_count', 0),
                'type': claim.get('type', 'general')
            })
        return formatted
    
    def _format_conflicts(self, conflicts):
        """Format conflicting claims."""
        formatted = []
        for conflict in conflicts:
            formatted.append({
                'claim': self._clean_text(conflict.get('claim', '')),
                'supporting_methods': conflict.get('supporting_methods', []),
                'opposing_methods': conflict.get('opposing_methods', []),
                'type': conflict.get('type', 'general'),
                'description': self._clean_text(conflict.get('description', ''))
            })
        return formatted
    
    def _format_research_gaps(self, gap_data):
        """Format research gaps for display."""
        gaps = gap_data.get('research_gaps', [])
        
        # Categorize gaps
        categorized_gaps = {
            'methodological': [],
            'data_related': [],
            'scalability': [],
            'evaluation': [],
            'other': []
        }
        
        for gap in gaps:
            gap_lower = gap.lower()
            if any(term in gap_lower for term in ['method', 'approach', 'algorithm', 'model']):
                categorized_gaps['methodological'].append(self._clean_text(gap))
            elif any(term in gap_lower for term in ['data', 'dataset', 'benchmark']):
                categorized_gaps['data_related'].append(self._clean_text(gap))
            elif any(term in gap_lower for term in ['scale', 'efficiency', 'computational', 'resource']):
                categorized_gaps['scalability'].append(self._clean_text(gap))
            elif any(term in gap_lower for term in ['evaluation', 'metric', 'benchmark', 'comparison']):
                categorized_gaps['evaluation'].append(self._clean_text(gap))
            else:
                categorized_gaps['other'].append(self._clean_text(gap))
        
        return {
            'total_gaps': len(gaps),
            'all_gaps': [self._clean_text(g) for g in gaps],
            'categorized': categorized_gaps,
            'status': gap_data.get('status', 'unknown')
        }
    
    def _format_research_ideas(self, ideation_data):
        """Format research ideas for display."""
        ideas = ideation_data.get('research_ideas', [])
        
        formatted_ideas = []
        for i, idea in enumerate(ideas, 1):
            formatted_ideas.append({
                'id': i,
                'idea': self._clean_text(idea.get('idea', '')),
                'gap_addressed': self._clean_text(idea.get('gap_addressed', '')),
                'proposed_method': self._clean_text(idea.get('proposed_method', '')),
                'impact': self._clean_text(idea.get('impact', '')),
                'feasibility': self._clean_text(idea.get('feasibility', 'Unknown'))
            })
        
        # Categorize by impact level
        high_impact = [i for i in formatted_ideas if 'high' in i['impact'].lower()]
        medium_impact = [i for i in formatted_ideas if 'medium' in i['impact'].lower()]
        
        return {
            'total_ideas': len(formatted_ideas),
            'all_ideas': formatted_ideas,
            'high_impact_ideas': high_impact,
            'medium_impact_ideas': medium_impact,
            'top_recommendation': formatted_ideas[0] if formatted_ideas else None,
            'status': ideation_data.get('status', 'unknown')
        }
    
    def _generate_summary(self, all_agent_data):
        """Generate executive summary of the analysis."""
        retrieval = all_agent_data.get('retrieval', {})
        extraction = all_agent_data.get('extraction', {})
        comparison = all_agent_data.get('comparison', {})
        gap = all_agent_data.get('gap_analysis', {})
        ideation = all_agent_data.get('ideation', {})
        
        papers_count = retrieval.get('papers_found', 0)
        methods_count = comparison.get('total_methods', 0)
        gaps_count = gap.get('gap_count', 0)
        ideas_count = ideation.get('idea_count', 0)
        
        summary_text = (
            f"Analyzed {papers_count} research papers from arXiv. "
            f"Identified {methods_count} distinct methodological approaches. "
            f"Discovered {gaps_count} research gaps and generated {ideas_count} actionable research ideas."
        )
        
        return {
            'text': summary_text,
            'statistics': {
                'papers_analyzed': papers_count,
                'methods_identified': methods_count,
                'gaps_found': gaps_count,
                'ideas_generated': ideas_count
            },
            'key_insights': self._extract_key_insights(all_agent_data)
        }
    
    def _extract_key_insights(self, all_agent_data):
        """Extract key insights from the analysis."""
        insights = []
        
        # Best performing method
        comparison = all_agent_data.get('comparison', {})
        best_method = comparison.get('method_comparison', {}).get('best_performing', '')
        if best_method and 'insufficient' not in best_method.lower():
            insights.append(f"Best performing approach: {best_method}")
        
        # Validation confidence
        validation = all_agent_data.get('validation', {})
        confidence = validation.get('validation', {}).get('confidence_score', '')
        if confidence:
            insights.append(f"Claim validation: {confidence}")
        
        # Top research opportunity
        ideation = all_agent_data.get('ideation', {})
        ideas = ideation.get('research_ideas', [])
        if ideas:
            top_idea = ideas[0].get('idea', '')
            if top_idea:
                insights.append(f"Top research opportunity: {top_idea}")
        
        return insights
    
    def _generate_metadata(self, all_agent_data):
        """Generate metadata about the analysis."""
        return {
            'timestamp': self.timestamp,
            'query': all_agent_data.get('retrieval', {}).get('query', ''),
            'agents_executed': [
                'Retrieval Agent',
                'Extraction Agent',
                'Comparison Agent',
                'Validation Agent',
                'Gap Analysis Agent',
                'Ideation Agent',
                'Output Agent'
            ],
            'pipeline_status': 'completed',
            'version': '1.0.0'
        }
    
    def _clean_text(self, text):
        """Clean and normalize text."""
        if not text:
            return ''
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove newlines
        text = text.replace('\n', ' ').replace('\r', '')
        
        return text.strip()
    
    def _truncate_text(self, text, max_length):
        """Truncate text to maximum length."""
        text = self._clean_text(text)
        
        if len(text) <= max_length:
            return text
        
        return text[:max_length].rsplit(' ', 1)[0] + '...'
