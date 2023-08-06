class LogLevel:
    from colorama import Fore as __Fore

    def __init__(self, name, color: str = __Fore, isFatal: bool = False):
        self.name = name
        self.color = color
        self.isFatal = isFatal

    def log(self, message):
        logger = Logger()
        logger.log(message, self)
        if self.isFatal and logger.quitWhenLogFatal:
            quit()


class Logger:
    from colorama import Fore as __Fore

    def __init__(self,
                 logLevel: bool = True,
                 colorLevelText: bool = True,
                 quitWhenLogFatal: bool = False,
                 colorText: bool = True,
                 warnLevel: LogLevel = LogLevel("WARN", __Fore.YELLOW),
                 infoLevel: LogLevel = LogLevel("INFO", __Fore.RESET),
                 debugLevel: LogLevel = LogLevel("DEBUG", __Fore.WHITE),
                 errorLevel: LogLevel = LogLevel("ERROR", __Fore.LIGHTRED_EX),
                 fatalLevel: LogLevel = LogLevel("FATAL", __Fore.RED, isFatal=True)):

        self.logLevel = logLevel
        self.colorLevelText = colorLevelText
        self.quitWhenLogFatal = quitWhenLogFatal
        self.colorText = colorText
        self.warnLevel = warnLevel
        self.infoLevel = infoLevel
        self.debugLevel = debugLevel
        self.errorLevel = errorLevel
        self.fatalLevel = fatalLevel

    def log(self, message: str, level: LogLevel = None, end: str = "\n"):
        from datetime import datetime
        from colorama import Fore
        if not level:
            level = self.debugLevel

        current_time = datetime.now()
        if self.colorText:
            if self.logLevel:
                print(
                    f"[{current_time.strftime('%X')}] {level.color if self.colorLevelText else Fore.RESET}[{level.name}]",
                    level.color + str(message), end=end + Fore.RESET)

            else:
                print(f"[{current_time.strftime('%X')}]", level.color + str(message), end=end + Fore.RESET)
        else:
            if self.logLevel:
                print(f"[{current_time.strftime('%X')}] [{level.name}]",
                      str(message), end=end)

            else:
                print(f"[{current_time.strftime('%X')}]", str(message), end=end)

    def log_warning(self, message: str):
        self.log(message, self.warnLevel)

    def log_info(self, message: str):
        self.log(message, self.infoLevel)

    def log_debug(self, message: str):
        self.log(message, self.debugLevel)

    def log_error(self, message: str):
        self.log(message, self.errorLevel)

    def log_fatal(self, message: str, exception=""):
        self.log(message, self.fatalLevel)
        if self.quitWhenLogFatal:
            quit(exception)
