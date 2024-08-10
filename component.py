from gologin import GoLogin
from time import sleep
from playwright.sync_api import sync_playwright
import csv
from tkinter import END

def content_generator_loop(api_key, profile_id, file_path, like, follow, comment_status, log):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        dicts = {}
        i = 0
        for list in csv_reader:
            dicts[i] = {
                'email': list[0].strip(),
                'password': list[1].strip(),
                'post': list[2].strip(),
                'comment': list[3].strip()
            }
            i += 1
    csv_file.close()
    gl = GoLogin(
        {
            "token": api_key,
            "profile_id": profile_id
        }
    )

    post_run = 1
    while post_run < len(dicts):
        email = dicts[post_run]['email']
        password = dicts[post_run]['password']
        post_url = dicts[post_run]['post']
        comment = dicts[post_run]['comment']

        log.insert(END, f'Working Number : {str(post_run)}\n\n')
        log.insert(END, f'Email : {email}\n')
        log.insert(END, f'Password : {password}\n')
        log.insert(END, f'Post_Url : {post_url}\n')
        log.insert(END, f'Comment : {comment}\n')

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
            page.locator("(//input[contains(@placeholder,'Enter your email address...')])[1]").type(email)
            # Insert password
            page.locator("(//input[contains(@placeholder,'Enter your password...')])[1]").type(password)
            # click login button
            page.locator("(//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-md__9TpuT BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt BaseButton_full-width__AlbZn'])[2]").click()
            sleep(2)
            page.wait_for_selector("//div[@class='avatar-img']")

            # Go to target page
            page.goto(post_url, timeout=60000)
            page.wait_for_load_state("load")
            sleep(3)

            # follow
            if follow == "Yes":
                page.locator("//div[@class='sc-65e7f566-0 sc-d8997efc-0 eQBACe nBTGy post-option']//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-sm__oHKNE BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt follow-btn unfollow']").click()
                try:
                    page.locator("//button[normalize-space()='Save']").click()
                except:
                    pass
                sleep(3)

            # like
            if like == "Yes":
                page.locator("//div[@id='EmojiSelectContainer-338594495']//div[contains(@class,'sc-65e7f566-0 sc-b7a6d103-0 eQBACe FMOQp emoji-list-item emoji-list-item-2')]").click()
                sleep(3)

            # comment
            if comment_status == "Yes":
                page.locator("(//div[contains(@role,'textbox')])[1]").type(comment)
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
            sleep(2)
            page.stop()
            gl.stop()
            log.insert(END, f'Number : {str(post_run)} completed...\n\n\n')
        post_run += 1



