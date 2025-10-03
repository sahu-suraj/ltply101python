import asyncio
import test_simple_form
import test_slider
import test_input_form

async def main():
    await test_simple_form.test_simple_form()
    await test_slider.test_slider()
    await test_input_form.test_input_form()

if __name__ == "__main__":
    asyncio.run(main())
