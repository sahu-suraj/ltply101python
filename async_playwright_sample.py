import os
import json
import urllib
import asyncio
import subprocess

from playwright._impl._page import Page
from playwright.async_api import async_playwright
from playwright.async_api._generated import Playwright

capabilities = {
    "browserName": "Chrome",  # Browsers allowed: `Chrome`, `MicrosoftEdge`, `pw-chromium`, `pw-firefox` and `pw-webkit`
    "browserVersion": "latest",
    "LT:Options": {
        "platform": "Linux",
        "build": "Playwright Python Build",
        "name": "Playwright Test",
        'user': 'surajsahu124',
        'accessKey': 'JYvphyRIMkzZI44wLeVZB3PHOSKcP7oqdkFYSQccX8YLShY6vx',
        "network": True,
        "video": True,
        "console": True,
        "tunnel": False,  # Add tunnel configuration if testing locally hosted webpage
        "tunnelName": "",  # Optional
        "geoLocation": "",  # country code can be fetched from https://www.lambdatest.com/capabilities-generator/
    },
}


async def run(playwright: Playwright):
    playwrightVersion = (
        str(subprocess.getoutput("playwright --version")).strip().split(" ")[1]
    )
    capabilities["LT:Options"]["playwrightClientVersion"] = playwrightVersion  # type: ignore

    lt_cdp_url = (
        "wss://cdp.lambdatest.com/playwright?capabilities="
        + urllib.parse.quote(json.dumps(capabilities))
    )
    browser = await playwright.chromium.connect(lt_cdp_url, timeout=120000)
    page: Page = await browser.new_page()  # type: ignore
    try:
        # 1. Open Selenium Playground
        await page.goto("https://www.lambdatest.com/selenium-playground")

        # 2. Click "Drag & Drop Sliders"
        await page.click("text=Drag & Drop Sliders")

        # 3. Locate slider with default value 15 and set to 95
        slider = page.locator("input[type='range'][value='15']")
        await slider.fill("95")  # directly set the value

        # 4. Validate the value
        value_box = page.locator("#rangeSuccess")
        actual_value = await value_box.text_content()
        if actual_value == "95":
            await set_test_status(page, "passed", "Slider successfully moved to 95")
            print("✅ Test Passed: Slider successfully moved to 95")
        else:
            await set_test_status(page, "failed", f"Expected 95, got {actual_value}")
            print(f"❌ Test Failed: Expected 95, got {actual_value}")

    except Exception as err:
        print("❌ Error:", err)
        await set_test_status(page, "failed", str(err))

    finally:
        await browser.close()


async def set_test_status(page: Page, status: str, remark: str):
    action_dict = {
        "action": "setTestStatus",
        "arguments": {"status": status, "remark": remark},
    }
    await page.evaluate(
        "_ => {}",
        json.dumps({"lambdatest_action": action_dict})
    )


async def run_playwright():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(run_playwright())
