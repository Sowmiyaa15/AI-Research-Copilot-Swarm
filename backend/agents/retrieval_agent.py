import requests
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetrievalAgent:
    ARXIV_API_URL = 'http://export.arxiv.org/api/query'
    
    def __init__(self):
        self.max_results = 5
    
    def process(self, query):
        """
        Retrieve research papers from arXiv API based on user query.
        
        Args:
            query (str): Research topic to search for
            
        Returns:
            dict: Structured JSON with papers list
        """
        try:
            logger.info(f"Starting retrieval for query: {query}")
            
            # Query arXiv API
            papers = self._query_arxiv(query)
            
            logger.info(f"Successfully retrieved {len(papers)} papers")
            
            return {
                'agent': 'Retrieval Agent',
                'status': 'completed',
                'query': query,
                'papers_found': len(papers),
                'papers': papers,
                'message': f"Retrieved {len(papers)} papers from arXiv"
            }
            
        except requests.RequestException as e:
            logger.error(f"Network error during arXiv API request: {str(e)}")
            return {
                'agent': 'Retrieval Agent',
                'status': 'error',
                'query': query,
                'papers_found': 0,
                'papers': [],
                'message': f"Network error: {str(e)}"
            }
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {str(e)}")
            return {
                'agent': 'Retrieval Agent',
                'status': 'error',
                'query': query,
                'papers_found': 0,
                'papers': [],
                'message': f"Failed to parse API response: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                'agent': 'Retrieval Agent',
                'status': 'error',
                'query': query,
                'papers_found': 0,
                'papers': [],
                'message': f"Unexpected error: {str(e)}"
            }
    
    def _query_arxiv(self, query):
        """Query arXiv API and return top papers."""
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': self.max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        logger.info(f"Querying arXiv API with params: {params}")
        
        response = requests.get(self.ARXIV_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        return self._parse_response(response.text)
    
    def _parse_response(self, xml_data):
        """Parse arXiv API XML response and extract paper details."""
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        entries = root.findall('atom:entry', ns)
        
        logger.info(f"Parsing {len(entries)} entries from API response")
        
        for entry in entries:
            try:
                paper = {
                    'title': self._get_text(entry, 'atom:title', ns).strip().replace('\n', ' '),
                    'authors': ', '.join([
                        author.find('atom:name', ns).text 
                        for author in entry.findall('atom:author', ns)
                    ]),
                    'abstract': self._get_text(entry, 'atom:summary', ns).strip().replace('\n', ' '),
                    'url': self._get_text(entry, 'atom:id', ns)
                }
                papers.append(paper)
                logger.debug(f"Parsed paper: {paper['title'][:50]}...")
            except Exception as e:
                logger.warning(f"Failed to parse entry: {str(e)}")
                continue
        
        return papers
    
    def _get_text(self, element, path, namespace):
        """Safely extract text from XML element."""
        found = element.find(path, namespace)
        return found.text if found is not None else ''
