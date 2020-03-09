import asyncio
from io import BytesIO
import imagehash
import lxml
import dhash
import json
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from PIL import Image


async def fetch():

    loop = True
    name = 'https://www.pokemon.com/us/pokedex/'
    id = 0
    pklist = {}

    while loop == True:
        id += 1
        url = name + str(id)
        async with ClientSession() as session:
            async with session.get(url, allow_redirects=True) as response:
                if response.status==200:
                    text = await response.read()
                    print('url: ', response.url)
                else:
                    print('No more Pokemon found, stopping.')
                    return
        soup = BeautifulSoup(text, 'html.parser')
        imgb = soup.find("div", {'class':'profile-images'})
        inat = imgb.find_all('img')
        for img in inat:
            pknm = img.get('alt')
            pklink = img.get('src')
            img = BytesIO()
            print(pklink)
            async with ClientSession() as session:
                async with session.get(pklink) as res:
                    if res.status==200:
                        img.write(await res.read())
                    else:
                        raise Exception('Image didn\'t return 200')
            imgh = Image.open(img)
            dhash = imagehash.dhash(imgh)
            hd = str(dhash)
            pklist[pknm] = hd
            print(pklist)

        with open('dhash.json', 'w') as o:
            json.dump(pklist, o)

asyncio.get_event_loop().run_until_complete(fetch())
