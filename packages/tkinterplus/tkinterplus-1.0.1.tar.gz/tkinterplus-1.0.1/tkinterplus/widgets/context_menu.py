from tkinter import INSERT, SEL_FIRST, SEL_LAST, SEL, END, Text, Menu, Tk
from _tkinter import TclError
from enum import Enum

class ContextMenu(Menu):
    REDO='redo'
    UNDO='undo'
    CUT='cut'
    COPY='copy'
    PASTE='paste'
    DELETE='delete'
    SELECT_ALL='select_all'
    def __init__(self,master: Tk,showcommand=None):
        """Make a right click context menu."""
        self.master=master
        Menu.__init__(self,master, tearoff=0)
        self.config(showcommand)

    def _mouse(self,e):
        """Internal Function"""
        if self.showcommand!=None: self.showcommand()
        try: self.tk_popup(e.x_root, e.y_root, 0)
        finally: self.grab_release()

    def config(self,showcommand=None,state=None):
        """Config the context menu"""
        if showcommand!=None: self.showcommand = showcommand

        # Disable menu if master is disabled.
        try:
            st = self.master['state']
            if st=='normal':
                self.enable()
            elif st=='disabled' or st=='readonly':
                self.disable()

        except: self.enable()

    def _app(self,e):
        """Internal Function"""
        try: self.tk_popup(0,0, 0)
        finally: self.grab_release()

    def disable(self):
        """Unbind context menu so it will not show"""
        self.master.unbind("<Button-3>")
        self.master.unbind('<App>')
    
    def enable(self):
        """Bind the context menu so it will show"""
        self.master.bind("<Button-3>", self._mouse)
        self.master.bind('<App>', self._app)
    
    #NOTE Disable btn if selected widget is not a `Text` widget.
    # def add_command(self,cnf:dict=None, accelerator:str=None, activebackground=None, activeforeground=None, background=None, bitmap=None, columnbreak:int=None, command=None, compound=None, font=None, foreground=None, hidemargin:bool=None, image=None, label:str=None, state=None, underline:int=None, **kw):

    def add_command(self,cnf={},**kw):
        """
        Add command menu item. add type for a built-in command ie. type=ContextMenuType.COPY
        
        Arguments
        ---
        label, command, type
        """
        # self.winfo_atomname()
        def cut():
            copy()
            delete()

        def copy():
            try:
                focus = self.focus_get()
                if focus.winfo_class() == 'Text':
                    focus.clipboard_clear()
                    focus.clipboard_append(focus.selection_get())
                    return True
                else:
                    return False
            except TclError:
                return False

        def paste():
            delete()
            focus = self.focus_get()
            focus.insert(focus.index(INSERT), focus.clipboard_get())
            return True

        def delete():
            focus = self.focus_get()
            try:
                first =focus.index(SEL_FIRST)
                last=focus.index(SEL_LAST)
                focus.delete(first,last)
                return True
            except TclError:
                return False

        def select_all():
            focus = self.focus_get()
            focus.tag_add(SEL, "1.0", END)
            focus.mark_set(INSERT, "1.0")
            focus.see(INSERT)
            return True

        def undo():
            try:
                focus:Text = self.focus_get()
                focus.edit_undo()
                return True
            except AttributeError:
                return False
        
        def redo():
            try:
                focus:Text = self.focus_get()
                focus.edit_redo()
                return True
            except TclError:
                return False
            except AttributeError:
                return False

        def run_command(name):
            focus = self.focus_get()
            if focus.winfo_class() == 'Text':
                print('WORKED: ',name)

        # Apply commands to type
        try:
            type = kw['type']
            kw['command'] = lambda: run_command(type)
            del kw['type']
        except: pass

        self.add('command', cnf or kw)

class ContextMenuType(Enum):
    """"ContextMenuType deprived! use `ContextMenu.<type>` instead"""
    REDO=staticmethod('redo')
    UNDO=staticmethod('undo')
    CUT=staticmethod('cut')
    COPY=staticmethod('copy')
    PASTE=staticmethod('paste')
    DELETE=staticmethod('delete')
    SELECT_ALL=staticmethod('select_all')
