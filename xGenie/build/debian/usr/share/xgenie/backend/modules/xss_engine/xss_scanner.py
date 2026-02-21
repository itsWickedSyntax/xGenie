from backend.modules.xss_engine.crawler import DynamicCrawler
from backend.modules.xss_engine.parameter_mapper import ParameterMapper
from backend.modules.xss_engine.reflection_tester import ReflectionTester
from backend.modules.xss_engine.dom_analyzer import DOMAnalyzer
from backend.modules.xss_engine.context_classifier import ContextClassifier
from backend.modules.xss_engine.risk_scorer import RiskScorer

class XSSScanner:
    def __init__(self, target):
        self.target = target
        if not target.startswith('http'):
            self.base_url = f'https://{target}'
        else:
            self.base_url = target
    
    def scan(self):
        result = {
            'target': self.base_url,
            'vulnerabilities': [],
            'tested_endpoints': 0,
            'tested_parameters': 0,
            'scan_summary': {}
        }
        
        try:
            # Phase 1: Dynamic Crawling
            print("  [XSS] Phase 1: Dynamic crawling...")
            crawler = DynamicCrawler(self.base_url)
            endpoints = crawler.crawl(max_depth=2, max_pages=20)
            result['tested_endpoints'] = len(endpoints)
            
            if not endpoints:
                return {'error': 'Unable to crawl target'}
            
            # Phase 2: Parameter Mapping
            print("  [XSS] Phase 2: Parameter mapping...")
            mapper = ParameterMapper()
            attack_surface = mapper.map_parameters(endpoints)
            result['tested_parameters'] = sum(len(e.get('parameters', [])) for e in attack_surface)
            
            # Phase 3: Reflection Testing
            print("  [XSS] Phase 3: Reflection testing...")
            tester = ReflectionTester()
            reflections = tester.test_reflections(attack_surface)
            
            # Phase 4: Context Classification
            print("  [XSS] Phase 4: Context classification...")
            classifier = ContextClassifier()
            classified = classifier.classify_contexts(reflections)
            
            # Phase 5: DOM Analysis
            print("  [XSS] Phase 5: DOM sink analysis...")
            dom_analyzer = DOMAnalyzer(self.base_url)
            dom_vulns = dom_analyzer.analyze_dom_sinks(endpoints)
            
            # Phase 6: Risk Scoring
            print("  [XSS] Phase 6: Risk scoring...")
            scorer = RiskScorer()
            
            # Process reflected XSS
            for item in classified:
                if item.get('reflected'):
                    risk = scorer.calculate_risk(item)
                    
                    vuln = {
                        'type': 'Reflected XSS',
                        'url': item['url'],
                        'parameter': item['parameter'],
                        'method': item['method'],
                        'context': item['context'],
                        'payload': item['payload'],
                        'risk_score': risk['score'],
                        'severity': risk['severity'],
                        'exploitability': risk['exploitability'],
                        'evidence': item.get('evidence', '')
                    }
                    result['vulnerabilities'].append(vuln)
            
            # Process DOM-based XSS
            for dom_vuln in dom_vulns:
                risk = scorer.calculate_risk(dom_vuln)
                
                vuln = {
                    'type': 'DOM-based XSS',
                    'url': dom_vuln['url'],
                    'sink': dom_vuln['sink'],
                    'source': dom_vuln.get('source', 'Unknown'),
                    'risk_score': risk['score'],
                    'severity': risk['severity'],
                    'exploitability': risk['exploitability'],
                    'evidence': dom_vuln.get('code_snippet', '')
                }
                result['vulnerabilities'].append(vuln)
            
            # Summary
            result['scan_summary'] = {
                'total_vulnerabilities': len(result['vulnerabilities']),
                'reflected_xss': sum(1 for v in result['vulnerabilities'] if v['type'] == 'Reflected XSS'),
                'dom_based_xss': sum(1 for v in result['vulnerabilities'] if v['type'] == 'DOM-based XSS'),
                'high_risk': sum(1 for v in result['vulnerabilities'] if v['severity'] == 'High'),
                'medium_risk': sum(1 for v in result['vulnerabilities'] if v['severity'] == 'Medium'),
                'low_risk': sum(1 for v in result['vulnerabilities'] if v['severity'] == 'Low')
            }
            
            return result
            
        except Exception as e:
            return {'error': f'Unable to complete XSS scan: {str(e)}'}
