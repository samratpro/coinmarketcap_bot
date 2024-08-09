
from gologin import GoLogin
from time import sleep
from playwright.sync_api import sync_playwright


gl = GoLogin(
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NDMwOTJjNGI3MWE5ODA1NDc3MzBkZGMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NDMwYWEwMmM0NTRiZDE4MTY3YjBkMTQifQ.8Q6PhxlSBksH69FDYs0QmC5UFGGag8AK5tAJjCDkZ4o",
        "profile_id": "66a954cef9f15e35623783b9"
    }
)
with sync_playwright() as p:
    debugger_address = gl.start()
    browser = p.chromium.connect_over_cdp("http://" + debugger_address)
    default_context = browser.contexts[0]
    page = default_context.pages[0]

    page.goto("https://coinmarketcap.com/", timeout=60000)
    page.wait_for_load_state("load")
    # click login
    page.locator("//button[normalize-space()='Log In']").click()
    # wait for login field
    page.wait_for_selector("(//input[contains(@placeholder,'Enter your email address...')])[1]")
    # insert email
    page.locator("(//input[contains(@placeholder,'Enter your email address...')])[1]").type("zoophagouslusa@filmla.org")
    # Insert password
    page.locator("(//input[contains(@placeholder,'Enter your password...')])[1]").type("zoophagouslusa123")
    # click login button
    page.locator("(//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-md__9TpuT BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt BaseButton_full-width__AlbZn'])[2]").click()
    sleep(2)
    page.wait_for_selector("//div[@class='avatar-img']")


    # Go to target page
    page.goto("https://coinmarketcap.com/community/post/338594495", timeout=60000)
    page.wait_for_load_state("load")
    sleep(3)

    # follow
    page.locator("//div[@class='sc-65e7f566-0 sc-d8997efc-0 eQBACe nBTGy post-option']//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-sm__oHKNE BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt follow-btn unfollow']").click()
    try:
        page.locator("//button[normalize-space()='Save']").click()
    except:
        pass

    sleep(3)

    # like
    page.locator("//div[@id='EmojiSelectContainer-338594495']//div[contains(@class,'sc-65e7f566-0 sc-b7a6d103-0 eQBACe FMOQp emoji-list-item emoji-list-item-2')]").click()

    sleep(3)

    # comment
    page.locator("(//div[contains(@role,'textbox')])[1]").type("wow!")
    sleep(3)
    # post comment
    page.locator("(//button[contains(@class,'sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-md__9TpuT BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt')])[1]").click()

    sleep(3)

    # click and hold profile
    profile = page.locator("//div[@class='sc-5438cb4a-0 ehFKAE']")
    profile.click()

    sleep(3)

    # singout
    page.locator("(//div[contains(@class,'cmc-profile-popover__option')])[5]").click()

    sleep(50)

    page.stop()
    gl.stop()

