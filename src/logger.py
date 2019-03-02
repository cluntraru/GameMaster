class Logger:
    DEBUG_MODE = None
    SPEAK_MODE = None

    def __init__(self, debug_mode, speak_mode):
        Logger.DEBUG_MODE = debug_mode
        Logger.SPEAK_MODE = speak_mode


    def log_info(self, text):
        print(text)


    def log_debug(self, text):
        if Logger.DEBUG_MODE:
            print(text)


    def is_debug_mode(self):
        ''' Returns if debug mode is enabled. '''
        return Logger.DEBUG_MODE


    def is_speak_mode(self):
        ''' Returns if speak mode is enabled. '''
        return Logger.SPEAK_MODE
