import asyncio
from playwright.async_api import async_playwright
import test_simple_form, test_slider, test_input_form

# Only supported combinations
TEST_COMBINATIONS = [
    (test_simple_form.test_simple_form, "pw-chromium", "latest", "Windows 10"),
    (test_slider.test_slider, "MicrosoftEdge", "latest", "Windows 10"),
    (test_input_form.test_input_form, "pw-chromium", "latest", "macOS 13"),
]

async def run_test_on_browser(playwright, test_func, browser_name, version, platform):
    try:
        print(f"🚀 Running {test_func.__name__} on {browser_name} {version} {platform}")
        await test_func(playwright, browser_name, version, platform)
    except Exception as e:
        print(f"❌ Error running {test_func.__name__} on {browser_name} {platform}: {e}")

async def main():
    async with async_playwright() as playwright:
        tasks = [
            run_test_on_browser(playwright, test_func, browser_name, version, platform)
            for test_func, browser_name, version, platform in TEST_COMBINATIONS
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
