
try:
    import requests
    import json
    from bs4 import BeautifulSoup
    from python3_anticaptcha import NoCaptchaTaskProxyless
except ImportError as e:
    print(e, 'you should install this modules: \
requests, json, beautifulsoup4, python3_anticaptcha', sep="\n")


ANTICAPTCHA_KEY = input("Please enter anticaptcha API key:\n").strip()
login = 'vabavo'
passwd = input("Please enter password for user 'vabavo':\n").strip()
website_url = 'https://pikabu.ru'
website_captcha_key = '6Lf5DUsUAAAAAGeOi2l8EpSqiAteDx5PGFMYPkQW'
auth_url = 'https://pikabu.ru/ajax/auth.php'
useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
filename = 'pikabu_top10_tags.txt'
articles_to_parse = 100
articles_parsed = 0
tags = []
tags_counted = {}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;\
q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://pikabu.ru/',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': useragent
}

session = requests.Session()
res = session.get('https://pikabu.ru', headers=headers)
if res.status_code == 200:
    print('Successfully connected to ' + website_url)

with NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(
        anticaptcha_key=ANTICAPTCHA_KEY) as nocaptcha:
    print('Connected to anti-captcha.com to get google captcha response key.\
 It takes 40-60 seconds. Please, be patient.')
    recaptcha_result = nocaptcha.captcha_handler(
        websiteURL=website_url,
        websiteKey=website_captcha_key,
    )

if recaptcha_result['status'] == 'ready':
    gRecaptchaResponse = recaptcha_result['solution']['gRecaptchaResponse']
    print('Received google captcha response key from anti-captcha.com')
else:
    raise Exception('There was an error while getting captcha response key from anti-captcha. \
Please, try run script again')

post_data = {
    'mode': 'login',
    'username': login,
    'password': passwd,
    'g-recaptcha-response': gRecaptchaResponse
}

ajax_headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-length': '604',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'dnt': '1',
    'origin': 'https://pikabu.ru',
    'pragma': 'no-cache',
    'referer': 'https://pikabu.ru/',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': useragent,
    'x-requested-with': 'XMLHttpRequest'
}

r = session.post(auth_url, data=post_data, headers=ajax_headers)
try:
    auth_response = json.loads(r.text)
    if auth_response['result']:
        print('Auth was successful')
    else:
        print(auth_response['message'], 'there is an error while logging in')
except Exception as err:
    print(err, "can't authorise at site " + website_url)

res = session.get('https://pikabu.ru', headers=headers)

if 'Ошибка. Пожалуйста, попробуйте авторизоваться позже' in res.text:
    print('Ошибка. Пожалуйста, попробуйте авторизоваться позже')
elif login in res.text:
    print('You are logged in as ' + login)

page = 1
while articles_parsed < articles_to_parse:
    url = 'https://pikabu.ru/?page=' + str(page)
    html_source = session.get(url, headers=headers)
    soup = BeautifulSoup(html_source.text, 'html.parser')
    tags_on_page = soup.select('a[data-tag]')
    tags += [tag.getText() for tag in tags_on_page]
    articles_parsed += len(soup.find_all('article'))
    print("Parsed", str(page), "page, total found",
          articles_parsed, "articles")
    page += 1

for tag in tags:
    tags_counted[tag] = tags_counted.get(tag, 0) + 1

sort_tags_counted = sorted(tags_counted.items(),
                           key=lambda x: x[1], reverse=True)

with open(filename, 'w') as file:
    list_tags = [tag[0] + ' ' + str(tag[1]) for tag in sort_tags_counted]
    file.write('\n'.join(list_tags[:10]))
    print("TOP 10 tags of user", login, "was wrote at file", filename)
