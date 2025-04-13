from windows.win_comp import pccomponents_windows
from usystem import usystem

def main():
    system = usystem()[1]
    s = usystem()[0]
    if system == "Windows":
        print(pccomponents_windows(usystem()[0]))
        s = pccomponents_windows(usystem()[0])
    else:
        error_text = "Работает только на Windows!"
        print(error_text)
        s += error_text
    with open("result.txt", "w", encoding="utf-8") as file:
            file.write(f"{s}")

if __name__ == "__main__":
    main()