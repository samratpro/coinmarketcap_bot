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
        with sync_playwright() as p:
            debugger_address = gl.start()
            browser = p.chromium.connect_over_cdp("http://" + debugger_address)
            default_context = browser.contexts[0]
            page = default_context.pages[0]

            email = dicts[post_run]['email']
            password = dicts[post_run]['password']
            post_url = dicts[post_run]['post']
            comment = dicts[post_run]['comment']

            log.insert(END, f'Working Number : {str(post_run)}\n\n')
            log.insert(END, f'Email : {email}\n')
            log.insert(END, f'Password : {password}\n')
            log.insert(END, f'Post_Url : {post_url}\n')
            log.insert(END, f'Comment : {comment}\n')

            page.goto(post_url)
            page.wait_for_selector("//button[normalize-space()='Log In']")

            # click login
            try:
                page.locator("//button[normalize-space()='Log In']").click()
            except:
                pass

            # wait for login field

            page.wait_for_selector("(//input[contains(@placeholder,'Enter your email address...')])[1]")
            # insert email
            page.locator("(//input[contains(@placeholder,'Enter your email address...')])[1]").type(email)
            # Insert password
            page.locator("(//input[contains(@placeholder,'Enter your password...')])[1]").type(password)
            # click login button
            page.locator("//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-md__9TpuT BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt BaseButton_full-width__AlbZn']").click()
            login = "Fail"
            try:
                page.wait_for_selector("//div[@class='avatar-img']")
                login = "Success"
                log.insert(END, 'Login Done..\n')
                print("Login Done..")
            except:
                pass

            # Go to target page
            if login == "Success":
                page.goto(post_url, timeout=60000)
                page.wait_for_load_state("load")

                # follow
                if follow == "Yes":
                    try:
                        page.locator(
                            "//div[@class='sc-65e7f566-0 sc-d8997efc-0 eQBACe nBTGy post-option']//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-sm__oHKNE BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt follow-btn unfollow']").click()
                        log.insert(END, 'Follow Done..\n')
                        print("Follow Done..")
                    except:
                        pass
                    # save profile
                    try:
                        page.locator("//button[normalize-space()='Save']").click()
                    except:
                        pass

                # like
                if like == "Yes":
                    try:
                        page.locator("(//div[@class='animation-box LIKE'])[1]").click()
                        print("Done Love Thumbs up..")
                        log.insert(END, 'Done Love Thumbs up..\n')
                    except:
                        log.insert(END, 'Fail to Love Thumbs up..\n')
                        print("Fail to Love Thumbs up..")

                # comment
                if comment_status == "Yes":
                    locator = page.locator("(//div[@role='textbox'])[1]")
                    sleep(0.5)
                    locator.type("  " + comment, delay=100)
                    page.locator("//div[@class='sc-4c05d6ef-0 dlQYLv comment-input-wrapper']//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-md__9TpuT BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt']").click()
                    log.insert(END, 'Comment Done..\n')
                    print("Comment Done..")

                    # save profile
                    try:
                        page.locator("//button[normalize-space()='Save']").click()
                    except:
                        pass

            else:
                print("Login Failed")
                log.insert(END, 'Login Failed\n')

            log.insert(END, f'Number : {str(post_run)} completed...\n\n\n')

            browser.close()
            gl.stop()
        log.insert(END, f'1 second delay to clear profile data..\n\n')
        sleep(1)
        post_run += 1




