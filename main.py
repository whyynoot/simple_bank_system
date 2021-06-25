import string
import random

# HSE Exam : )

def load_data():
    base = {}
    file = open('bankdata.txt', 'r')
    for line in file:
        info = line.split(';')
        if len(info) > 3:
            base.update({info[0] : [[info[1], info[2]], info[3].replace('\n', '')]})
            for i in range(int(info[3].replace('\n', ''))):
                line = next(file).split(';')
                if len(line) >= 1:
                    base[info[0]].append([line[0], line[1].replace('\n', '')])
    file.close()
    return base

def check_for_login(user, password):
    flag = False
    for person in base:
        if (base[person][0][0] == user) and (base[person][0][1] == password):
            flag = person
    return flag

def list_accounts(session):
    for i in range(int(base[session][1])):
        print(f"{i + 1}. {base[session][i + 2][0]} | {base[session][i + 2][1]} RUB")
    print('')

def transfer_money(session):
    list_accounts(session)
    source = int(input('Select the source account: '))
    target = int(input('Select the target account: '))
    if (source == target):
        print('Same source and target.\nTry again.')
        return transfer_money(session)
    amount = int(input('Enter the amount to transfer: '))
    if (amount <= 0):
        print('Wrong amount on transfer\nTry again.')
        return transfer_money(session)
    try:
        if amount <= int(base[session][source + 1][1]):
            base[session][source + 1][1] = int(base[session][source + 1][1]) - amount
            base[session][target + 1][1] = int(base[session][target + 1][1]) + amount
        else:
            print('No such amount on source[or other error], try again.')
            return transfer_money(session)
    except:
        return transfer_money(session)
    list_accounts(session)
    save_data()

def save_data():
    file = open('bankdata.txt', 'w')
    for person in base:
        file.write(f"{person};{base[person][0][0]};{base[person][0][1]};{base[person][1]}\n")
        for i in range(int(base[person][1])):
            file.write(f"{base[person][i + 2][0]};{base[person][i + 2][1]}\n")
    file.close()

def open_account(session):
    flag = True
    S = 16
    ran = ''.join(random.choices(string.digits + string.digits, k=S))
    for person in base:
        for i in range(int(base[person][1])):
            if base[person][i + 2][0] == ran:
                flag = False
    if flag:
        base[session].append([ran, '0'])
        base[session][1] = int(base[session][1]) + 1
        print("Successfully opened a new account!")
    save_data()

def main():
    username = input("Enter your username: ")
    password = input('Enter password: ')
    session = check_for_login(username, password)
    if session:
        print(f"Welcome, {session}")
        while(session):
            action = input('''1 - list accounts
2 - transfer money
3 - open a new account
4 - logout
Choose an action: ''')
            try:
                action_n = int(action)
                if action_n == 1:
                    list_accounts(session)
                if action_n == 2:
                    transfer_money(session)
                if action_n == 3:
                    open_account(session)
                if action_n == 4:
                    return main()
            except:
                print('Wrong  action')
    if not session:
        print("Wrong user or password")
        return main()


if __name__ == '__main__':
    base = load_data()
    print('Welcome to the online bank!')
    while True:
        main()

