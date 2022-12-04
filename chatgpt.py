from playwright.sync_api import sync_playwright
import os
import time
from dotenv import load_dotenv

load_dotenv()

PLAY = sync_playwright().start()
BROWSER = PLAY.chromium.launch_persistent_context(
    user_data_dir="/tmp/playwright",
    headless=False,
)
PAGE = BROWSER.new_page()


def get_input_box():
    """Get the child textarea of `PromptTextarea__TextareaWrapper`"""
    return PAGE.query_selector("div[class*='PromptTextarea__TextareaWrapper']").query_selector("textarea")


def is_logged_in():
    try:
        # See if we have a textarea with data-id="root"
        return get_input_box() is not None
    except AttributeError:
        return False


def ask(question):
    get_input_box().fill(question)
    # Click the send message button
    PAGE.click("button[class*='PromptTextarea__PositionSubmit']")
    # Get the first message
    PAGE.wait_for_selector(
        "div[class*='request-:R2dm:-0 markdown prose dark:prose-invert break-words light']")
    answer = PAGE.query_selector(
        "div[class*='request-:R2dm:-0 markdown prose dark:prose-invert break-words light']").inner_text()
    print("Asked")
    print(answer)
    return answer


def prompt():
    prompt_message = "What is python?"
    get_input_box().fill(prompt_message)
    # Click the send message button
    PAGE.click("button[class*='PromptTextarea__PositionSubmit']")
    # Get the first message
    PAGE.wait_for_selector(
        "div[class*='request-:R2dm:-0 markdown prose dark:prose-invert break-words light']")
    print("Prompted")
    print(PAGE.query_selector(
        "div[class*='request-:R2dm:-0 markdown prose dark:prose-invert break-words light']").inner_text())


def login():
    PAGE.click("button[class*='btn-primary']")
    PAGE.wait_for_selector("input[name='username']")
    # fill in the email and password
    PAGE.fill("input[name='username']", os.getenv("OPENAI_EMAIL"))
    # Click the continue button
    PAGE.click("button[name='action']")
    PAGE.fill("input[name='password']", os.getenv("OPENAI_PASSWORD"))
    # click the login button
    PAGE.click("button[name='action']")
    # wait for the login to complete
    PAGE.wait_for_selector("div[class*='PromptTextarea__TextareaWrapper']")
    print("Logged in")


def wait():
    while True:
        time.sleep(1)


def start_browser():
    PAGE.goto("https://chat.openai.com/")
    if not is_logged_in():
        login()
    else:
        print("Logged in")
        prompt()
        # wait()


if __name__ == '__main__':
    start_browser()
