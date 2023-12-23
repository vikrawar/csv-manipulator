from sys import argv, exit
from tabulate import tabulate
import csv
import re
import os

changed = False
sno = 1
keys = []

def main():
    global sno
    if len(argv) != 2 or not re.search(r"^.+\.csv$", argv[1]):
        print("Usage: python csvmanip.py example.csv")
    else:

        data = []
        try:
            with open(argv[1]) as file:
                reader = csv.DictReader(file)
                for lines in reader:
                    tmp = {"S.no": sno}
                    tmp.update(lines)
                    data.append(tmp)
                    sno += 1

                global keys
                keys = [key for key in data[0] if key != "S.no"]

        except FileNotFoundError:
            pass

        opt(data)


def opt(data):
    n = "1"
    invalid = False
    while(n > "0"):
        try:
            if invalid == False:
                print()
                print(tabulate([["Welcome to csv file manipulater. Easily view/edit csv files.\n(enter 0 to save & exit, enter h for more options)"],
                ["1. View\n2. Add\n3. Delete\n4. Update\n5. Save copy"]],tablefmt="fancy_grid"))
                n = input(("Enter an option: ")).lower().strip()
            else:
                n = input(("Please enter a valid option: ")).lower().strip()
            match n:
                case "1" : view(data); invalid = False
                case "2" : add(data); invalid = False
                case "3" : delete(data); invalid = False
                case "4" : update(data); os.system('cls' if os.name == 'nt' else 'clear'); invalid = False
                case "5" : copy(data); invalid = False
                case "0" :
                    done(data)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    exit("\nThank you for using csv file manipulator.\n")
                case "h" | "help": options(); invalid = False
                case _ : invalid = True
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nThank you for using csv file manipulator.\n")
            exit()


def view(data):

    os.system('cls' if os.name == 'nt' else 'clear')
    if len(data) != 0:
        print(tabulate(data, headers="keys",tablefmt="fancy_grid"))

    else:
        if len(keys) == 0:
            print(tabulate(["Empty File"]))
        else:
            print(tabulate([keys],tablefmt="fancy_grid"))

def add(data):
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        print(tabulate([["1. Add row\n2. Add column\n0. Back"]],
        tablefmt="fancy_grid"))
        n = input("Enter an option: ")
        match n:
                case "1" : get_keys(data)
                case "2" : add_column(data)
                case "0" : os.system('cls' if os.name == 'nt' else 'clear'); opt(data)
                case _ : print("Please enter a valid option!")


def get_keys(data):
    global keys

    if len(data) == 0:

        if len(keys) != 0:
            pass

        else:
            print(tabulate(["Empty File"]))

            while True:
                try:
                    k = int(input("How many keys to add? "))
                    break
                except ValueError:
                    pass

            keys = []
            for i in range(k):
                match i:
                    case 0: keys.append(input("1st key: "))
                    case 1: keys.append(input("2nd key: "))
                    case 2: keys.append(input("3rd key: "))
                    case _: keys.append(input(f"{i+1}th key: "))

    add_rows(data,keys)


def add_rows(data,keys):
    global sno
    global changed
    while True:
        try:
            n = int(input("How many rows to add? "))
            break
        except ValueError:
            pass

    for i in range(n):
        row = {"S.no": sno}
        print()
        for j in range(len(keys)):
            value = input(f"{i+1}. {keys[j]}: ")
            row[keys[j]] = value

        data.append(row)
        sno += 1

    changed = True
    add(data)


def add_column(data):
    global keys
    global changed

    while True:
        try:
            k = int(input("How many keys to add? "))
            break
        except ValueError:
            pass

    for i in range(k):
        match i:
            case 0: keys.append(input("1st key: "))
            case 1: keys.append(input("2nd key: "))
            case 2: keys.append(input("3rd key: "))
            case _: keys.append(input(f"{i+1}th key: "))

    for rows in data:
        for k in keys:
            if not k in rows:
                rows[k] = None

    changed = True


def delete(data):

    os.system('cls' if os.name == 'nt' else 'clear')

    if len(data) == 0 and len(keys) == 0:
        print(tabulate(["Empty File"]))
        opt(data)

    else:

        while True:
            print(tabulate([["1. Delete row\n2. Delete column\n0. Back"]],
            tablefmt="fancy_grid"))
            n = input("Enter an option: ")
            match n:
                case "1" : delete_row(data)
                case "2" : delete_column(data)
                case "0" : os.system('cls' if os.name == 'nt' else 'clear'); opt(data)
                case _ : print("Please enter a valid option!")


def delete_row(data):

    os.system('cls' if os.name == 'nt' else 'clear')

    if len(data) == 0:
        print(tabulate(["Empty File"]))
        opt(data)
    else:
        while True:
            print(tabulate([["Enter the S.no of the row to delete\n\
            (enter 'v' to view table, enter '0' to go back)"]],tablefmt="fancy_grid"))
            n = input("Enter an option: ")

            match n:
                case "0" : delete(data)
                case "v" : view(data)
                case _ :
                    deleted = False
                    for i in range(len(data)):
                        if str(data[i]["S.no"]) == n:
                            del data[i]
                            print("Deleted")
                            deleted = True
                            global changed
                            global sno
                            changed = True

                            for x in range(i, len(data)):
                                data[x]["S.no"] -= 1
                            sno -= 1
                            break
                    if deleted == False:
                        print(tabulate(["S.no not found"]))


def delete_column(data):

    os.system('cls' if os.name == 'nt' else 'clear')
    global keys
    print("Which column do you want to delete?")

    for key in keys:
        print(key, end="   ")
    print()
    x = input("Enter the column name: ").strip().lower()

    if x in keys:
        for row in data:
            del row[x]
        global changed
        changed = True
        keys.remove(x)
        print("Deleted column")
    else:
        print(tabulate(["NO SUCH COLUMN"]))



def update(data):

    os.system('cls' if os.name == 'nt' else 'clear')
    if len(data) == 0:
        print(tabulate(["Empty File"]))
        opt(data)

    while True:
        print(tabulate([["1. Update whole row\n2. Update an entry of a row\n\
3. Update name of a column\n4. Update values of a whole column\n0. Back"]],tablefmt="fancy_grid"))
        n = input("Enter an option: ")
        match n:
            case "1": update_row(data)
            case "2": update_entry(data)
            case "3": update_key(data)
            case "4": update_column(data)
            case "0": os.system('cls' if os.name == 'nt' else 'clear'); opt(data)
            case _: print("Invalid option")


def update_row(data):
    while True:
        print("S.no of row to update\n(enter 'v' to view table, enter '0' to go back)")
        n = input("Enter an option: ")
        match n:
            case "v": view(data)
            case "0": update(data)
            case _:
                deleted = False
                for i in range(len(data)):
                    if str(data[i]["S.no"]) == n:

                        for x in data[i]:
                            if x != "S.no":
                                data[i][x] = input(f"{x}: ")
                        print("Updated")
                        deleted = True
                        global changed
                        changed = True
                        break
                if deleted == False:
                    print(tabulate(["S.no not found"]))


def update_entry(data):
    while True:
        print("S.no of row to update\n(enter 'v' to view table, enter '0' to go back)")
        n = input("Enter an option: ")
        match n:
            case "v": view(data)
            case "0": update(data)
            case _:

                deleted = False
                for i in range(len(data)):
                    if str(data[i]["S.no"]) == n:
                        print(tabulate([data[i]], headers="keys",tablefmt="fancy_grid"))

                        while True:
                            x = input("Which column to update: ").strip()
                            if x == "S.no":
                                print("S.no doesn't actually exist in the csv file.\nIts just for reference")
                            elif x not in data[i]:
                                print("No such column")
                            else:
                                data[i][x] = input(f"{x}: ")
                                break
                        print("Updated")
                        deleted = True
                        global changed
                        changed = True
                        break
                if deleted == False:
                    print(tabulate(["S.no not found"]))


def update_key(data):
    print(tabulate([keys],tablefmt="fancy_grid"))
    while True:
        x = input("Which column name do you want to change: ").strip()
        found = False

        for i in range(len(keys)):
            if keys[i] == x:
                old_key = keys[i]
                keys[i] = input("New heading: ")
                new_key = keys[i]
                found = True

                for j in range(len(data)):
                    tmp = {}
                    for key in data[j]:
                        if key == old_key:
                            tmp.update({new_key: data[j][old_key]})
                        else:
                            tmp.update({key: data[j][key]})
                    data[j] = tmp

                print("Updated")
                update(data)
        if found == False:
            print(tabulate(["Invalid option"]))

def update_column(data):
    print(tabulate([keys],tablefmt="fancy_grid"))
    while True:
        x = input("Which column entries do you want to update: ").strip()
        found = False

        for i in range(len(keys)):
            if keys[i] == x:
                found = True
                ans = input("Enter the values: ")
                for rows in data:
                    rows[x] = ans

                print("Updated")
                update(data)
        if found == False:
            print(tabulate(["Invalid option"]))


def copy(data):

    while True:
        print(tabulate([["enter 0 to go back"]],tablefmt="fancy_grid"))
        name = input("Enter name of the new file: ").strip()

        if not name or name == ".csv":
            print("Name can't be blank")
        else:
            if name.endswith(".csv"):
                save(data, name)
            else:
                save(data, name + ".csv")
            print("Saved")
            break


def options():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("if you exit the program without entering '0', changes made will not be saved.\n\
type exactly as prompted")


def done(data):

    if changed == False:
        pass
    else:
        save(data, argv[1])


def save(data, name):

    tmp = data.copy()

    for row in tmp:
        del row["S.no"]

    with open(name, "w") as file:
        key_writer = csv.writer(file)
        key_writer.writerow(keys)
        writer = csv.DictWriter(file,[*keys])
        for i in tmp:
            writer.writerow(i)


if __name__ == "__main__":
    main()