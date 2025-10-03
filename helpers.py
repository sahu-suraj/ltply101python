import os
import json
import urllib
import subprocess
from playwright.async_api import async_playwright, Page, Playwright

capabilities = {
    "browserName": "Chrome",
    "browserVersion": "latest",
    "LT:Options": {
        "platform": "Windows 10",
        "build": "Playwright Python Build",
        'user': 'surajsahu124',
        'accessKey': 'JYvphyRIMkzZI44wLeVZB3PHOSKcP7oqdkFYSQccX8YLShY6vx',
        "network": True,
        "video": True,
        "console": True,
        "tunnel": False,
        "tunnelName": "",
        "geoLocation": "",
    },
}

async def set_test_status(page: Page, status: str, remark: str):
    action_dict = {
        "action": "setTestStatus",
        "arguments": {"status": status, "remark": remark},
    }
    await page.evaluate("_ => {}", json.dumps({"lambdatest_action": action_dict}))

async def get_lambdatest_browser(playwright: Playwright, test_name: str):
    # Set Playwright version and test name
    playwright_version = str(subprocess.getoutput("playwright --version")).strip().split(" ")[1]
    capabilities["LT:Options"]["playwrightClientVersion"] = playwright_version
    capabilities["LT:Options"]["name"] = test_name

    lt_cdp_url = "wss://cdp.lambdatest.com/playwright?capabilities=" + urllib.parse.quote(json.dumps(capabilities))
    browser = await playwright.chromium.connect(lt_cdp_url, timeout=120000)
    page = await browser.new_page()
    return browser, page
