import sublime, sublime_plugin, os, sys, re, subprocess

ST_MAIN_PROGRAM = 'sublime_text.exe'

# ST2: main program path isn't included in sys.path, but sys.executable points to the main program. 
def isAppExist2(app_name):
    st_path = os.path.dirname(sys.executable)
    absPath = st_path + "\\" + app_name
    if(os.path.isfile(absPath)):
        return True, absPath
    return False, ""

# ST3: main program path is included in sys.path. 
def isAppExist3(app_name):
    for dirName in sys.path:
        if(os.path.isfile(dirName + "\\" + ST_MAIN_PROGRAM)):
            absPath = dirName + "\\" + app_name
            if(os.path.isfile(absPath)):
                return True, absPath
    return False, ""

def findApp(app_name):
    if sys.version_info[0] == 2:
        return isAppExist2(app_name)
    else:
        return isAppExist3(app_name)

def set_window_transparency_nt(pid, alpha, app_title, app_name):
    found, app_path = findApp(app_name)
    if(found):
        command = "\"" + app_path + "\"" + " " + str(pid) + " " + str(alpha) + " " + app_title
        subprocess.Popen(command, shell=True)
        print("Sublime window transparency is set to %d" %(alpha))
    else:
        print("Cannot find %s! Please download and put into sublime path." %(app_name))

def update_window_transparency_nt():
    set_window_transparency_nt(config.st_pid, config.alpha_current, config.st_title, config.app_name)

def plugin_loaded():
    settings = sublime.load_settings('glassit.sublime-settings')

    global config

    class config:
        def load(self):
            if (sublime.platform() == "windows"):
                config.alpha_per_default = int(settings.get('alpha_percentage', 90))
                config.alpha_step = int(settings.get('alpha_step', 5))
                config.app_name = settings.get('application', "SetTransparency.exe")
                config.st_title = settings.get('st_title', "Sublime Text")
                if sys.version_info[0] == 2:
                    # ST2 load plugin within main process
                    config.st_pid = os.getpid()
                else:
                    # ST3 load plugin in the child process "plugin_host.exe"
                    config.st_pid = os.getppid()

                config.enable = True

                config.alpha_per_current = config.alpha_per_default
                config.alpha_per_last = config.alpha_per_current
                config.alpha_current = 255 * config.alpha_per_current / 100
                config.delay = 5000
            else:
                print("Set transparency doesn't support this platform yet!")

    config = config()
    config.load()

    if (sublime.platform() == "windows"):
        # Delay set transparency until main window is created.
        sublime.set_timeout(update_window_transparency_nt, config.delay)
    else:
        print("Set transparency doesn't support this platform yet!")

    settings.add_on_change('reload', lambda:config.load())

if sys.version_info[0] == 2:
    plugin_loaded()

class ToggleTransparencyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if (config.enable == True):
            config.enable = False
            config.alpha_per_current = 100
            config.alpha_current = 255 * config.alpha_per_current / 100
            update_window_transparency_nt()
        else:
            config.enable = True
            config.alpha_per_current = config.alpha_per_last
            config.alpha_current = 255 * config.alpha_per_current / 100
            update_window_transparency_nt()

    def is_checked(self, **args):
        if (config.enable == True):
            return True
        else:
            return False

class ResetTransparencyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if(config.enable == True):
            config.alpha_per_current = config.alpha_per_default
            config.alpha_per_last = config.alpha_per_current
            config.alpha_current = 255 * config.alpha_per_current / 100
            update_window_transparency_nt()

class IncreaseTransparencyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if(config.enable == True):
            config.alpha_per_current = config.alpha_per_current - config.alpha_step
            if(config.alpha_per_current < 0):
                config.alpha_per_current = 0
            config.alpha_per_last = config.alpha_per_current
            config.alpha_current = 255 * config.alpha_per_current / 100
            update_window_transparency_nt()

class DecreaseTransparencyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if(config.enable == True):
            config.alpha_per_current = config.alpha_per_current + config.alpha_step
            if(config.alpha_per_current > 100):
                config.alpha_per_current = 100
            config.alpha_per_last = config.alpha_per_current
            config.alpha_current = 255 * config.alpha_per_current / 100
            update_window_transparency_nt()
