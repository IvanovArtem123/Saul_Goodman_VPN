import requests
from http.cookiejar import CookieJar

URL = 'https://soul-goodman.space:8443/qgwcqFXkhD6gxZqHlT/panel/api/inbounds/get/1'
data = {
    'username': 'V8Y21-!fvwdhg9G',
    'password': '4216GUYSA-!0@N#hf123'
}

cookie_jar = requests.cookies.RequestsCookieJar()
cookie_jar.set('3x-ui', 'MTc3NzQ5NDM0MHxEWDhFQVFMX2dBQUJFQUVRQUFCOV80QUFBUVp6ZEhKcGJtY01EQUFLVEU5SFNVNWZWVk5GVWpCbmFYUm9kV0l1WTI5dEwyMW9jMkZ1WVdWcEx6TjRMWFZwTDNZeUwyUmhkR0ZpWVhObEwyMXZaR1ZzTGxWelpYTF9nUU1CQVFSVmMyVnlBZi1DQUFFREFRSkpaQUVFQUFFSVZYTmxjbTVoYldVQkRBQUJDRkJoYzNOM2IzSmtBUXdBQUFCVl80SlNBUUlCRDFZNFdUSXhMU0ZtZG5ka2FHYzVSd0U4SkRKaEpERXdKSGhxY1d4cWR5NVhUR2RKY1VkcVJuRTNRVWt5TjA5elVtTjNTSGh6ZWpnek5VUlpiRzFJU0hWRUwyTnRTbnA1TUhOdlMxUjVBQT09fFfSvZj7GpM-FtoCWhGYygJOpf2beR9t62yLCPlxu4nO', 
                     domain='soul-goodman.space', 
                     path='/')

# Используем куки в запросе
response = requests.get(URL, json=data, cookies=cookie_jar)
print(response.text)