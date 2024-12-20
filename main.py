import requests
import time
import os
import random
from prettytable import PrettyTable
from colorama import Fore, Style

def generate_email():
    domains = ["1secmail.com", "1secmail.net", "1secmail.org"]
    username = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=10))
    domain = random.choice(domains)
    email = f"{username}@{domain}"
    print(Fore.GREEN + f"Generated Email: {email}" + Style.RESET_ALL)
    return username, domain, email


def fetch_messages(username, domain):
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
    response = requests.get(url).json()
    return response


def fetch_message_content(username, domain, message_id):
    url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={message_id}"
    response = requests.get(url).json()
    return response


def display_messages(messages):
    if not messages:
        print(Fore.YELLOW + "No new messages yet." + Style.RESET_ALL)
        return

    table = PrettyTable(["From", "Subject", "Date"])
    for message in messages:
        table.add_row([message['from'], message['subject'], message['date']])
    print(Fore.CYAN + str(table) + Style.RESET_ALL)


def main():
    print(Fore.MAGENTA + "Welcome to 1SecMail CLI" + Style.RESET_ALL)
    username, domain, email = generate_email()

    try:
        while True:
            messages = fetch_messages(username, domain)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.MAGENTA + "Listening for new messages..." + Style.RESET_ALL)
            print(Fore.GREEN + f"Generated Email: {email}" + Style.RESET_ALL)
            display_messages(messages)

            for message in messages:
                content = fetch_message_content(username, domain, message['id'])
                print(Fore.BLUE + f"\nMessage from: {content['from']}" + Style.RESET_ALL)
                print(Fore.GREEN + f"Subject: {content['subject']}" + Style.RESET_ALL)
                print(Fore.WHITE + f"Body:\n{content['textBody']}\n" + Style.RESET_ALL)

            time.sleep(10)
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting..." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
