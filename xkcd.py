import logging
import re
import requests
from errbot import BotPlugin, botcmd
from BeautifulSoup import BeautifulSoup


class ShowXkcd(BotPlugin):
    def get_image_and_wisdom(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        img = soup.first('div', {'id': 'comic'}).first('img')
        return img['src'], img['title']

    def callback_message(self, conn, mess):
        body = mess.getBody().lower()
        if body.find('http://xkcd.com') or body.find('http://www.xkcd.com'):
            logging.info('found xkcd link')
            url = re.search("(?P<url>https?://[^\s]+)", body).group("url")
            logging.info('xkcd url: %s' % url)
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

    @botcmd
    def xkcd(self, mess, args):
        random_url = 'http://dynamic.xkcd.com/random/comic/'
        image, wisdom = self.get_image_and_wisdom(random_url)
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
