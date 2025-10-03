from helpers import get_lambdatest_browser, set_test_status
import asyncio

async def test_slider(playwright, browser_name, version, platform):
    browser, page = await get_lambdatest_browser(
        playwright, "Slider Test", browser_name, version, platform
    )
    try:
        await page.goto("https://www.lambdatest.com/selenium-playground")
        await page.set_viewport_size({"width": 1920, "height": 1080})  # maximize window
        slider_page_link = page.locator("text=Drag & Drop Sliders")
        await slider_page_link.scroll_into_view_if_needed()
        await slider_page_link.click()
        await page.wait_for_timeout(1000)

        slider = await page.wait_for_selector("//input[@type='range' and @value='15']")

        # Get slider position and size
        slider_box = await slider.bounding_box()
        if not slider_box:
            raise Exception("Unable to get slider position")

        start_x = slider_box["x"]
        start_y = slider_box["y"] + slider_box["height"]/2
        width = slider_box["width"]

        # Move slider close to target value (e.g., 95)
        target_value = 95
        max_value = 100
        x_offset = width * target_value / max_value

        await page.mouse.move(start_x, start_y)
        await page.mouse.down()
        await page.mouse.move(start_x + x_offset, start_y, steps=5)
        await page.mouse.up()

        # Fine-tune using keyboard arrow keys
        current_value = await slider.evaluate("s => Number(s.value)")
        while current_value > target_value:
            await slider.press("ArrowLeft")
            current_value -= 1
        while current_value < target_value:
            await slider.press("ArrowRight")
            current_value += 1

        # Trigger input event for JS listeners
        await slider.evaluate("(s) => s.dispatchEvent(new Event('input', { bubbles: true }))")

        # Validate slider value
        value_text = await page.text_content("//output[@id='rangeSuccess']")
        if value_text.strip() == str(target_value):
            await set_test_status(page, "passed", "Slider Test Passed")
            print(f"✅ Slider Test Passed on {browser_name} {platform}")
        else:
            await set_test_status(page, "failed", f"Expected slider 95 but got {value_text}")
            print(f"❌ Slider Test Failed on {browser_name} {platform}")

    except Exception as e:
        await set_test_status(page, "failed", str(e))
        print(f"❌ Slider Test Error on {browser_name} {platform}: {e}")
    finally:
        await browser.close()
