################################################################################
#   GENERIC   ##################################################################

ANSI_FG_BLACK   = u"\u001b[30m"
ANSI_FG_RED     = u"\u001b[31m"
ANSI_FG_GREEN   = u"\u001b[32m"
ANSI_FG_YELLOW  = u"\u001b[33m"
ANSI_FG_BLUE    = u"\u001b[34m"
ANSI_FG_MAGENTA = u"\u001b[35m"
ANSI_FG_CYAN    = u"\u001b[36m"
ANSI_FG_WHITE   = u"\u001b[37m"

ANSI_BG_BLACK   = u"\u001b[40m"
ANSI_BG_RED     = u"\u001b[41m"
ANSI_BG_GREEN   = u"\u001b[42m"
ANSI_BG_YELLOW  = u"\u001b[43m"
ANSI_BG_BLUE    = u"\u001b[44m"
ANSI_BG_MAGENTA = u"\u001b[45m"
ANSI_BG_CYAN    = u"\u001b[46m"
ANSI_BG_WHITE   = u"\u001b[47m"

ANSI_BOLD       = u"\u001b[1m"

ANSI_RESET      = u"\u001b[0m"

################################################################################
#   PFS Colours   ##############################################################

COMMAND = ANSI_FG_MAGENTA
OKAY = ANSI_FG_GREEN
USER = ANSI_FG_YELLOW
WARN = ANSI_FG_RED
     
C_SCS = ANSI_FG_BLACK + ANSI_BG_GREEN # ??
C_ALT = ANSI_FG_BLACK + ANSI_BG_YELLOW # ??
ERROR = ANSI_FG_YELLOW + ANSI_BG_RED
     
C_SPL = ANSI_FG_RED + ANSI_BOLD
     
RESET = ANSI_RESET

col = {
        "cmd" : COMMAND,
        "okay" : OKAY,
        "user" : USER,
        "warn" : WARN,
        "error" : ERROR,
        "reset" : RESET
}
