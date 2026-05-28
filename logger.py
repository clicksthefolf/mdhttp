import colorama

class Log:
    @staticmethod
    def success(text):
        print(f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}{text}{colorama.Fore.RESET}{colorama.Style.RESET_ALL}")
    @staticmethod
    def message(text):
        print(f"{text}")
    @staticmethod
    def warning(text):
        print(f"{colorama.Fore.YELLOW}{colorama.Style.BRIGHT}{text}{colorama.Fore.RESET}{colorama.Style.RESET_ALL}")
    @staticmethod
    def error(text):
        print(f"{colorama.Fore.RED}{colorama.Style.BRIGHT}{text}{colorama.Fore.RESET}{colorama.Style.RESET_ALL}")