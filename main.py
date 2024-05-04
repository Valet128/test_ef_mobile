import os
import csv
import datetime

# проверка на наличие папки wallets если нет то создаем, также сразу добавляем путь к располжению исполняемого файла
file = os.path.realpath(__file__)
path = os.path.dirname(file)
wallets_path = path+'/wallets'
check_folder = os.path.isdir(wallets_path)

if not check_folder:
    os.mkdir(wallets_path)

# В данном коде много семантики, поэтому аннотации к каждой переменной являются излишни.    
# Класс кошелька для работы с данными 

class Wallet:    
    balance = 0
    incomes = 0
    expenses = 0
    new_note = {}
    all_notes = []
        

# Основной метод для запуска приложения

def main():
    print("Добро пожаловать в приложение VASHKASH!")
# Описание функционала программы и команд
    print("""
# Команды для приложения:
#     0 - Закрыть приложение 
#     1 - Создать новый кошелек 
#     2 - Открыть свой кошелек 
#     3 - Удалить кошелек
# Команды для кошелька:
#     0 - Предыдущее меню
#     1 - Показать баланс 
#     2 - Показать доходы 
#     3 - Показать расходы   
#     4 - Добавить новую запись   
#     5 - Редактировать запись
#     6 - Удалить запись
#     7 - Показать все записи
#     8 - Поиск
#           Команды для поиска:
#                0 - Предыдущее меню
#                1 - По дате 
#                2 - По сумме 
#                3 - По категории
    """)
    print("Создайте свой кошелек в 1 клик")
    
    # Запуск бесконечного цикла для работы приложения
    app_run = True
    while app_run == True:
        # Названия колонок в таблице записей
        columns = ['Id','Category','Amount','Description','Date']
        # Оборачиваем все в try except для избежания аварийных выходов приложения
        try:
            command = int(input("Введите команду для приложения: "))
            if command == 1:
                #добавляем новый кошелек, сразу считаем сколько у нас уже таких кошельков чтобы не заменять, а создавать новый.
                wallets_number = len(os.listdir(wallets_path))
                with open(f'{wallets_path}/wallet_{wallets_number+1}.csv', 'w', encoding='utf-8', newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=columns, delimiter=',')
                    writer.writeheader()
                print(f"""Кошелек успешно создан! ID Вашего кошелька: "{wallets_number+1}" 
                    Запомните его чтобы затем использовать при входе в приложение!""")
            elif command == 2:
                # входим в меню кошелька если он существует
                try:
                    id = int(input("Введите ID кошелька: "))
                except:
                    print("Ввести можно только числа!")
                if os.path.exists(f"{wallets_path}/wallet_{id}.csv"):
                    # создаем объект класса Wallet для работы с данными
                    my_wallet = Wallet()
                    # подгружаем все записи кошелька если они есть
                    with open(f'{wallets_path}/wallet_{id}.csv', 'r', encoding='utf-8', newline="") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            my_wallet.all_notes.append(row)
                        for row in my_wallet.all_notes:
                            print(f"{row}")
                    # не забываем чистить список для правильной дальнейшей работы
                    my_wallet.all_notes.clear()
                    print("Кошелек успешно открыт!")
                    wallet_run = True
                    # запускаем подменю для работы с кошельком
                    while wallet_run == True:
                        try:
                            wallets_command = int(input("Введите команду для кошелька: "))
                            
                            # Показать баланс --------------------------------

                            if wallets_command == 1:
                                with open(f'{wallets_path}/wallet_{id}.csv', 'r', encoding='utf-8', newline="") as file:
                                    reader = csv.DictReader(file)
                                    for row in reader:
                                        if row['Category'] == 'Расход':
                                            my_wallet.expenses += int(row['Amount'])
                                        else:
                                            my_wallet.incomes += int(row['Amount'])
                                    my_wallet.balance = my_wallet.incomes - my_wallet.expenses
                                    print(f'Баланс кошелька: {my_wallet.balance}руб.')
                                    my_wallet.incomes = 0
                                    my_wallet.expenses = 0
                            # Показать только доход --------------------------------

                            elif wallets_command == 2:
                                with open(f'{wallets_path}/wallet_{id}.csv', 'r', encoding='utf-8', newline="") as file:
                                    reader = csv.DictReader(file)
                                    for row in reader:
                                        if row['Category'] == 'Доход':
                                            my_wallet.incomes += int(row['Amount'])
                                    
                                    print(f'Доход: {my_wallet.incomes}руб.')
                                    my_wallet.incomes = 0
                            # Показать только расход --------------------------------

                            elif wallets_command == 3:
                                with open(f'{wallets_path}/wallet_{id}.csv', 'r', encoding='utf-8', newline="") as file:
                                    reader = csv.DictReader(file)
                                    for row in reader:
                                        if row['Category'] == 'Расход':
                                            my_wallet.expenses += int(row['Amount'])
                                    
                                    print(f'Расход: {my_wallet.expenses}руб.')
                                    my_wallet.expenses = 0
                            # Добавить новую запись --------------------------------

                            elif wallets_command == 4:
                                count = 0
                                with open(f'{wallets_path}/wallet_{id}.csv', 'r', encoding='utf-8', newline="") as file:
                                    reader = csv.DictReader(file)
                                    for row in reader:
                                        count +=1
                                my_wallet.new_note['Id'] = count + 1
                                try:
                                    category = int(input('1 = ДОХОД, 2 = РАСХОД, 0 = ОТМЕНА: '))
                                    if category == 1:
                                        my_wallet.new_note['Category'] = 'Доход'
                                    elif category == 2:
                                        my_wallet.new_note['Category'] = 'Расход'
                                    else:
                                        raise ValueError("Операция отменена!")
                                        
                                        
                                    try:
                                        my_wallet.new_note['Amount'] = abs(int(input("Введите сумму: ")))
                                        my_wallet.new_note['Description'] = input("Введите описание: ")
                                        my_wallet.new_note['Date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                                        
                                        with open(f'{wallets_path}/wallet_{id}.csv', 'a', encoding='utf-8', newline="") as file:
                                            writer = csv.DictWriter(file, delimiter=',', fieldnames=columns)
                                            writer.writerow(my_wallet.new_note)

                                    except:
                                        print("Операция отменена.")
                                        print("Ввести можно только числа!")
                                except:
                                    print("Операция отменена.")
                                    print("Ввести можно только числа!")

                            # Редактировать запись --------------------------------

                            elif wallets_command == 5:
                                try:
                                    note_id = int(input('Введите ID записи: '))
                                    count = 0
                                    with open(f'{wallets_path}/wallet_{id}.csv', 'r', encoding='utf-8', newline="") as file:
                                        reader = csv.DictReader(file)
                                        for row in reader:
                                            my_wallet.all_notes.append(row)
                                    for row in my_wallet.all_notes:
                                        if int(row['Id']) == note_id:
                                            print(f"Запись которую вы хотите изменить: \n {row}")
                                            new_category = int(input('Введите 1 = ДОХОД, 2 = РАСХОД, 0 = ОТМЕНА: '))
                                            if new_category == 1:
                                                row['Category'] = "Доход"
                                            elif new_category == 2:
                                                row['Category'] = "Расход"
                                            else:
                                                print("Операция отменена.")
                                                break
                                            row['Amount'] = int(input("Введите новую сумму: "))
                                            row['Description'] = input("Введите новое описание: ")
                                            # row['Date'] = datetime.datetime.now().strftime("%Y-%m-%d") Не всегда нужно менять дату при изменении записи.
                                            break
                                    with open(f'{wallets_path}/wallet_{id}.csv', 'w', encoding='utf-8', newline="") as file:
                                        writer = csv.DictWriter(file, fieldnames=columns, delimiter=',')
                                        writer.writeheader() 
                                        writer.writerows(my_wallet.all_notes)
                                    my_wallet.all_notes.clear()
                                except:
                                    print("Операция отменена.")
                                    print("Ввести можно только числа!")

                            # Удалить запись --------------------------------

                            elif wallets_command == 6:
                                try:
                                    note_id = int(input('Введите ID записи: '))
                                    count = 0
                                    with open(f'{wallets_path}/wallet_{id}.csv', 'r', encoding='utf-8', newline="") as file:
                                        reader = csv.DictReader(file)
                                        for row in reader:
                                            my_wallet.all_notes.append(row)
                                    for row in my_wallet.all_notes:
                                        if int(row['Id']) == note_id:
                                            print(f"Запись которую вы хотите Удалить: \n {row}")
                                            try:
                                                confirm = int(input("Вы действительно хотите удалить запись? 1 = Да, 2 = Нет: "))
                                                if confirm == 1:
                                                    my_wallet.all_notes.remove(row)
                                                    with open(f'{wallets_path}/wallet_{id}.csv', 'w', encoding='utf-8', newline="") as file:
                                                        writer = csv.DictWriter(file, fieldnames=columns, delimiter=',')
                                                        writer.writeheader() 
                                                        writer.writerows(my_wallet.all_notes)
                                                    print("Запись успешно удалена!")
                                                    my_wallet.all_notes.clear()
                                                else:
                                                    print("Операция отменена.")
                                                    my_wallet.all_notes.clear()
                                            except:
                                                print("Операция отменена.")
                                                print("Ввести можно только числа!")
                                            break
                                except:
                                    print("Операция отменена.")
                                    print("Ввести можно только числа!")

                            # Показать все записи --------------------------------

                            elif wallets_command == 7:
                                with open(f'{wallets_path}/wallet_{id}.csv', 'r', encoding='utf-8', newline="") as file:
                                    reader = csv.DictReader(file)
                                    for row in reader:
                                        my_wallet.all_notes.append(row)
                                    for row in my_wallet.all_notes:
                                        print(f"{row}")
                                my_wallet.all_notes.clear()
                            # Поиск --------------------------------

                            elif wallets_command == 8:
                                filter_wallet_run = True
                                while filter_wallet_run == True:
                                    try:
                                        with open(f'{wallets_path}/wallet_{id}.csv', 'r', encoding='utf-8', newline="") as file:
                                            reader = csv.DictReader(file)
                                            for row in reader:
                                                my_wallet.all_notes.append(row)
                                        
                                        filter_wallets_command = int(input("Введите команду для поиска: "))
                                        if filter_wallets_command == 1:
                                            matches = 0
                                            search_date = input("Введите дату для поиска в формате YYYY-MM-DD: ")
                                            for row in my_wallet.all_notes:
                                                if row['Date'] == search_date:
                                                    print(f"{row}")
                                                    matches += 1
                                            if matches == 0:
                                                print("Совпадений не найдено!")
                                        elif filter_wallets_command == 2:
                                            matches = 0
                                            try:
                                                search_amount = int(input("Введите сумму для поиска: "))
                                                for row in my_wallet.all_notes:
                                                    if int(row['Amount']) == search_amount:
                                                        print(f"{row}")
                                                        matches += 1
                                                if matches == 0:
                                                    print("Совпадений не найдено!")
                                            except:
                                                print("Операция отменена.")
                                                print("Ввести можно только числа!")
                                        elif filter_wallets_command == 3:
                                            matches = 0
                                            search_category = input("Введите категорию для поиска в формате Доход или Расход: ")
                                            for row in my_wallet.all_notes:
                                                    if row['Category'].lower() == search_category.lower():
                                                        print(f"{row}")
                                                        matches += 1
                                            if matches == 0:
                                                print("Совпадений не найдено!")
                                        elif filter_wallets_command == 0:
                                            filter_wallet_run = False
                                        else:
                                            print("Неизвестная команда!")
                                        my_wallet.all_notes.clear()
                                    except:
                                        print("Операция отменена.")
                                        print("Ввести можно только числа!")
                                    
                            elif wallets_command == 0:
                                wallet_run = False
                            else:
                                print("Неизвестная команда!")
                        except:
                            print("Операция отменена.")
                            print("Ввести можно только числа!")

                else:
                    print("Такого кошелька не существует!")
            elif command == 3:
            # если есть желание можно удалить кошелек
                try:
                    delete_wallet = int(input("Введите ID кошелька который хотите удалить: "))
                except:
                    print("Операция отменена.")
                    print("Ввести можно только числа!")
                if os.path.exists(f"{wallets_path}/wallet_{delete_wallet}.csv"):
                    os.remove(f"{wallets_path}/wallet_{delete_wallet}.csv")
                    print("Кошелек успешно удален!")
            elif command == 0:
            # выход из программы
                print("До встречи!")
                app_run = False
            else:
                print("Неизвестная команда!")
        except:
            print("Операция отменена.")
            print("Ввести можно только числа!")
        



# проверка на текущий модуль     
if __name__ == "__main__":
    main()



