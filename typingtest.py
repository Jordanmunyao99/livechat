import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pynput import keyboard

# Setup Chrome options
chrome_options = Options()

chrome_options.add_argument("--window-size=1920x1080")

# Initialize driver
driver = webdriver.Chrome(options=chrome_options)

# Global flag to track if Shift key was pressed
shift_pressed = False

def on_press(key):
    """Callback for key press events"""
    global shift_pressed
    try:
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            shift_pressed = True
            return False  # Stop listener
    except AttributeError:
        pass

def wait_for_shift_key():
    """Wait for user to press Shift key"""
    global shift_pressed
    shift_pressed = False
    
    print("\n" + "="*50)
    print("PRESS SHIFT KEY TO START TYPING")
    print("="*50 + "\n")
    
    # Start listening for keyboard events
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    
    print("Shift key pressed! Starting typing test...")
    time.sleep(0.5)

def debug_page_structure():
    """Debug function to see what elements are on the page"""
    try:
        # Get all elements with tst-input-wrapper class
        containers = driver.find_elements(By.CLASS_NAME, "tst-input-wrapper")
        print(f"\nFound {len(containers)} tst-input-wrapper containers")
        
        for i, container in enumerate(containers):
            print(f"\nContainer {i}:")
            print(f"  HTML: {container.get_attribute('outerHTML')[:200]}")
            print(f"  Text: {container.text[:100]}")
            
            # Find spans in this container
            spans = container.find_elements(By.TAG_NAME, "span")
            print(f"  Found {len(spans)} span elements")
            for j, span in enumerate(spans[:5]):  # Show first 5
                print(f"    Span {j}: '{span.text}' - class: {span.get_attribute('class')}")
    except Exception as e:
        print(f"Debug error: {e}")

def wait_for_test_start():
    """Wait for the typing test to be ready"""
    try:
        # Wait for the input box to be present
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "test-input"))
        )
        return input_box
    except TimeoutException:
        print("Timed out waiting for test to load")
        return None

def get_all_visible_words():
    """Get all visible words on screen using JavaScript"""
    try:
        # Use JavaScript to find the words display area
        script = """
        var words = [];
        var containers = document.querySelectorAll('.tst-input-wrapper');
        
        // The SECOND container (index 1) has the words to type
        if (containers.length > 1) {
            var spans = containers[1].querySelectorAll('span');
            spans.forEach(function(span) {
                if (span.innerText && span.innerText.trim()) {
                    words.push(span.innerText.trim());
                }
            });
        }
        return words;
        """
        words = driver.execute_script(script)
        return words
    except Exception as e:
        print(f"Error in get_all_visible_words: {e}")
        return []

def get_current_word_js():
    """Get the current word using JavaScript"""
    try:
        script = """
        var containers = document.querySelectorAll('.tst-input-wrapper');
        if (containers.length > 1) {
            var spans = containers[1].querySelectorAll('span');
            if (spans.length > 0) {
                return spans[0].innerText.trim();
            }
        }
        return null;
        """
        return driver.execute_script(script)
    except Exception as e:
        print(f"Error getting current word: {e}")
        return None

def type_with_human_delay(text, input_box):
    """Type text with human-like delays between keystrokes"""
    for char in text:
        input_box.send_keys(char)
        # Random delay between 0.05 and 0.15 seconds (human-like typing)
        delay = random.uniform(0.04, 0.09)
        time.sleep(delay)

def main():
    url = "https://www.livechat.com/typing-speed-test/#/"
    driver.get(url)
    
    print("Waiting for page to load...")
    time.sleep(5)  # Give more time for React to render
    
    # Debug: Check page structure
    print("\n=== DEBUGGING PAGE STRUCTURE ===")
    debug_page_structure()
    print("=== END DEBUG ===\n")
    
    # Wait for the input box
    input_box = wait_for_test_start()
    if not input_box:
        print("Could not find input box")
        driver.quit()
        return
    
    print("Clicking input box to start test...")
    input_box.click()
    time.sleep(2)
    
    # Check words again after clicking
    print("\n=== CHECKING AFTER CLICK ===")
    debug_page_structure()
    words = get_all_visible_words()
    print(f"Words found: {words[:10]}")
    print("=== END CHECK ===\n")
    
    # Wait for user to press Shift key before starting
    wait_for_shift_key()
    
    # Test duration (60 seconds typical)
    test_duration = 60
    start_time = time.time()
    
    print("Starting typing test...")
    
    word_count = 0
    last_word = None
    
    while time.time() - start_time < test_duration:
        # Get current word
        current_word = get_current_word_js()
        
        if not current_word:
            print("No word found")
            time.sleep(0.5)
            
            # Check if test ended
            if word_count > 0:
                print("Test may have ended")
                break
            continue
        
        # Skip if it's the same word as last time (already typed)
        if current_word == last_word:
            time.sleep(0.1)
            continue
        
        print(f"Word #{word_count + 1}: '{current_word}'")
        
        # Type the word
        type_with_human_delay(current_word, input_box)
        
        # Add space after word
        input_box.send_keys(" ")
        time.sleep(random.uniform(0.1, 0.3))
        
        last_word = current_word
        word_count += 1
        
        # Small pause
        time.sleep(0.01)

    print(f"\nTest completed! Typed {word_count} words")
    print("\n" + "="*50)
    print("WINDOW WILL REMAIN OPEN FOR 50 SECONDS")
    print("Take your screenshot now!")
    print("="*50 + "\n")
    
    # Wait 600 seconds before closing
    for remaining in range(600, 0, -1):
        print(f"Closing in {remaining} seconds...", end='\r')
        time.sleep(1)
    
    print("\nClosing browser...")
    driver.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        driver.quit()
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        driver.quit()