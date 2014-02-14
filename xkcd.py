import re
import requests
from errbot import BotPlugin
from BeautifulSoup import BeautifulSoup


class ShowXkcd(BotPlugin):
    def get_image_and_wisdom(self, url):
        response = requests.get(url).text
        soup = BeautifulSoup(response.text)
        img = soup.first('div', {'id': 'comic'}).first('img')
        return img['src'], img['title']

    def callback_message(self, conn, mess):
        body = mess.getBody().lower()
        if body.find('http://kxcd.com'):
            url = re.search("(?P<url>https?://[^\s]+)", body).group("url")
            image, wisdom = self.get_image_and_wisdom(url)
            self.send(
                mess.getFrom(),
                image,
                message_type='groupchat'
            )
            self.send(
                mess.getFrom(),
                '"%s"' % wisdom,
                message_type='groupchat'
            )
