import npyscreen, subprocess, threading, shlex

RUNSERVER = """
library(plumber)
server <- plumb("server.R")
server$run(port=8000)
"""


class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        # When Application starts, set up the Forms that will be used.
        # These two forms are persistent between each edit.
        self.addForm("MAIN", Output, name="R_Server", color="SAFE", command="ping google.com")
        self.addForm("webserver", Output, name="WebServer", color="SAFE", command="")
        
    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")
    
    def change_form(self, name):
        # Switch forms.  NB. Do *not* call the .edit() method directly (which 
        # would lead to a memory leak and ultimately a recursion error).
        # Instead, use the method .switchForm to change forms.
        self.switchForm(name)
        
        # By default the application keeps track of every form visited.
        # There's no harm in this, but we don't need it so:        
        self.resetHistory()


class Output(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = npyscreen.BufferPager
    
    def __init__(self, *args, **kwargs):
        super(Output, self).__init__(*args, **kwargs)
        self.command = kwargs["command"]
        self.thread = threading.Thread(target=self.run_command, args=())
        self.kill = threading.Event()

    def beforeEditing(self):
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.on_exit
        self.add_handlers({
            "^T": self.change_forms,
            "^Q": self.on_exit
        })
        self.wStatus1.value = self.name
        self.wMain.editable = False
        self.wMain.autowrap = False
        self.wMain.buffer(["Connecting..."])
        self.thread.start()
        self.edit()

    def run_command(self):
        proc = subprocess.Popen(shlex.split(self.command), stdout=subprocess.PIPE)
        while proc.poll() is None and not self.kill.is_set():
            line = proc.stdout.readline()
            if line != "":
                self.on_output(line)
        proc.kill()

    def on_output(self, line):
        self.wMain.buffer([line.decode("ascii")])
        self.display()

    def on_exit(self, _input):
        self.kill.set()
        self.parentApp.switchForm(None)

    def change_forms(self, _input):
        change_to = ""
        if self.name == "R_Server":
            change_to = "webserver"
        elif self.name == "WebServer":
            change_to = "MAIN"

        self.parentApp.change_form(change_to)


def main():
    ta = MyTestApp()
    ta.run()


if __name__ == '__main__':
    main()
