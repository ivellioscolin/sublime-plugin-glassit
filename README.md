## GlassIt v 1.4.0 <br/>

### NOTES
- With this plugin, you can change the window transparency by key pressing or mouse whell scroll.
- Works for both sublime 2, 3 & 4.
- Only works on Windows later than Windows XP.

### INSTALLATION
1. Get "SetTransparency.exe" from below link or compile by yourself.
https://github.com/ivellioscolin/settransparency/tree/master/binary
2. Put "SetTransparency.exe" into ST main path, or the location specified in settings "application_path_alt".
3. Search and install "GlassIt" via "Package Control". You may also download the archive and extract to "{sublime}\Data\Packages\GlassIt".

### USAGE
1. ST main window will be set as transparent after the plugin loaded.
2. To adjust the transparency behavior:
    - Increase/Decrease:
      - Via mouse wheel: alt + mouse wheel up/down
      - Via keyboard: ctrl + alt + z/c
      - Via command palette.
    - Reset to default:
      - Via keyboard: ctrl + alt + x
      - Via command palette.
    - Toggle on/off:
      - "Tools"->"Packages"->"Glass It".
      - Via command palette.
    - Modify "Glass It" user settings.
      - "enabled": Control whether Glass It is enabled or not.
      - "alpha_percentage": The alpha percentage if "Glass It" is enabled.
      - "application_path_alt": Location where SetTransparency.exe sits, other than ST main path.

### LINK
https://github.com/ivellioscolin/sublime-plugin-glassit.git

### HISTORY
- 1.4.0  
Add "application_path_alt" to allow "SetTransparency.exe" put in location other than ST main path.  
Now support ST4.
- 1.3.0  
Save user-made changes into user settings.
- 1.2.0  
Fix path search issue when main program and packages are installed into different locations.
- 1.1.0  
Fix path search issue, use absolute path instead. Add setting to change adjustment step.
- 1.0.0  
Initial version