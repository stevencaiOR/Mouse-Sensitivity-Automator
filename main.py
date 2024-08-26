from playwright.sync_api import sync_playwright
from time import sleep
import json

def better_click(page, selector):
    locator = page.locator(selector)
    locator.wait_for(state="visible", timeout=2000)
    locator.click()

def better_fill(page, selector, val):
    locator = page.locator(selector)
    locator.wait_for(state="visible", timeout=2000)
    locator.focus()
    for attempt in range(3):
        try:
            locator.fill('')
            locator.fill(val)
            # implement checking to see if val was inputted correctly
            break
        except Exception as e:
            print(f'Attempt {attempt+1} failed: {e}')
            sleep(1)

def main(debug=True):
    url = "https://www.mouse-sensitivity.com/"

    data = {}

    with open("input.json", "r") as file:
        data = json.load(file)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Select mode
        better_click(page, "span[aria-labelledby='select2-mode-container']")
        better_click(page, f"//ul[@id='select2-mode-results']//li[text()='{data['mode']}']")

        # Select units
        better_click(page, "span[aria-labelledby='select2-units-container']")
        better_click(page, f"//ul[@id='select2-units-results']//li[text()='{data['units']}']")

        # Select source game
        better_click(page, "span[aria-labelledby='select2-g0-container']")
        better_click(page, f"//ul[@id='select2-g0-results']//li[text()='{data['source_game']}']")

        # Select target game
        better_click(page, "span[aria-labelledby='select2-g1-container']")
        better_click(page, f"//ul[@id='select2-g1-results']//li[text()='{data['target_game']}']")

        # Set location for target game
        g1_location_text = "In-game"
        better_click(page, "span[aria-labelledby='select2-locationag1-container']")
        better_click(page, f"//ul[@id='select2-locationag1-results']//li[text()='{g1_location_text}']")
        print(f"Location set (target game): {g1_location_text}")

        # Set aim type for target game
        better_click(page, "[aria-labelledby='select2-ag1-container']")
        better_click(page, f"//ul[@id='select2-ag1-results']//li[text()='{data['source_game_aim']}']")

        # Set DPI and sensitivity (for source game)
        better_fill(page, "#dpiag0", data["dpi"])
        print(f"DPI set: {data['dpi']}")
        better_fill(page, "#sens1ag0", data["sensitivity"])
        print(f"Sensitivity set (source game): {data['sensitivity']}")

        # Field of view configuration (both games)
        if data["mode"] == "Advanced" or data["mode"] == "Default":
            better_click(page, "span[aria-labelledby='select2-fovtypeag0-container']")
            better_click(page, f"//ul[@id='select2-fovtypeag0-results']//li[text()='{data['field_of_view_type']}']")
            print(f"Field of view type set (source game): {data['field_of_view_type']}")

            better_click(page, "span[aria-labelledby='select2-fovtypeag1-container']")
            better_click(page, f"//ul[@id='select2-fovtypeag1-results']//li[text()='{data['field_of_view_type']}']")
            print(f"Field of view type set (target game): {data['field_of_view_type']}")

        better_fill(page, "#fovag0", data["field_of_view"])
        better_fill(page, "#fovag1", data["field_of_view"])
        print(f"Field of views set: {data['field_of_view']}")

        # Set resolutions (for both games)
        better_fill(page, "#hresag0", data["resolution_width"])
        better_fill(page, "#vresag0", data["resolution_height"])
        better_fill(page, "#hresag1", data["resolution_width"])
        better_fill(page, "#vresag1", data["resolution_height"])

        if debug:
            mode_confirm = page.locator("#select2-mode-container")
            mode_confirm.wait_for(state="visible")
            print(f"Mode expected: {data['mode']}")
            print(f"Mode actual: {mode_confirm.text_content()}")

            units_confirm = page.locator("#select2-units-container")
            units_confirm.wait_for(state="visible")
            print(f"Units expected: {data['units']}")
            print(f"Units actual: {units_confirm.text_content()}")

            g0_confirm = page.locator("#select2-g0-container")
            g0_confirm.wait_for(state="visible")
            print(f"Source game expected: {data['source_game']}")
            print(f"Source game actual: {g0_confirm.text_content()}")

            g1_confirm = page.locator("#select2-g1-container")
            g1_confirm.wait_for(state="visible")
            print(f"Target game expected: {data['target_game']}")
            print(f"Target game actual: {g1_confirm.text_content()}")

            g0_resolution_width = page.locator("#hresag0")
            g0_resolution_width.wait_for(state="visible")
            g0_resolution_height = page.locator("#vresag0")
            g0_resolution_height.wait_for(state="visible")
            print(f"Resolution expected (source game): {data['resolution_width']} x {data['resolution_height']}")
            print(f"Resolution actual (source game): {g0_resolution_width.input_value()} x {g0_resolution_height.input_value()}")

            g1_resolution_width = page.locator("#hresag1")
            g1_resolution_width.wait_for(state="visible")
            g1_resolution_height = page.locator("#vresag1")
            g1_resolution_height.wait_for(state="visible")
            print(f"Resolution expected (target game): {data['resolution_width']} x {data['resolution_height']}")
            print(f"Resolution actual (target game): {g1_resolution_width.input_value()} x {g1_resolution_height.input_value()}")
        
        sleep(3)

        sens_xpath = "//div[contains(@class,'horizontalbar')]/following-sibling::div[text()='Sensitivity 1: ']/following-sibling::div[contains(@class,'calcright')]/div[contains(@class,'params')]"
        sens = page.locator(sens_xpath)
        sens.wait_for(state="visible", timeout=2000)
        sens_text = sens.text_content()
        print(sens_text)

        fov_xpath = "//div[contains(@class,'horizontalbar')]/following-sibling::div[text()='Config FOV: ']/following-sibling::div"
        fov = page.locator(fov_xpath)
        fov.wait_for(state="visible", timeout=2000)
        fov_text = fov.text_content()
        print(fov_text)

        browser.close()
        
main()