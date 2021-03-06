"""basicformatter module

Classes:
    Formatter: Class for formatting text in a text file.
    Line: Class for building the next formatted line.
    FormatSettings: Class for keeping track of the format settings.
"""
import fileinput

class Formatter():
    """This is a class for formatting text in a .txt file.

    Attributes:
        No public attributes.
    """    
    
    def __init__(self, filename):
        """The constructor for Formatter class.

        Args:
            filename (str): The file name of a .txt file.
        """
        self._file = self._openfile(filename)
        self._settings = FormatSettings()
        self._formattedlines = []    
        self._currentline = Line(self._settings) 

    def format(self):
        """Return the formatted text.
       
        Args:
            No arguments.

        Returns:
            _formattedlines (list[str]): Formatted lines of text.
        """
        for line in self._file:
            if line.startswith("."):
                self._settings.updatesettings(line.split())
            else:
                self._processline(line)
        if self._settings.formatting and not self._currentline.isempty():
            self._endline()
        return self._formattedlines
    
    def _processline(self, line):
        """Check if line needs formatting."""
        if self._settings.formatting:
            self._formatline(line)
        else:
            self._formattedlines.append(line)
  
    def _formatline(self, line):
        """Format the line with appropriate width, spacing, and margin."""
        line = line.split()

        if not line:
            #Format when line is empty
            if not self._currentline.isempty():
                self._endline()
                self._addlinespacing()
            self._endline()
            self._addlinespacing()
        else:
            #Format line as normal
            for word in line:
                if not self._currentline.hasspacefor(word):    
                    self._endline()    
                    self._addlinespacing()
                if self._currentline.isempty():
                    self._currentline.addmargin()
                self._currentline.addword(word)
 
    def _endline(self):
        """Add current formatted line to list of formatted lines."""
        self._formattedlines.append(self._currentline.getline()+'\n')
        self._currentline.reset()

    def _addlinespacing(self):
        """Add empty lines to list of formatted lines."""
        for i in range(self._settings.linespacing):
            self._formattedlines.append('\n')
          
    def _openfile(self, filename):
        """Opens file.
        
        Args:
            filename (str): The file name of file to be formatted.

        Returns:
            Instance of FileInput class
        """

        try:
            return fileinput.input(filename)
        except FileNotFoundError:
            print(filename, "not found. Please input an existing file.")
        except PermissionError:
            print("Permission denied.")
            print("please change permissions of", self.filename,
                "or input a file with proper permissions.")

class Line():
    """This is a class for building the next formatted line.

    Attributes:
        No public attributes.
    """

    def __init__(self, settings):
        """The constructor for Line class.

        Args:
            settings (FormatSettings): The format settings.
        """
        self._settings = settings
        self._settings.bindto(self.updatespaceleft)
        self._line = []
        self._spaceleft = self._settings.linewidth

    def getline(self):
        """Return current line.
        
        Returns:
            String of all words in line joined by spaces.
        """
        return " ".join(self._line)

    def isempty(self):
        """Check if line is empty.
        
        Returns:
            True if line is empty, False otherwise.
        """
        return len(self._line) == 0
    
    def reset(self):
        """Empty line and reset space left in line."""
        self._line.clear()
        self._spaceleft = self._settings.linewidth

    def addmargin(self):
        """Add a margin to the line."""
        for i in range(self._settings.linemargin):
            self._line.append("")
            self._spaceleft -= 1

    def addword(self, word):
        """Add the word to the end of line.

        Args:
            word (str): A word to add to the line.
        """
        self._line.append(word)
        self._spaceleft -= len(word)+1 #+1 for space

    def hasspacefor(self, word):
        """Check if there is enough room for word in line.

        Args:
            word (str): Next word to add to the line.
        
        Returns:
            True if enough space, False otherwise.
        """
        return len(word) <= self._spaceleft

    def updatespaceleft(self):
        """Update spaceleft to current linewidth setting."""
        self._spaceleft = self._settings.linewidth


class FormatSettings():
    """This is a class for keeping track of the formatting settings.

    Attributes:
        No public attributes.
    """

    def __init__(self):
        """The constructor for FormatSettings."""
        self._settings = {'FT': 0, 'LW': 132, 'LS': 0, 'LM': 0}
        self._observers = []

    def updatesettings(self, bufferline):
        """Updates settings to the value given in the command.

        Args:
            bufferline (list[str]): A line with command.
        """
        command = bufferline[0]
        value = bufferline[1]
        if command == ".FT":
            self.formatting = value
        elif command == ".LW":
            self.linewidth = value
        elif command == ".LS":
            self.linespacing = value
        elif command == ".LM":
            self.linemargin = value
    
    @property
    def formatting(self):
        """Setting for if formatting is on or off."""
        return self._settings['FT'] 
    
    @property
    def linewidth(self):
        """Setting of line width.
        
        Setter:
            Updates spaceleft in class Line to line width using observers
            callback.
        """
        return self._settings['LW'] 

    @property
    def linespacing(self):
        """Setting for linespacing."""
        return self._settings['LS']

    @property
    def linemargin(self):
        """Setting for line margin.
        
        Setter:
            Max margin is line width - 20.
            Min margin is 0.
        """
        return self._settings['LM'] 
    
    @formatting.setter
    def formatting(self, value):
        if value == "off":
            self._settings['FT'] = 0
        elif value == "on":
            self._settings['FT'] = 1

    @linewidth.setter
    def linewidth(self, value):
        self._settings['LW'] = int(value)
        for callback in self._observers:
            callback()
        self.formatting = "on"
        
    @linespacing.setter
    def linespacing(self, value):
        self._settings['LS'] = int(value)

    @linemargin.setter
    def linemargin(self, value):
        if '+' in value or '-' in value:
            self._settings['LM'] += int(value)
        else:
            self._settings['LM']= int(value)

        maxmargin = self._settings['LW'] - 20
        if self._settings['LM'] < 0:
            self._settings['LM'] = 0
        elif self._settings['LM'] > maxmargin:
            self._settings['LM'] = maxmargin

    def bindto(self, callback):
        """Add callback method to observers list.
        
        Args:
            callback (method): Method to be called after some event.
        """
        self._observers.append(callback)

