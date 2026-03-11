from playwright.sync_api import sync_playwright


def capture_chart(symbol):

    url = f"https://www.tradingview.com/chart/?symbol=BINANCE:{symbol}"

    filename = f"{symbol}.png"

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url)

        page.wait_for_timeout(8000)

        page.screenshot(path=filename)

        browser.close()

    return filename
