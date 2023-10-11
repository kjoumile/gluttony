import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import random
import time
import json
import generate_reply
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import base64

account_data_file = "database/black_account_data.txt"      #файл с логином и паролем в формате logg:pass в первой строчке
json_filename = "database/titles_group.json"               #Названия групп из которых берем подписки
post_text = "#casino #free #help\ntake free spins from my referral please https://betworld.cc/go/2a5f10f7bd15426b268ae4242aaa9b3e365b64d1eb0a0b0b/"
s = Service(executable_path="webdriver/chromedriver.exe")  # расположение драйвера хрома

def main():
    while True:
        json_file_data = open_file_json(json_filename)
        #create_post(post_text)
        group_followers(json_file_data[0]['User']['Group'])
        movie_by_following()
        time.sleep(60*60*3)

def open_twitter(account_data):
    time.sleep(5)
    loggin, password, cookie, ip = account_data.split(',')
    options = webdriver.ChromeOptions()
    options.add_argument(f'--proxy-server={ip}')
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    global driver
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()
    driver.get(f"https://twitter.com")
    time.sleep(10)

    coded_string = f"{cookie}"
    bytes_data = base64.b64decode(coded_string)
    decoded_string = bytes_data.decode()
    json_data = json.loads(decoded_string)
    for cookie in json_data:
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, "//article[@data-testid='tweet']")
        main(loggin, password, ip)
    except:
        file = open('database/break_bot.txt', 'a')
        file.write(loggin + ',' + password + ',' + ip)
        file.close()
        driver.quit()

def create_image_post(window_post):
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(1)
    image_list = os.listdir(path='image/')
    file_path = 'E:/program/py/twitter_bot/image/'
    file_path += image_list[random.randint(0, len(image_list))]
    time.sleep(1)
    file_img = window_post.find_element(By.XPATH, "//input[@data-testid='fileInput']")
    time.sleep(1)
    ActionChains(driver).move_to_element(file_img).click().perform()
    time.sleep(5)
    file_img.send_keys(file_path)

def create_post(text):
    button_post = driver.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']")
    button_post.click()
    time.sleep(5)
    window_post = driver.find_element(By.XPATH, "//div[@role='dialog']")
    time.sleep(1)
    create_image_post(window_post)
    time.sleep(5)
    try:
        text_label = window_post.find_element(By.XPATH, "//div[@data-testid='tweetTextarea_0']")
        text_label.send_keys(text)
    except:
        button_follow = driver.find_element(By.XPATH, ".//div[@role='button']")
        time.sleep(1)
        driver.execute_script("arguments[0].click();", button_follow)
        time.sleep(2)
        text_label = window_post.find_element(By.XPATH, "//div[@data-testid='tweetTextarea_0']")
        text_label.send_keys(text)
    time.sleep(5)
    window_post.find_element(By.XPATH, "//div[@data-testid='tweetButton']").click()
    time.sleep(5)

def delete_bot_link(link):
    with open('database/subscription_list.txt', 'r') as file:
        data = file.read().replace(link, '')
    with open('database/subscription_list.txt', 'w') as file:
        file.write(data)

def save_human_link(link):
    link_file = open('database/human_list.txt', 'a')
    link_file.write(link)
    link_file.close()

def check_on_bot(post, user_link):
    popa = post.find_element(By.XPATH, "//div[contains(@class, 'css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj')]").text

    following_number = popa.split("\n")[0].split(" ")[0]
    followers_number = popa.split("\n")[1].split(" ")[0]

    if following_number.find(",") > 0: following_number = float(following_number.split(",")[0] + following_number.split(",")[1])
    elif following_number.find("K") > 0: following_number = float(following_number.split("K")[0]) * 1000
    elif following_number.find("M") > 0: following_number = float(following_number.split("M")[0]) * 1000000
    else: following_number = float(following_number)

    if followers_number.find(",") > 0: followers_number = float(followers_number.split(",")[0] + followers_number.split(",")[1])
    elif followers_number.find("K") > 0: followers_number = float(followers_number.split("K")[0]) * 1000
    elif followers_number.find("M") > 0: followers_number = float(followers_number.split("M")[0]) * 1000000
    else: followers_number = float(followers_number)

    if following_number / followers_number >= 2:
        delete_bot_link(user_link)
        return True    #аккаунт бот
    else:
        if following_number / followers_number <= 4: save_human_link(user_link)
        return False  #аккаунт не бот

def open_file_json(fileName):
    file = fileName
    with open(file, 'r', encoding="UTF-8") as f:
        data = json.loads(f.read())
    return data

def random_wait(min, max):
    random_time = random.randint(min, max)
    time.sleep(random_time)

def create_like(post):
    likes = post.find_element(By.XPATH, "//div[@data-testid='like']")
    driver.execute_script("arguments[0].click();", likes)
    time.sleep(2)


def create_retweet(post):
    random_wait(14, 31)
    retweets = post.find_element(By.XPATH, "//div[@data-testid='retweet']")
    driver.execute_script("arguments[0].click();", retweets)
    time.sleep(2)
    retweet = driver.find_elements(By.XPATH, "//div[@role='menuitem']")
    retweet[-1].click()


def create_retweet_quot(post):
    random_wait(14, 31)
    retweets = post.find_element(By.XPATH, "//div[@data-testid='retweet']")
    driver.execute_script("arguments[0].click();", retweets)
    time.sleep(2)
    retweet = driver.find_elements(By.XPATH, "//a[@role='menuitem']")
    time.sleep(2)
    retweet[0].click()
    time.sleep(2)
    textfield = driver.find_element(By.XPATH,"//div[contains(@class, 'public-DraftStyleDefault-block')]")
    prompt_text = take_text_from_post(post)
    reply_text = generate_reply.generate_text_gamling(prompt_text)
    textfield.send_keys(reply_text)
    random_wait(2,5)
    all_buttons = driver.find_elements(By.XPATH, "//div[@data-testid='tweetButton']")
    all_buttons[-1].click()
    random_wait(2,5)


def find_posts_by_hashtag(hashtag):
    key_word = hashtag
    driver.get(f"https://twitter.com/search?q=%23{key_word}&src=typed_query")
    random_wait(14, 31)
    posts = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    return posts

def take_text_from_post(post):
    text_label = post.find_element(By.XPATH, "//div[@data-testid='tweetText']")
    list_text_tweet = []
    list_text = text_label.find_elements(By.TAG_NAME, "span")
    for i in range(len(list_text)):
        list_text_tweet.append(list_text[i].text)
    textTweet = ' '.join(list_text_tweet)
    return textTweet

def check_generation_available():
    file = open("database/generation_busy.txt", 'r')
    string_list = file.readlines()
    if len(string_list) >= 2:
        file.close()
        return False
    else:
        file.close()
        return True

def take_generation_place():
    file = open("database/generation_busy.txt", 'a')
    file.write("took\n")
    file.close()

def get_out_of_queue_generation():
    file = open("database/generation_busy.txt", 'r')
    string_list = file.readlines()
    file.close()

    file = open("database/generation_busy.txt", 'w')
    for i in range(len(string_list)):
        if i < len(string_list) - 1: file.write(string_list[i])
    file.close()

def create_reply(post):
    random_wait(4, 7)
    comment_button = post.find_element(By.XPATH, "//div[@data-testid='reply']")
    driver.execute_script("arguments[0].click();", comment_button)
    random_wait(4, 7)

    label_comment = driver.find_element(By.XPATH, "//div[contains(@class, 'public-DraftStyleDefault-block')]")
    prompt_text = take_text_from_post(post)
    while not check_generation_available(): time.sleep(5)
    take_generation_place()
    reply_text = generate_reply.generate_text_gamling(prompt_text)
    get_out_of_queue_generation()
    label_comment.send_keys(reply_text)
    random_wait(2, 4)

    button_reply = driver.find_element(By.XPATH, "//div[@data-testid='tweetButton']")
    driver.execute_script("arguments[0].click();", button_reply)
    random_wait(4, 7)

def movie_by_following():
    movie_counter = random.randint(70,120)
    while movie_counter > 0:
        movie_counter -= 1
        user_link = take_user_link()
        driver.get(user_link)
        time.sleep(5)
        try:
            post_without_like = driver.find_element(By.XPATH, "//article[@data-testid='tweet']")
            if check_on_bot(post_without_like, user_link): continue
            try:
                post_without_like.find_element(By.XPATH, ".//div[contains(@aria-label,'Liked')]")
            except:
                create_reply(post_without_like)
                create_like(post_without_like)
                movie_counter -= 1
                random_wait(24, 46)
        except:
            delete_bot_link(user_link)
            continue

def take_user_link():
    with open('database/subscription_list.txt', 'r') as f:
        link_file = f.readlines()
    random_user = random.randint(0, len(link_file)-1)
    return link_file[random_user]

def group_followers(group_name):
    following_count = random.randint(150, 250)
    while following_count > 0:
        for i in range(len(group_name)):
            if following_count <= 0: break
            driver.get(f'https://twitter.com/{group_name[i]}/followers')
            random_wait(4,7)
            following_count -= follow_user()

def save_user_link(user):
    link_file = open('database/subscription_list.txt', 'a')
    nickname = user.find_element(By.XPATH, ".//a[@role='link']")
    link_file.write(nickname.get_attribute('href') + '\n')
    link_file.close()

def follow_user():
    try:
        follows = driver.find_elements(By.XPATH, "//div[@data-testid='UserCell']")
        following_count, temp = random.randint(1, 5)
        if len(follows) < following_count: following_count = len(follows)
        for i in range(following_count):
            check_press = follows[i].find_element(By.XPATH,
                                                  "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[2]/div/div/span/span")
            if check_press.text == 'Following':
                temp -= 1
                continue
            time.sleep(2)
            button_follow = follows[i].find_element(By.XPATH, ".//div[@role='button']")
            time.sleep(2)
            driver.execute_script("arguments[0].click();", button_follow)

            save_user_link(follows[i])
            random_wait(24, 46)
        return temp
    except:
        return 0

def take_account_data(data_file):
    file = open(data_file, 'r')
    arr = []
    for i in file:
        arr.append(i)
    return arr


if __name__ == "__main__":
    datas = take_account_data(account_data_file)
    for account_data in datas:
        time.sleep(15)
        process = multiprocessing.Process(target=open_twitter, args=(account_data,))
        process.start()