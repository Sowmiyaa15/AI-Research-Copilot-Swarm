class ResearchQuery:
    def __init__(self, query, results=None):
        self.query = query
        self.results = results or {}
    
    def to_dict(self):
        return {
            'query': self.query,
            'results': self.results
        }
