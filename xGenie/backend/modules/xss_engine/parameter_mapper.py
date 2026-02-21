class ParameterMapper:
    def __init__(self):
        self.attack_surface = []
    
    def map_parameters(self, endpoints):
        """
        Map all injectable parameters from discovered endpoints
        """
        
        for endpoint in endpoints:
            # URL parameters
            if endpoint.get('parameters'):
                for param in endpoint['parameters']:
                    self.attack_surface.append({
                        'url': endpoint['url'],
                        'method': 'GET',
                        'parameter': param['name'],
                        'location': 'url',
                        'original_value': param['value']
                    })
            
            # Form parameters
            if endpoint.get('forms'):
                for form in endpoint['forms']:
                    for input_field in form.get('inputs', []):
                        # Skip CSRF tokens and passwords
                        if any(skip in input_field['name'].lower() for skip in ['csrf', 'token', 'password', 'pass']):
                            continue
                        
                        self.attack_surface.append({
                            'url': form['action'],
                            'method': form['method'],
                            'parameter': input_field['name'],
                            'location': 'form',
                            'input_type': input_field['type'],
                            'original_value': input_field['value']
                        })
        
        return self.attack_surface
