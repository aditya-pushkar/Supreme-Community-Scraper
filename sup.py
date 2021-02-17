import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import random
import time

hook = ''

droplist_link = 'https://www.supremecommunity.com/season/spring-summer2021/droplist/2021-02-18/'

def main():
    r = requests.get(droplist_link)
    soup = BeautifulSoup(r.text,"html.parser")
    cards = soup.find('div',{'id':'catalog-list'}).findAll('div')
    for card in cards:
        try:
            item = card['data-name']
            img = card.find("img")["data-src"]
            image = f'https://supremecommunity.com{img}'
            price_usd = card['data-usdprice']
            price_gbp = card['data-gbpprice']
            upvotes = card['data-upvotes']
            downvotes = card['data-downvotes']
            sender.webhook(item,price_usd,price_gbp,upvotes,downvotes,image)
            print("| WEBHOOK SENT |")
            time.sleep(1.5) #If droplist is shorter you can lower the delay
        except Exception as e:
            # print(e)
            pass


class sender:
    @staticmethod
    def webhook(item,price_usd,price_gbp,upvotes,downvotes,image):
        try:
            webhook = DiscordWebhook(hook)
            embed = DiscordEmbed(title='', description='', color=0x2feb61) #2feb61
            embed.set_title(title='Supreme Droplist')
            embed.set_image(url=image)
            embed.add_embed_field(name='Item',value=f'**{item}**',inline=False)
            embed.add_embed_field(name='Price',value=f'**${price_usd}** / **£{price_gbp}**',inline=False)
            embed.add_embed_field(name='Upvotes',value=f'**{upvotes}**',inline=True)
            embed.add_embed_field(name='Downvotes',value=f'**{downvotes}**',inline=True)
            embed.set_footer(text='CharlieAIO | Supreme Droplist')
            webhook.add_embed(embed)
            webhook.execute()
        except:
            time.sleep(3)
            webhook(item,price_usd,price_gbp,upvotes,downvotes,image)


main()