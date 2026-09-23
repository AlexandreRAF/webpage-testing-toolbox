from html.parser import HTMLParser

class WCAG22_1_1(HTMLParser):
    criterion = '1.1.1'

    def __init__(self):
        super().__init__()
        self.results = []

    def validate(self, html):
        self.reset()
        self.results = []
        self.feed(html)
        self.close()
        return self.results

    def handle_starttag(self, tag, attrs):  
        if tag == 'img':
            has_alt = False
            for name, value in attrs:
                if name == 'alt':
                    has_alt = True
                    break
            if not has_alt:
                self.results.append({
                    'tag': tag,
                    'message': 'Missing alt text attribute',
                    'code': self.get_starttag_text()
                })
        elif tag in ('svg', 'canvas', 'audio', 'video'):
            has_label = False
            for name, value in attrs:
                if name in ('aria-label', 'aria-labelledby'):
                    has_label = True
                    break
            if not has_label:
                self.results.append({
                    'tag': tag,
                    'message': 'Missing aria-label/aria-labelledby attribute',
                    'code': self.get_starttag_text()
                })
        else:
            # This is less reliable: unmarked graphics are missed, and label presence alone does not guarantee a valid text alternative.
            for name, value in attrs:
                if name == 'role' and value == 'img':
                    has_label = False
                    for label_name, label_value in attrs:
                        if label_name in ('aria-label', 'aria-labelledby'):
                            has_label = True
                            break
                    if not has_label:
                        self.results.append({
                            'tag': tag,
                            'message': 'Possible missing aria-label/aria-labelledby attribute',
                            'code': self.get_starttag_text()
                        })
                    break

# Add future checker classes here. Each class must provide criterion and validate(html).
CHECKERS = [WCAG22_1_1]
