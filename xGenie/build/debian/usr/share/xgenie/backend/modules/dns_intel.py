import dns.resolver
import dns.exception

class DNSIntel:
    def __init__(self, target):
        self.target = target
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5
    
    def gather(self):
        result = {
            'domain': self.target,
            'A': [],
            'AAAA': [],
            'MX': [],
            'NS': [],
            'TXT': [],
            'CNAME': [],
            'SOA': None,
            'spf': None,
            'dmarc': None,
            'dkim': None
        }
        
        # A Records
        try:
            answers = self.resolver.resolve(self.target, 'A')
            result['A'] = [str(rdata) for rdata in answers]
        except:
            pass
        
        # AAAA Records
        try:
            answers = self.resolver.resolve(self.target, 'AAAA')
            result['AAAA'] = [str(rdata) for rdata in answers]
        except:
            pass
        
        # MX Records
        try:
            answers = self.resolver.resolve(self.target, 'MX')
            result['MX'] = [f"{rdata.preference} {rdata.exchange}" for rdata in answers]
        except:
            pass
        
        # NS Records
        try:
            answers = self.resolver.resolve(self.target, 'NS')
            result['NS'] = [str(rdata) for rdata in answers]
        except:
            pass
        
        # TXT Records
        try:
            answers = self.resolver.resolve(self.target, 'TXT')
            txt_records = [str(rdata) for rdata in answers]
            result['TXT'] = txt_records
            
            # Parse SPF
            for txt in txt_records:
                if 'v=spf1' in txt.lower():
                    result['spf'] = txt
        except:
            pass
        
        # DMARC
        try:
            answers = self.resolver.resolve(f'_dmarc.{self.target}', 'TXT')
            for rdata in answers:
                txt = str(rdata)
                if 'v=DMARC1' in txt:
                    result['dmarc'] = txt
        except:
            pass
        
        # SOA
        try:
            answers = self.resolver.resolve(self.target, 'SOA')
            result['SOA'] = str(answers[0])
        except:
            pass
        
        # Clean empty values
        result = {k: v for k, v in result.items() if v}
        
        if len(result) <= 1:
            return {'error': 'Unable to retrieve DNS data'}
        
        return result
