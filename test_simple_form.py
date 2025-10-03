import asyncio
from playwright.async_api import async_playwright
from helpers import set_test_status, get_lambdatest_browser

async def test_simple_form():
    async with async_playwright() as playwright:
        browser, page = await get_lambdatest_browser(playwright, "Simple Form Demo Test")
        try:
            await page.goto("https://www.lambdatest.com/selenium-playground")
            await page.click("text=Simple Form Demo")
            message = "Welcome to LambdaTest"
            await page.fill("input#user-message", message)
            await page.click("text=Get Checked Value")
            output_text = await page.inner_text("p#message")

            if output_text == message:
                await set_test_status(page, "passed", "Simple Form test passed")
                print("✅ Simple Form Test Passed")
            else:
                await set_test_status(page, "failed", f"Expected '{message}', got '{output_text}'")
                print("❌ Simple Form Test Failed")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_simple_form())
