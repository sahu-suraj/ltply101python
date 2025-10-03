import asyncio
from playwright.async_api import async_playwright
from helpers import set_test_status, get_lambdatest_browser

async def test_slider():
    async with async_playwright() as playwright:
        browser, page = await get_lambdatest_browser(playwright, "Slider Test")
        try:
            await page.goto("https://www.lambdatest.com/selenium-playground")
            await page.click("text=Drag & Drop Sliders")
            slider = page.locator("input[type='range'][value='15']")
            await slider.fill("95")
            value_box = page.locator("#rangeSuccess")
            actual_value = await value_box.text_content()

            if actual_value == "95":
                await set_test_status(page, "passed", "Slider test passed")
                print("✅ Slider Test Passed")
            else:
                await set_test_status(page, "failed", f"Slider test failed: got {actual_value}")
                print(f"❌ Slider Test Failed")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_slider())
