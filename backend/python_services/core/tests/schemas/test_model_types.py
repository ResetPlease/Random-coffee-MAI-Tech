import pytest
from schemas.model_types import xss_injection_validate



class TestXXSIngection:
    
    
    @staticmethod
    def test_detect_xss_threats() -> None:
        dangerous_cases = [
            '<script>alert("XSS")</script>',
            '<script type="text/javascript">>alert("XSS")</script>',
            '<  script  >alert(1)<  /  script  >',
            '<iframe src="dengerous-site.com"></iframe>',
            '<IMG SRC="javascript:alert(1)">',
            '<svg onload=alert(1)>',
            '<body onload="alert(1)">',
            '<input type="text" name="name" onfocus="alert(1)">',
            '<link rel="stylesheet" href="data:text/css,body{background:red}">',
            '<style>body {color: red;}</style>',
            '<div onclick="alert(1)">Click me</div>',
            '<a href="dengerous.html" onmouseover="alert(1)">Link</a>',
            '<form action="javascript:alert(1)"></form>',
            '<button onfocus=alert(1)>Submit</button>',
            '<div onclick="alert(1)" >',
            '<div ONMOUSEOVER="dengerous()" >',
            "<div onload='dengerous()'>",
            'javascript:alert(document.cookie)',
            'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
            'data:application/x-shockwave-flash,dengerous',
            'eval("alert(1)")',
            'window.eval("something")',
            '<a href="javascript:alert(1)" onmouseover="alert(2)">Click</a>',
            '<div onclick="alert(1)">',
            '<img onerror="malicious()">',
            '<a onmouseover=\'alert("XSS")\'>Link</a>', 
        ]

        for input in dangerous_cases:
            with pytest.raises(ValueError):
                xss_injection_validate(input)


    @staticmethod
    def test_accept_safe_input():
        safe_cases = [
                'Hello World!',
                'This is a safe line without tags and scripts.',
                'http://example.com/path?param=value',
                'user@example.com',
                '<notlistedtag>No closing tag', 
                'Processor: normalOnClick()',
                'Valid JSON: {"key": "value"}',
                'String with symbols: !@#$%^&*()',
                'onion=vegetable',   
                'evalutation',      
                'alertness',         
                'data_point', 
                'console.log("Logging");',
                'background: url("http://example.com/image.png");',
            ]
        for input in safe_cases:
            assert xss_injection_validate(input) == input


    @staticmethod
    def test_case_insensitivity():
        with pytest.raises(ValueError):
            xss_injection_validate('<SCRIPT>alert(1)</SCRIPT>')  
        with pytest.raises(ValueError):
            xss_injection_validate('JaVaScRiPt:alert(1)')      
            
            
            