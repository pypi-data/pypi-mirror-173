# AutoBr: Auto Browser

A bot to control web browser actions

## Installation
```pip
pip install autobr
```

Download ChromeDriver [Chromium](https://chromedriver.chromium.org/downloads) or [GoogleAPIs](https://chromedriver.storage.googleapis.com/index.html?path=107.0.5304.62/) according to your computer's Chrome version.

### Example

```python
from autobr.bot import *

if __name__ == "__main__":
    bot = Bot(chromedriver_path='browsers/chromedriver.exe')
    bot.start()
    bot.open("https://pypi.org/")
    html=bot.get_html_str()
    print(html)
    bot.close()

```

## License
The `AutoBr` project is provided by [Donghua Chen](https://github.com/dhchenx). 

