import sublime, sublime_plugin, os, sys, re, subprocess

def findApp(app_name):
    # ST2: main program path isn't included in sys.path, but sys.executable points to the main program.
    if sys.version_info[0] == 2:
        st_path = os.path.dirname(sys.executable)
    else:
        # ST3 & ST4: main program path from sublime.executable_path()
        st_path = os.path.dirname(sublime.executable_path())

    absPath = st_path + "\\" + app_name
    if(os.path.isfile(absPath)):
        return True, absPath
    return False, ""

def findAppAlt(app_name):
    absPathAlt = os.path.join(config.app_path_alt, app_name)
    if (os.path.isfile(absPathAlt)):
        return True, absPathAlt
    return False, ""

def set_window_transparency_nt(pid, alpha, app_title, app_name):
    found, app_path = findApp(app_name)
    if (not found):
        found, app_path = findAppAlt(app_name)
    if(found):
        command = "\"" + app_path + "\"" + " " + str(pid) + " " + str(alpha) + " " + app_title
        subprocess.Popen(command, shell=True)
        print('Using transparency utility from "%s"' %(app_path))
        print("Sublime window transparency is set to %d" %(alpha))
    else:
        print("Cannot find %s! Please download and put into sublime path or application_path_alt." %(app_name))
    return found

def update_window_transparency_nt():
    if (set_window_transparency_nt(config.st_pid, config.alpha_current if config.enabled else config.alpha_max, config.st_title, config.app_name)):
        if (config.enabled_saved != config.enabled or config.alpha_per_current_saved != config.alpha_per_current):
            if (config.enabled_saved != config.enabled):
                config.settings.set('enabled', config.enabled)
                config.enabled_saved = config.enabled
            if (config.alpha_per_current_saved != config.alpha_per_current):
                config.settings.set('alpha_percentage', config.alpha_per_current)
                config.alpha_per_current_saved = config.alpha_per_current
            sublime.save_settings('glassit.sublime-settings')

def plugin_loaded():
    settings = sublime.load_settings('glassit.sublime-settings')

    global config

    class config:
        def load(self):
            if (sublime.platform() == "windows"):
                config.settings = settings
                config.enabled = bool(settings.get('enabled', True))
                config.enabled_saved = config.enabled
                config.alpha_per_default = int(settings.get('alpha_percentage_default', 90))
                config.alpha_per_current = int(settings.get('alpha_percentage', config.alpha_per_default))
                config.alpha_per_current_saved = config.alpha_per_current
                config.alpha_step = int(settings.get('alpha_step', 5))
                config.alpha_max = 255
                config.app_name = settings.get('application', "SetTransparency.exe")
                config.app_path_alt  = settings.get('application_path_alt', "")
                config.st_title = settings.get('st_title', "Sublime Text")
                config.delay = 5000

                config.alpha_current = config.alpha_max * config.alpha_per_current / 100

                if sys.version_info[0] == 2:
                    # ST2 load plugin within main process
                    config.st_pid = os.getpid()
                else:
                    # ST3 load plugin in the child process "plugin_host.exe"
                    config.st_pid = os.getppid()
            else:
                print("Set transparency doesn't support this platform yet!")

        def reload(self):
            self.load()
            if (sublime.platform() == "windows"):
                update_window_transparency_nt()

    config = config()
    config.load()

    if (sublime.platform() == "windows"):
        # Delay set transparency until main window is created.
        sublime.set_timeout(update_window_transparency_nt, config.delay)
    else:
        print("Set transparency doesn't support this platform yet!")

    settings.add_on_change('reload', lambda:config.reload())

if sys.version_info[0] == 2:
    plugin_loaded()

class ToggleTransparencyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        config.enabled = not config.enabled
        update_window_transparency_nt()

    def is_checked(self, **args):
        return config.enabled

class ResetTransparencyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if(config.enabled == True):
            config.alpha_per_current = config.alpha_per_default
            config.alpha_current = config.alpha_max * config.alpha_per_current / 100
            update_window_transparency_nt()

class IncreaseTransparencyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if(config.enabled == True):
            config.alpha_per_current = config.alpha_per_current - config.alpha_step
            if(config.alpha_per_current < 0):
                config.alpha_per_current = 0
            config.alpha_current = config.alpha_max * config.alpha_per_current / 100
            update_window_transparency_nt()

class DecreaseTransparencyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if(config.enabled == True):
            config.alpha_per_current = config.alpha_per_current + config.alpha_step
            if(config.alpha_per_current > 100):
                config.alpha_per_current = 100
            config.alpha_current = config.alpha_max * config.alpha_per_current / 100
            update_window_transparency_nt()
