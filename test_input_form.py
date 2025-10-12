from helpers import get_lambdatest_browser, set_test_status

async def test_input_form(playwright, browser_name, version, platform):
    browser, page = await get_lambdatest_browser(
        playwright, "Input Form Submit Test", browser_name, version, platform
    )
    try:
        await page.goto("https://www.lambdatest.com/selenium-playground")
        slider_page_link = page.locator("text=Input Form Submit")
        await slider_page_link.scroll_into_view_if_needed()
        await slider_page_link.click()
        await page.wait_for_timeout(1000)

        # Click the Submit button without filling the form
        await page.click("button:has-text('Submit')")

        # Locate the first required input field (Name field)
        input_field = page.locator("input[name='name']")

        # Trigger validation message (ensures browser generates it)
        await page.evaluate("el => el.reportValidity()", await input_field.element_handle())

        # Get the actual HTML5 validation message
        validation_msg = await page.evaluate("el => el.validationMessage", await input_field.element_handle())

        print("Validation message:", validation_msg)

        # ✅ Assert or log test result
        expected_msg = "Please fill out this field."
        if validation_msg.strip().lower().startswith("please fill"):
            await set_test_status(page, "passed", "Validation message displayed correctly")
            print(f"✅ Validation message verified on {browser_name} {platform}")
        else:
            await set_test_status(page, "failed", f"Unexpected message: {validation_msg}")
            print(f"❌ Unexpected validation message: {validation_msg}")

        await page.wait_for_timeout(5000)

        await page.fill("input[name='name']", "John Doe")
        await page.fill("#inputEmail4", "johndoe@example.com")
        await page.fill("#inputPassword4", "Password123")
        await page.fill("input[name='company']", "LambdaTest")
        await page.fill("input[name='website']", "www.lambdatest.com")
        await page.select_option("select[name='country']", label="United States")
        await page.fill("input[name='city']", "New York")
        await page.fill("#inputAddress1", "123 Test Street")
        await page.fill("#inputAddress2", "Suite 45")
        await page.fill("#inputState", "NY")
        await page.fill("input[name='zip']", "10001")
        await page.click("button:has-text('Submit')")


        await page.wait_for_timeout(5000)

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
