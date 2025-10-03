from helpers import get_lambdatest_browser, set_test_status

async def test_input_form(playwright, browser_name, version, platform):
    browser, page = await get_lambdatest_browser(
        playwright, "Input Form Submit Test", browser_name, version, platform
    )
    try:
        await page.goto("https://www.lambdatest.com/selenium-playground/input-form-demo")
        await page.fill("input[name='name']", "John Doe")
        await page.fill("input[name='email']", "johndoe@example.com")
        await page.fill("input[name='password']", "Password123")
        await page.fill("input[name='company']", "LambdaTest")
        await page.fill("input[name='website']", "www.lambdatest.com")
        await page.select_option("select[name='country']", label="United States")
        await page.fill("input[name='city']", "New York")
        await page.fill("input[name='address1']", "123 Test Street")
        await page.fill("input[name='address2']", "Suite 45")
        await page.fill("input[name='state']", "NY")
        await page.fill("input[name='zip']", "10001")
        await page.click("button:has-text('Submit')")

        success_msg = await page.text_content("p.success-msg")
        if success_msg.strip() == "Thanks for contacting us, we will get back to you shortly.":
            await set_test_status(page, "passed", "Input Form Test Passed")
            print(f"✅ Input Form Test Passed on {browser_name} {platform}")
        else:
            await set_test_status(page, "failed", f"Unexpected message: {success_msg}")
            print(f"❌ Input Form Test Failed on {browser_name} {platform}")
    except Exception as e:
        await set_test_status(page, "failed", str(e))
        print(f"❌ Input Form Error on {browser_name} {platform}: {e}")
    finally:
        await browser.close()
