import json
import urllib.parse

LT_USERNAME = ''
LT_ACCESS_KEY = ''


async def set_test_status(page, status, remark):
    script = (
        'lambdatest_action: '
        + json.dumps({
            "action": "setTestStatus",
            "arguments": {"status": status, "remark": remark}
        })
    )
    await page.evaluate("_ => {}", script)


async def get_lambdatest_browser(
    playwright,
    test_name="Playwright Test",
    browser_name="pw-chromium",
    browser_version="latest",
    platform="Windows 10"
):
    """
    Launch a browser on LambdaTest via Playwright WebSocket connection.
    Supports:
      - Windows 10 Chrome (pw-chromium)
      - Windows 10 Edge (MicrosoftEdge)
      - macOS Firefox (pw-firefox)
    """

    browser_name_lower = browser_name.lower()
    if browser_name_lower == "pw-chromium":
        lt_browser_name = "pw-chromium"
        engine = playwright.chromium
    elif browser_name_lower == "pw-firefox":
        lt_browser_name = "pw-firefox"
        engine = playwright.firefox
    elif browser_name_lower == "microsoftedge":
        lt_browser_name = "MicrosoftEdge"
        engine = playwright.chromium  # Edge runs on Chromium engine
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    capabilities = {
        "browserName": lt_browser_name,
        "browserVersion": browser_version,
        "LT:Options": {
            "platform": platform,
            "build": "Playwright Python Parallel Build",
            "name": test_name,
            "user": LT_USERNAME,
            "accessKey": LT_ACCESS_KEY,
            "network": True,
            "video": True,
            "console": True,
        }
    }

    caps_encoded = urllib.parse.quote(json.dumps(capabilities))
    ws_endpoint = f"wss://cdp.lambdatest.com/playwright?capabilities={caps_encoded}"

    browser = await engine.connect(ws_endpoint, timeout=60000)
    context = await browser.new_context(
    viewport={"width": 1920, "height": 1080}
)
    page = await context.new_page()

    return browser, page
