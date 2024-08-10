from customtkinter import *
import sqlite3
import base64
import shutil
import os
import threading
import webbrowser
from tkinter import filedialog
from component import *


email = "cauicojyawftpyk@miteon.com"
password = 'POASKPOk3p'
like = 'Yes'
comment_status = 'Yes'
post_url = "https://coinmarketcap.com/community/post/338594496"
follow = "Yes"
comment = "Wow!"




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

    # click and hold profile
    try:
        profile = page.locator("//div[@class='sc-5438cb4a-0 ehFKAE']")
        profile.click()
        sleep(3)
        # singout
        page.locator("(//div[contains(@class,'cmc-profile-popover__option')])[5]").click()
        sleep(2)
    except:
        pass


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
    page.locator(
        "(//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-md__9TpuT BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt BaseButton_full-width__AlbZn'])[2]").click()
    sleep(2)
    page.wait_for_selector("//div[@class='avatar-img']")

    # Go to target page
    page.goto(post_url, timeout=60000)
    page.wait_for_load_state("load")
    sleep(3)

    # follow
    if follow == "Yes":
        page.locator(
            "//div[@class='sc-65e7f566-0 sc-d8997efc-0 eQBACe nBTGy post-option']//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-sm__oHKNE BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt follow-btn unfollow']").click()
        try:
            page.locator("//button[normalize-space()='Save']").click()
        except:
            pass
        sleep(3)

    # like
    if like == "Yes":
        try:
            page.locator("(//div[@class='animation-box LIKE'])[1]").click()
            print("Done Love Thumbs up..")
            # log.insert(END, 'Done Love Thumbs up..\n')
        except:
            # log.insert(END, 'Fail to Love Thumbs up..\n')
            print("Fail to Love Thumbs up..")
        sleep(0.5)
        try:
            page.locator("(//div[@class='animation-box GOOD'])[1]").click()
            print("Done Like Thumbs up..")
            # log.insert(END, 'Done Likee Thumbs up..\n')
        except:
            # log.insert(END, 'Fail to Like Thumbs up..\n')
            print("Fail to Like Thumbs up..")
        sleep(3)

    # comment
    if comment_status == "Yes":
        page.locator("(//div[contains(@role,'textbox')])[1]").fill(comment)
        page.locator("(//button[@class='sc-65e7f566-0 eQBACe BaseButton_base__34gwo bt-base BaseButton_t-default__8BIzz BaseButton_size-md__9TpuT BaseButton_v-primary__gkWpJ BaseButton_vd__gUkWt'])[1]").click()
        sleep(3)

    # click and hold profile
    try:
        profile = page.locator("//div[@class='sc-5438cb4a-0 ehFKAE']")
        profile.click()
        sleep(3)
        # singout
        page.locator("(//div[contains(@class,'cmc-profile-popover__option')])[5]").click()
        sleep(2)
    except:
        pass

    browser.close()
    gl.stop()
    # log.insert(END, f'Number : {str(post_run)} completed...\n\n\n')