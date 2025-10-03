import os
import json
import urllib
import asyncio
import subprocess
from playwright.async_api import async_playwright, Page, Playwright
from helpers import set_test_status, get_lambdatest_browser  # reuse helpers.py

async def test_input_form():
    async with async_playwright() as playwright:
        # Connect to LambdaTest
        browser, page = await get_lambdatest_browser(playwright, "Input Form Submit Test")

        try:
            # 1. Open Selenium Playground
            await page.goto("https://www.lambdatest.com/selenium-playground")

            # 2. Click "Input Form Submit"
            await page.click("text=Input Form Submit")

            # 3. Click "Submit" without filling form
            await page.click("button:has-text('Submit')")

            # 4. Assert error message is displayed
            error_message = page.locator("input[name='name'] + .help-block")
            error_text = await error_message.text_content()
            if error_text.strip() == "Please fill out this field.":
                print("✅ Error message displayed correctly for empty form")
            else:
                print(f"❌ Unexpected error message: {error_text}")
                await set_test_status(page, "failed", f"Unexpected error message: {error_text}")

            # 5. Fill in form fields
            await page.fill("input[name='name']", "John Doe")
            await page.fill("input[name='email']", "johndoe@example.com")
            await page.fill("input[name='password']", "Password123")
            await page.fill("input[name='company']", "LambdaTest")
            await page.fill("input[name='website']", "www.lambdatest.com")

            # 6. Select "United States" from country dropdown
            await page.select_option("select[name='country']", label="United States")

            # 7. Fill address details
            await page.fill("input[name='city']", "New York")
            await page.fill("input[name='address1']", "123 Test Street")
            await page.fill("input[name='address2']", "Suite 45")
            await page.fill("input[name='state']", "NY")
            await page.fill("input[name='zip']", "10001")

            # 8. Submit the form
            await page.click("button:has-text('Submit')")

            # 9. Validate success message
            success_msg = page.locator("p.success-msg")
            msg_text = await success_msg.text_content()
            if msg_text.strip() == "Thanks for contacting us, we will get back to you shortly.":
                await set_test_status(page, "passed", "Form submitted successfully")
                print("✅ Test Passed: Form submitted successfully!")
            else:
                await set_test_status(page, "failed", f"Unexpected success message: {msg_text}")
                print(f"❌ Test Failed: Unexpected success message: {msg_text}")

        except Exception as e:
            print("❌ Error:", e)
            await set_test_status(page, "failed", str(e))
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_input_form())
