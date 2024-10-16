import os
import time
import requests
from colorama import init, Fore, Style

# Inicializa o Colorama
init(autoreset=True)

def clear_terminal():
    """Limpa o terminal com um comando apropriado para o sistema operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')

def blinking_art(interval=0.5, duration=2):
    """Faz a arte piscar por um determinado tempo."""
    end_time = time.time() + duration
    full_art = Fore.RED + r"""
 ##   ##  #######  ##  ##    ####      ####     ##     ##   ##  ######   ######
 ### ###   ##   #  ##  ##     ##      ##  ##   ####    ###  ##   ##  ##   ##  ##
 #######   ## #     ####      ##     ##       ##  ##   #### ##   ##  ##   ##  ##
 #######   ####      ##       ##     ##       ##  ##   ## ####   #####    #####
 ## # ##   ## #     ####      ##     ##       ######   ##  ###   ##  ##   ## ##
 ##   ##   ##   #  ##  ##     ##      ##  ##  ##  ##   ##   ##   ##  ##   ##  ##
 ##   ##  #######  ##  ##    ####      ####   ##  ##   ##   ##  ######   #### ##
""" + Fore.RESET

    while time.time() < end_time:
        clear_terminal()
        print(full_art)
        time.sleep(interval)
        clear_terminal()
        time.sleep(interval)
    clear_terminal()
    print(full_art)

def login(token):
    """Realiza o login e exibe informações do usuário."""
    url = "https://api.thevertus.app/users/get-data"
    headers = get_headers(token)
    
    try:
        response = requests.post(url, headers=headers, json={}, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        balance = int(data.get("user").get("balance")) / 10**18
        farm_b = data.get("user").get("vertStorage") / 10**18
        pph = data.get("user").get("valuePerHour") / 10**18
        eo = data.get("user").get("earnedOffline") / 10**18
        print(Fore.GREEN + Style.BRIGHT + f"Saldo Vert: {balance:.3f} | Ganhos Offline: {eo:.4f}")
        print(Fore.GREEN + Style.BRIGHT + f"Saldo da Fazenda: {farm_b:.5f} | PPH: {pph:.4f}")

        # Exibe a arte final e créditos após o login
        display_final_art_and_credits()

    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f"Falha na requisição: {e}")

def display_final_art_and_credits():
    """Exibe a arte final e os créditos."""
    clear_terminal()
    print(Fore.GREEN + r"""     
 ##   ##  #######  ##  ##    ####      ####     ##     ##   ##  ######   ######
 ### ###   ##   #  ##  ##     ##      ##  ##   ####    ###  ##   ##  ##   ##  ##
 #######   ## #     ####      ##     ##       ##  ##   #### ##   ##  ##   ##  ##
 #######   ####      ##       ##     ##       ##  ##   ## ####   #####    #####
 ## # ##   ## #     ####      ##     ##       ######   ##  ###   ##  ##   ## ##
 ##   ##   ##   #  ##  ##     ##      ##  ##  ##  ##   ##   ##   ##  ##   ##  ##
 ##   ##  #######  ##  ##    ####      ####   ##  ##   ##   ##  ######   #### ##
""" + Fore.RESET + "\033[0m" + "\033[1;96m---------------------------------------\033[0m\n" + \
    "\033[1;93mScript criado por: Mexican BR\033[0m\n" + \
    "\033[1;92mJunte-se ao Telegram: \nhttps://t.me/MexicanbrScripts\033[0m\n" + \
    "\033[1;91mVisite meu GitHub: \nhttps://github.com/mexicanbr\033[0m\n" + \
    "\033[1;96m---------------------------------------\033[0m")

def daily_bonus(token):
    """Reivindica o bônus diário."""
    url = "https://api.thevertus.app/users/claim-daily"
    headers = get_headers(token)
    
    try:
        response = requests.post(url, headers=headers, json={}, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        
        success = data.get("success")
        n_balance = data.get("balance") / 10**18 if data.get("balance") is not None else 0
        massage = data.get("msg", "")
        reward = data.get("claimed") / 10**18 if data.get("claimed") is not None else 0
        day = data.get("consecutiveDays", 0)
        
        if success:
            print(Fore.GREEN + Style.BRIGHT + f"Dia {day} Bônus Diário {reward} Reivindicado com Sucesso")
            print(Fore.GREEN + Style.BRIGHT + f"Novo Saldo: {n_balance}")
        else:
            print(Fore.YELLOW + Style.BRIGHT + f"{massage}")
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f"Falha na requisição: {e}")

def ads(token):
    """Reivindica recompensas de anúncios."""
    url_1 = "https://api.thevertus.app/missions/check-adsgram"
    headers = get_headers(token)

    try:
        response = requests.post(url_1, headers=headers, json={}, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        isSuccess = data.get("isSuccess")
        massage = data.get("msg")

        if isSuccess:
            print(Fore.CYAN + Style.BRIGHT + "Reivindicando Recompensa de Anúncios.....")
            time.sleep(30)
            url_2 = "https://api.thevertus.app/missions/complete-adsgram"
            response_2 = requests.post(url_2, headers=headers, json={}, allow_redirects=True)
            response_2.raise_for_status()
            data_2 = response_2.json()
            
            isSuccess = data_2.get("isSuccess")
            new_balance = data_2.get("newBalance") / 10**18 if data_2.get("newBalance") is not None else 0
            total_claim = data_2.get("completion")
            
            if isSuccess:
                new_balance = f"{new_balance:.3f}"
                print(Fore.GREEN + Style.BRIGHT + "Recompensa de Anúncios Reivindicada com Sucesso")
                print(Fore.GREEN + Style.BRIGHT + f"Novo Saldo: {new_balance} | Reivindicação Total: {total_claim} vezes")
            else:
                print(Fore.YELLOW + Style.BRIGHT + f"{data_2}")
                      
        else:
            print(Fore.YELLOW + Style.BRIGHT + f"{massage}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f"Falha na requisição: {e}")        

def upgrade_farm(token):
    """Atualiza a fazenda."""
    url = "https://api.thevertus.app/users/upgrade"
    headers = get_headers(token)
    body = {"upgrade": "farm"}

    try:
        response = requests.post(url, headers=headers, json=body, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        
        success = data.get("success")
        message = data.get("msg")
        
        abilities = data.get("abilities", {})
        farm = abilities.get("farm", {})
        farm_lvl = farm.get("level", "Desconhecido")
        farm_des = farm.get("description", "Nenhuma descrição disponível")
        new_balance = data.get("newBalance")
        
        a_b = new_balance / 10**18 if new_balance is not None else 0
        
        if success:
            print(Fore.GREEN + Style.BRIGHT + "Atualização da Fazenda Bem-Sucedida")
            print(Fore.GREEN + Style.BRIGHT + f"Novo Nível da Fazenda: {farm_lvl} | Habilidade da Fazenda: {farm_des}")
            print(Fore.GREEN + Style.BRIGHT + f"Saldo Disponível: {a_b:.3f}")
        else:
            print(Fore.RED + Style.BRIGHT + f"Atualização Falhou: {message}")
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f"Falha na requisição: {e}")

def upgrade_storage(token):
    """Atualiza o armazém."""
    url = "https://api.thevertus.app/users/upgrade"
    headers = get_headers(token)
    body = {"upgrade": "storage"}

    try:
        response = requests.post(url, headers=headers, json=body, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        
        success = data.get("success")
        message = data.get("msg")
        
        abilities = data.get("abilities", {})
        storage = abilities.get("storage", {})
        storage_lvl = storage.get("level", "Desconhecido")
        storage_des = storage.get("description", "Nenhuma descrição disponível")
        new_balance = data.get("newBalance")
        
        a_b = new_balance / 10**18 if new_balance is not None else 0
        
        if success:
            print(Fore.GREEN + Style.BRIGHT + "Atualização do Armazém Bem-Sucedida")
            print(Fore.GREEN + Style.BRIGHT + f"Novo Nível do Armazém: {storage_lvl} | Habilidade do Armazém: {storage_des}")
            print(Fore.GREEN + Style.BRIGHT + f"Saldo Disponível: {a_b:.3f}")
        else:
            print(Fore.RED + Style.BRIGHT + f"Atualização Falhou: {message}")
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f"Falha na requisição: {e}")

def upgrade_population(token):
    """Atualiza a população."""
    url = "https://api.thevertus.app/users/upgrade"
    headers = get_headers(token)
    body = {"upgrade": "population"}

    try:
        response = requests.post(url, headers=headers, json=body, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        
        success = data.get("success")
        message = data.get("msg")
        
        abilities = data.get("abilities", {})
        population = abilities.get("population", {})
        population_lvl = population.get("level", "Desconhecido")
        population_des = population.get("description", "Nenhuma descrição disponível")
        new_balance = data.get("newBalance")
        
        a_b = new_balance / 10**18 if new_balance is not None else 0
        
        if success:
            print(Fore.GREEN + Style.BRIGHT + "Atualização da População Bem-Sucedida")
            print(Fore.GREEN + Style.BRIGHT + f"Novo Nível da População: {population_lvl} | Habilidade da População: {population_des}")
            print(Fore.GREEN + Style.BRIGHT + f"Saldo Disponível: {a_b:.3f}")
        else:
            print(Fore.RED + Style.BRIGHT + f"Atualização Falhou: {message}")
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f"Falha na requisição: {e}")

def get_cards(token):
    """Obtém os cartões de atualização."""
    url = "https://api.thevertus.app/upgrade-cards"
    headers = get_headers(token)
    card_details = []

    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        
        for category in ['economyCards', 'militaryCards', 'scienceCards']:
            for card in data.get(category, []):
                card_id = card['_id']
                card_name = card.get('cardName', 'Nome Desconhecido')
                card_details.append((card_id, card_name))
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f"Falha na requisição: {e}")

    return card_details

def post_card_upgrade(card_id, card_name, token):
    """Atualiza um cartão específico."""
    url = "https://api.thevertus.app/upgrade-cards/upgrade"
    headers = {'Authorization': f'Bearer {token}'}
    body = {"cardId": card_id}
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        
        success = data.get("isSuccess")
        message = data.get("msg")
        
        balance_str = data.get("balance")
        new_pph_str = data.get("newValuePerHour")
        
        if balance_str is not None:
            try:
                a_balance = int(balance_str) / 10**18
            except (ValueError, TypeError):
                a_balance = "Valor de saldo inválido"
        else:
            a_balance = "Saldo não fornecido"
        
        if new_pph_str is not None:
            try:
                new_pph = int(new_pph_str) / 10**18
            except (ValueError, TypeError):
                new_pph = "Novo PPH inválido"
        else:
            new_pph = "Novo PPH não fornecido"
        
        if success:
            print(Fore.GREEN + Style.BRIGHT + f"A atualização do Cartão {card_name} foi Bem-Sucedida")
            print(Fore.GREEN + Style.BRIGHT + f"Saldo Disponível: {a_balance}")
            print(Fore.GREEN + Style.BRIGHT + f"Novo PPH: {new_pph}")
        else:
            print(Fore.RED + Style.BRIGHT + f"{message}")
            print(Fore.RED + Style.BRIGHT + f"A atualização do Cartão {card_name} Falhou")
        
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f"Falha na requisição para o ID do cartão {card_id}, Nome do Cartão: {card_name}: {e}")

def get_headers(token):
    """Gera os cabeçalhos para as requisições."""
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }

def countdown_timer(seconds):
    """Função de contagem regressiva."""
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print(f"{Fore.CYAN + Style.BRIGHT}Aguarde {hours:02}:{mins:02}:{secs:02}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("Aguarde 00:00:00          ", end='\r')

def load_tokens(filename):
    """Carrega tokens de um arquivo."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    """Função principal que executa o script."""
    blinking_art(interval=0.5, duration=2)  # Mostra a arte piscando antes de começar o script
    
    run_uf = input(Fore.CYAN + "Você quer atualizar a Fazenda? (S/N): ").strip().upper()
    run_us = input(Fore.CYAN + "Você quer atualizar o Armazém? (S/N): ").strip().upper()
    run_up = input(Fore.CYAN + "Você quer atualizar a População? (S/N): ").strip().upper()
    run_cards = input(Fore.CYAN + "Você quer atualizar os Cartões? (S/N): ").strip().upper()
    
    clear_terminal()
    
    while True:
        tokens = load_tokens('data.txt')
        
        if not tokens:
            print(Fore.RED + Style.BRIGHT + "Nenhum token encontrado.")
            return
    
        for i, token in enumerate(tokens, start=1):
            print(Fore.CYAN + Style.BRIGHT + f"------Conta No.{i}------")
            login(token)
            daily_bonus(token)
            ads(token)
            
            if run_uf == 'S':
                upgrade_farm(token)
            
            if run_us == 'S':
                upgrade_storage(token)
            
            if run_up == 'S':
                upgrade_population(token)
                
            if run_cards == 'S':
                card_details = get_cards(token)
                for card_id, card_name in card_details:
                    post_card_upgrade(card_id, card_name, token)
                            
        countdown_timer(1 * 15 * 60)
        clear_terminal()

if __name__ == "__main__":
    main()