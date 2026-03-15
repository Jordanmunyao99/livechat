# LiveChat Typing Speed Test Automation

A Python automation script for the [LiveChat Typing Speed Test](https://www.livechat.com/typing-speed-test/) that simulates human-like typing patterns to complete the 60-second typing challenge.

## Features

- ⌨️ **Automated Typing**: Completes the typing test automatically
- 🎯 **Human-like Speed**: Random delays between keystrokes (40-90ms)
- 🔍 **Smart Word Detection**: Dynamically fetches words from the page
- ⏱️ **60-Second Test**: Designed for the standard 1-minute typing test
- 🖱️ **Manual Start**: Press SHIFT to begin automation (prevents accidental runs)
- 📸 **Screenshot Time**: Window stays open for 10 minutes after completion
- 🐛 **Debug Mode**: Detailed console output for troubleshooting

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation

1. **Clone or download this repository**

2. **Install required Python packages:**
```bash
pip install selenium pynput
```

3. **Install ChromeDriver:**
   - Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
   - Download the version matching your Chrome browser
   - Add to system PATH or place in the same directory as the script

## Usage

### Basic Usage

1. **Run the script:**
```bash
python test.py
```

2. **Wait for the page to load** (the script will automatically open the LiveChat typing test)

3. **Review the debug information** displayed in the console

4. **Press SHIFT** when you're ready to start the automated typing

5. **Watch the automation complete the test** (takes ~60 seconds)

6. **Take your screenshot** - the window stays open for 10 minutes

7. **Press Ctrl+C** or wait for auto-close

### What Happens

```
Waiting for page to load...

=== DEBUGGING PAGE STRUCTURE ===
Found 2 tst-input-wrapper containers
...
=== END DEBUG ===

==================================================
PRESS SHIFT KEY TO START TYPING
==================================================

Shift key pressed! Starting typing test...

Word #1: 'hello'
Word #2: 'world'
Word #3: 'typing'
...

Test completed! Typed 95 words

==================================================
WINDOW WILL REMAIN OPEN FOR 50 SECONDS
Take your screenshot now!
==================================================
```

## Configuration

### Adjust Typing Speed

Modify the delay range in the `type_with_human_delay()` function:

```python
# Current: 40-90ms per character
delay = random.uniform(0.04, 0.09)

# Faster typing: 30-60ms
delay = random.uniform(0.03, 0.06)

# Slower typing: 60-120ms
delay = random.uniform(0.06, 0.12)
```

### Change Test Duration

Modify the `test_duration` variable in `main()`:

```python
# Current: 60 seconds
test_duration = 60

# For 30 seconds
test_duration = 30

# For 2 minutes
test_duration = 120
```

### Adjust Window Open Time

Change the countdown duration:

```python
# Current: 600 seconds (10 minutes)
for remaining in range(600, 0, -1):

# For 60 seconds
for remaining in range(60, 0, -1):

# For 5 minutes
for remaining in range(300, 0, -1):
```

## How It Works

1. **Page Load**: Opens LiveChat typing test and waits for elements to load
2. **Element Detection**: Finds the input box and word containers using CSS selectors
3. **Word Extraction**: Uses JavaScript to extract words from the second `.tst-input-wrapper` container
4. **Dynamic Typing**: 
   - Fetches the current word from the page
   - Types each character with randomized human-like delays
   - Adds a space after each word
   - Moves to the next word
5. **Completion Detection**: Stops after 60 seconds or when no more words are found
6. **Results Display**: Keeps browser open for screenshot/review

## Troubleshooting

### "Could not find input box"
- The page may not have loaded completely
- Increase the initial sleep time: `time.sleep(5)` → `time.sleep(10)`

### "No word found" repeatedly
- The word containers may have different class names
- Check the debug output for actual HTML structure
- Modify the JavaScript selectors in `get_current_word_js()`

### ChromeDriver errors
```bash
# Make sure ChromeDriver matches your Chrome version
chrome --version

# Download matching ChromeDriver from:
# https://chromedriver.chromium.org/downloads
```

### Script types same word repeatedly
- The page may not be updating the word list
- This is normal if the test has ended
- Check if 60 seconds have elapsed

### Import errors
```bash
# Upgrade pip first
pip install --upgrade pip

# Install packages individually
pip install selenium
pip install pynput
```

## Technical Details

### Word Detection Method

The script uses a two-container approach:
- Container 0: User's typed text
- Container 1: Words to be typed

Words are extracted using:
```javascript
var containers = document.querySelectorAll('.tst-input-wrapper');
var spans = containers[1].querySelectorAll('span');
```

### Typing Pattern

- **Base delay**: 40-90ms between characters
- **Word spacing**: 100-300ms after each word
- **Small pause**: 10ms between word iterations
- **Natural variation**: Random delays simulate human typing

## Limitations

- ⚠️ Only works with the LiveChat typing test website
- ⚠️ Requires the page structure to remain consistent
- ⚠️ May not work if the website updates its HTML structure
- ⚠️ Internet connection required

## Legal & Ethical Considerations

**⚠️ IMPORTANT DISCLAIMER:**

This script is provided for **educational and testing purposes only**.

- Automated testing may violate LiveChat's Terms of Service
- Results from automation should not be represented as genuine human performance
- Use responsibly and ethically
- Consider the implications of automation on typing test leaderboards
- The author is not responsible for misuse of this tool

## Contributing

Found a bug or want to improve the script? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is provided as-is under the MIT License.

## Acknowledgments

- Built with [Selenium WebDriver](https://www.selenium.dev/)
- Keyboard control via [pynput](https://pynput.readthedocs.io/)
- Designed for [LiveChat Typing Speed Test](https://www.livechat.com/typing-speed-test/)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the debug output in the console
3. Ensure ChromeDriver and Chrome versions match
4. Open an issue on GitHub with error details

---

**Note**: This tool is not affiliated with, endorsed by, or connected to LiveChat Inc. Use at your own discretion.
