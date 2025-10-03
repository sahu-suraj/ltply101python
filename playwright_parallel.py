import asyncio
from playwright.async_api import async_playwright
from helpers import set_test_status, get_lambdatest_browser

# the actual test function
async def simple_form_test(playwright, test_name, browser_name, browser_version, platform):
    browser, page = await get_lambdatest_browser(playwright, test_name, browser_name, browser_version, platform)
    try:
        await page.goto("https://www.lambdatest.com/selenium-playground")
        await page.click("text=Simple Form Demo")
        message = "Welcome to LambdaTest"
        await page.fill("input#user-message", message)
        await page.click("text=Get Checked Value")
        output_text = await page.inner_text("p#message")

        if output_text == message:
            await set_test_status(page, "passed", f"{test_name} passed")
            print(f"✅ {test_name} Passed")
        else:
            await set_test_status(page, "failed", f"Expected '{message}', got '{output_text}'")
            print(f"❌ {test_name} Failed")
    finally:
        await browser.close()


async def main():
    async with async_playwright() as playwright:
        # define browser/os combinations
        combos = [
            ("Win10-Chrome", "Chrome", "latest", "Windows 10"),
            ("Mac-Firefox", "pw-firefox", "latest", "macOS Catalina")
        ]

        tasks = [
            simple_form_test(playwright, test_name, browser, version, platform)
            for (test_name, browser, version, platform) in combos
        ]

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
