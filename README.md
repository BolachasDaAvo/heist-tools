A set of AI-based tools to improve your heisting experience in PoE. 
At the moment, only automatic price-checking of unusual gems is supported.

## How to Run
1. Download [Tesseract](https://github.com/tesseract-ocr/tesseract).
2. Install dependencies.
```bash
> pip install -r requeriments.txt
```
3. Update price database (you should repeat this step every day to have the most up-to-date data).
```bash
> python update_prices.py
```
4. Run the price checker script.
```bash
> python get_price.py
```
5. <kbd>Ctrl</kbd> + <kbd>a</kbd> on the Unusual Gem to print the corresponding price.
6. <kbd>Ctrl</kbd> + <kbd>m</kbd> to exit the application.