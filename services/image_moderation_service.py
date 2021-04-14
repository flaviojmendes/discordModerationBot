import os

from clarifai.rest import ClarifaiApp


async def moderate_image(message):
    url = message.attachments[0].url
    app = ClarifaiApp(api_key=os.environ['CLARIFAI_API_KEY'])
    #General model
    model = app.models.get('d16f390eb32cad478c7ae150069bd2c6')

    response = model.predict_by_url(url=url)
    content_type = response['outputs'][0]['data']['concepts'][0]['name']
    if content_type != 'safe':
        member = await message.author.create_dm()
        await member.send(f'Hey, I have removed your image because it seems to have '
                          f'{content_type} content.')
        await message.delete()
