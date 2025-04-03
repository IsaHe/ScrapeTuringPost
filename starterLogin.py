import nodriver as uc
from time import sleep
from Credentials import EMAIL, PASSWORD

URL = 'https://www.turingpost.com/'

async def main():

    driver = await uc.start(
        user_data_dir="userFolder/"
    )
    tab = await driver.get(URL)
    
    sleep(10)
    
    print('Iniciando sesion...')
    
    login_with_pass = await tab.find('Log in with password', best_match=True)
    await login_with_pass.click()
    
    sleep(7)
    
    email = await tab.select('input[type=text]')
    await email.send_keys(EMAIL)
    
    sleep(8.76)
    
    password = await tab.select('input[type=password]')
    await password.send_keys(PASSWORD)
    
    sleep(2.35)
    
    login_button = await tab.find('Log in', best_match=True)
    await login_button.click()
    
    sleep(10)

if __name__ == '__main__':

    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())