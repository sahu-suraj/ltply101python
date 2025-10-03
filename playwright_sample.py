import json
import os
import urllib
import subprocess

from playwright.sync_api import sync_playwright

capabilities = {
    'browserName': 'Chrome',  # Browsers allowed: `Chrome`, `MicrosoftEdge`, `pw-chromium`, `pw-firefox` and `pw-webkit`
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': 'Windows 10',
        'build': 'Playwright Python Build',
        'name': 'Playwright Test',
        'user': 'surajsahu124',
        'accessKey': 'JYvphyRIMkzZI44wLeVZB3PHOSKcP7oqdkFYSQccX8YLShY6vx',
        'network': True,
        'video': True,
        'console': True,
        'tunnel': False,  # Add tunnel configuration if testing locally hosted webpage
        'tunnelName': '',  # Optional
        'geoLocation': '', # country code can be fetched from https://www.lambdatest.com/capabilities-generator/
    }
}

def run(playwright):
    playwrightVersion = str(subprocess.getoutput('playwright --version')).strip().split(" ")[1]
    capabilities['LT:Options']['playwrightClientVersion'] = playwrightVersion

    lt_cdp_url = 'wss://cdp.lambdatest.com/playwright?capabilities=' + urllib.parse.quote(
        json.dumps(capabilities))
    browser = playwright.chromium.connect(lt_cdp_url, timeout=120000)
    page = browser.new_page()
    try:

        # 2. Open Selenium Playground
        page.goto("https://www.lambdatest.com/selenium-playground")

            # 3. Click "Drag & Drop Sliders"
        page.click("text=Drag & Drop Sliders")

            # 4. Locate the slider with default value 15
        slider = page.locator("input[type='range'][value='15']")

            # 5. Drag slider → set to 95
        slider.fill("95")   # set directly if input is type=range

            # 6. Validate the value shows 95
        value_box = page.locator("#rangeSuccess")   # value is shown here
        expect(value_box).to_have_text("95")

        print("✅ Test Passed: Slider successfully moved to 95")
    except Exception as err:
        print("Error:: ", err)
        set_test_status(page, "failed", str(err))
    finally:
        page.wait_for_timeout(2000)  # let LT log final status
        try:
            page.close()
        except Exception:
            pass
        try:
            browser.close()
        except Exception:
            pass



def set_test_status(page, status, remark):
    page.evaluate("_ => {}",
                  "lambdatest_action: {\"action\": \"setTestStatus\", \"arguments\": {\"status\":\"" + status + "\", \"remark\": \"" + remark + "\"}}");


with sync_playwright() as playwright:
    run(playwright)
