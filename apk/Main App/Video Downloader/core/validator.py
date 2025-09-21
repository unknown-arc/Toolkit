
from urllib.parse import urlparse

class url_validator:

    def validate_url(self, url: str) -> bool:

            """Validate the provided URL."""
        
            try:
                result = urlparse(url)
                return all([result.scheme, result.netloc])
            except (ValueError, AttributeError):
                return False
            
if __name__ == "__main__":
    validator = url_validator()
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    if validator.validate_url(test_url):
        print(f"✅ Valid URL: {test_url}")
    else:
        print(f"❌ Invalid URL: {test_url}")        