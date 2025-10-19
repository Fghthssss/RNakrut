import random
import requests
import subprocess
import time
import threading
from concurrent.futures import ThreadPoolExecutor

with open('cookies.txt', 'w') as f:
    f.write("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhAB.F786A8CCF32B47FBCA0495AAC5AAB434486F4E6F02763A269B6C42912738CD14E6877A725E3ABCDFF8E5590C133F30D7FB7C09D53844600C48A55C3CD29DC4FBC2E97C7CEC176105FDBAB13F45E16F7FCEF24E3EBDDD4C57F4182161A04E481888EEB0C6388EE778B237F193B901CC7595DCF494FCC5521FB7F8492275899AAFF40043F0FCEF1331E7BF0A1792981B169A8A726160BE71FCD0A2D05DEF95E44781D31A9D98A5B29BED0B248CF346445CBDFA83A4EC44E4115815774E2EB5B067F87A5773BA5D4F824E1955732B0CC1DB4875A6B64ABF29BE9312B546ECF55E731F748348478A74BF8E3129085B633AB5C02C808CEF2D46BE7A0639AD52ADB4ABB7D7A4C859404C1CF1A5388A23940CA25D3CF950F7CABE31213B3D518BCC649EE89C337D7B29D75C18C456B503629E6EB2E95DAF4F814991414353C63BFADC7C7CF74BF1B7F98C54E82B85476E971AFE4B0880BA730963FAC0231BA1A7DC93AEFEB339835F27DD304ADB7146C16396812F255D85B10EC6B82DB92C28812EEBA6B6C3BA7548FCD38CF4E0D52BF762D952A5539F2818C46F8AAEA9425BA4A8C6F7562B585BDF3A03ACFB6C987463AE6E252C7923CB9F96B577445AC1913072110FCE5BA58D000D5E225B287784637E46DC14E227DBB22463880E76B401FE8709BC6F7C3BA36578126859B06B260C9F6B5C70D374ABA01FE5014B2420C33A8CD8077388036C4DB5164AE8E3B14A1EBA51152D5875CD306200BDF690CC447AC3D2C311B8914AD7F3CD3DFF5812C085DC95D78C24951F711FCA89EBD52661582BFF612A6AE99FF6DD4EA568326B305448FFCAB46CE8F61CD052873C87F1D1134AD1F09F0AEEE16A84C9061602FA5FDC3687081130CB01140B271AC5B9F5C92937D9075E5128D9400C4D634C30872A95DD8A5E095C2911EB82442AEB00514CF158BEC1336EB3E3A809E58FBDB5EAE7ED1343AB8C8758D86C5E379E9EEE68DDC1A49CDBC9E78C482FDB46D10951E3AD84F5DB0BBC67D15C21EF62EA1EE9E2C6C51C42542FDE407B25498B2AE51A1DE7B700B1957CF0E28C09EADC67041921DFD64A8A9657C83A077FEC64C4C689F3E2D005C21B29610709F530F6AB1E4F1BE4818BAD7A51A1410A90C26D56300726AA6F0E144FA77CDA39DAFBF2E711FD8DA75BF0752018AEE5860AC5AE4BC85DD2848892A2A6BCA5E5E7A323445CCA3EBDCC8CAE4EEB65018491\n")

class RobloxVisitBot:
    def __init__(self, game_id, max_workers=5):
        self.game_id = game_id
        self.cookies = self.load_cookies()
        self.max_workers = max_workers
        self.session = requests.Session()
        
    def load_cookies(self):
        try:
            with open("cookies.txt", "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("Файл cookies.txt не найден")
            return []
    
    def get_user_info(self, cookie):
        session = requests.Session()
        session.cookies['.ROBLOSECURITY'] = cookie
        
        try:
            response = session.get('https://users.roblox.com/v1/users/authenticated')
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def get_auth_ticket(self, cookie):
        session = requests.Session()
        session.cookies['.ROBLOSECURITY'] = cookie
        
        try:
            # Получаем CSRF токен
            csrf_response = session.post('https://auth.roblox.com/v1/authentication-ticket')
            csrf_token = csrf_response.headers.get('x-csrf-token', '')
            
            if csrf_token:
                session.headers['x-csrf-token'] = csrf_token
                auth_response = session.post(
                    'https://auth.roblox.com/v1/authentication-ticket',
                    headers={'referer': f'https://www.roblox.com/games/{self.game_id}'}
                )
                return auth_response.headers.get('rbx-authentication-ticket', '')
        except:
            pass
        return None
    
    def launch_roblox(self, auth_ticket, browser_id):
        try:
            launch_url = (
                f"roblox-player:1+launchmode:play+gameinfo:{auth_ticket}+"
                f"launchtime:{browser_id}+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2F"
                f"game%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D{browser_id}%26"
                f"placeId%3D{self.game_id}%26isPlayTogetherGame%3Dfalse+"
                f"browsertrackerid:{browser_id}+robloxLocale:en_us+gameLocale:en_us+channel:"
            )
            
            subprocess.Popen(
                f'start "" "{launch_url}"',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except:
            return False
    
    def cleanup_processes(self):
        processes = [
            "RobloxPlayerBeta.exe",
            "RobloxPlayerLauncher.exe"
        ]
        
        for process in processes:
            try:
                subprocess.run(f"taskkill /IM {process} /F", 
                             shell=True, 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
            except:
                pass
    
    def single_visit(self, cookie, visit_duration=30):
        user_info = self.get_user_info(cookie)
        if not user_info:
            return False
        
        username = user_info.get('name', 'Unknown')
        print(f"Запуск от имени: {username}")
        
        auth_ticket = self.get_auth_ticket(cookie)
        if not auth_ticket:
            return False
        
        browser_id = random.randint(1000000, 9999999)
        
        if self.launch_roblox(auth_ticket, browser_id):
            print(f"Успешный запуск для {username}")
            time.sleep(visit_duration)
            self.cleanup_processes()
            return True
        
        return False
    
    def start_visits(self, total_visits=10, delay_range=(5, 15)):
        if not self.cookies:
            print("Нет доступных cookies")
            return
        
        successful_visits = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            for i in range(total_visits):
                if not self.cookies:
                    break
                    
                cookie = random.choice(self.cookies)
                future = executor.submit(self.single_visit, cookie)
                futures.append(future)
                
                # Случайная задержка между запусками
                delay = random.randint(delay_range[0], delay_range[1])
                time.sleep(delay)
            
            # Сбор результатов
            for future in futures:
                if future.result():
                    successful_visits += 1
        
        print(f"Завершено успешных посещений: {successful_visits}/{total_visits}")

# Использование
if __name__ == "__main__":
    GAME_ID = "123456789"  # Заменить на нужный ID игры
    
    bot = RobloxVisitBot(GAME_ID, max_workers=3)
    bot.start_visits(total_visits=20, delay_range=(10, 30))