# spyl
a simple python logger

# how to use

* ## downloading the logger and installing required libraries

1. download the logger and add to your project `pip install spyl`
* ## personalizing the logger
* when instantiating the `Logger` class you can configure a few parameters about the logger
* `logLevel`, default to `True` - will the logger print out the level label e.g. if set to true: `[12:00:00] [LEVEL] message` if set to false `[12:00:00] message`
* `colorLevelText`, default to `True` - will the level label get colored
* `quitWhenLogFatal`, default to `False` - will the program quit when something with the fatal level is logged
* `colorText`, default to `True` - will the message get colored
* `warnLevel`, an instance of `LogLevel`, default to `LogLevel("WARN", Fore.YELLOW)`
* `infoLevel`, an instance of `LogLevel`, default to `LogLevel("INFO", Fore.RESET)`
* `debugLevel`, an instance of `LogLevel`, default to `LogLevel("DEBUG", Fore.WHITE)`
* `errorLevel`, an instance of `LogLevel`, default to `LogLevel("ERROR", Fore.LIGHTRED_EX),`
* `fatalLevel`, an instance of `LogLevel`, default to `LogLevel("FATAL", Fore.RED, isFatal=True)`
* ## logging default levels

1. import the library using `import spyl`
2. create an instance of the `Logger` class `logger = spyl.Logger()`

* to log a warning use the `logger.log_warning` function
* to log an info message use the `logger.log_info` function
* to log a debug message use the `logger.log_debug` function
* to log an error use the `logger.log_error` function
* to log a fatal error use the `logger.log_fatal` function

* ## adding additional custom levels

1. import the library using `import spyl`
2. import the colorama library using `from colorama import Fore`
3. create an instance of the `Logger` class `logger = spyl.Logger()`
4. create an instance of the `LogLevel` class `customLevel = spyl.LogLevel("CUSTOM", Fore.GREEN, isFatal=False)`
* the `LogLevel` class has a few parameters which can be configured
* `name` - the name/label of the level
* `color` - the color in which the level will be logged
* `isFatal`, default to `False`- is the level fatal (this in important because if it is and `logger.quitWhenLogFatal` is set to true and the level is fatal the program will exit when logged) 
5. log the custom level using `logger.log("message", customLevel)` or `customLevel.log("message")`