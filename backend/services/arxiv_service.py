import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

class ArxivService:
    BASE_URL = 'http://export.arxiv.org/api/query'
    
    def search(self, query, max_results=10):
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results
        }
        
        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read().decode('utf-8')
            
            return self._parse_response(data)
        except Exception as e:
            return {'error': str(e), 'papers': []}
    
    def _parse_response(self, xml_data):
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            paper = {
                'title': entry.find('atom:title', ns).text.strip(),
                'summary': entry.find('atom:summary', ns).text.strip(),
                'authors': [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)],
                'published': entry.find('atom:published', ns).text,
                'link': entry.find('atom:id', ns).text
            }
            papers.append(paper)
        
        return {'papers': papers}
