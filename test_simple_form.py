from helpers import get_lambdatest_browser, set_test_status

async def test_simple_form(playwright, browser_name, version, platform):
    browser, page = await get_lambdatest_browser(
        playwright, "Simple Form Test", browser_name, version, platform
    )
    try:
        await page.goto("https://www.lambdatest.com/selenium-playground")
        slider_page_link = page.locator("text=Simple Form Demo")
        await slider_page_link.scroll_into_view_if_needed()
        await slider_page_link.click()
        await page.wait_for_timeout(1000) 

        await page.fill("#user-message", "Hello LambdaTest")
        await page.click("#showInput")
        text = await page.text_content("#message")
        if text.strip() == "Hello LambdaTest":
            await set_test_status(page, "passed", "Simple Form Test Passed")
            print(f"✅ Simple Form Test Passed on {browser_name} {platform}")
        else:
            await set_test_status(page, "failed", f"Expected 'Hello LambdaTest' but got '{text}'")
            print(f"❌ Simple Form Test Failed on {browser_name} {platform}")
    except Exception as e:
        await set_test_status(page, "failed", str(e))
        print(f"❌ Simple Form Test Error on {browser_name} {platform}: {e}")
    finally:
        await browser.close()
