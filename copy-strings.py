import ida_kernwin
from PyQt5.Qt import QApplication


class copy_only_string(ida_kernwin.action_handler_t):
    ACTION_NAME = "copy only string"
    ACTION_LABEL = "Copy only string(s)"
    ACTION_SHORTCUT = "Ctrl+C"

    def __init__(self):
        ida_kernwin.action_handler_t.__init__(self)

    def activate(self, ctx):
        data = []
        for idx in ctx.chooser_selection:
            _, _, _, s = ida_kernwin.get_chooser_data(ctx.widget_title, idx)
            data.append(s)
        QApplication.clipboard().setText(", ".join(data))
        return 0

    def update(self, ctx):
        if ctx.widget_type == ida_kernwin.BWN_STRINGS:
            return ida_kernwin.AST_ENABLE_FOR_WIDGET
        return ida_kernwin.AST_DISABLE_FOR_WIDGET


class print_string(ida_kernwin.action_handler_t):
    ACTION_NAME = "print_string"
    ACTION_LABEL = "Print string(s)"
    ACTION_SHORTCUT = "Ctrl+P"

    def __init__(self):
        ida_kernwin.action_handler_t.__init__(self)

    def activate(self, ctx):
        for idx in ctx.chooser_selection:
            addr, _, _, s = ida_kernwin.get_chooser_data(ctx.widget_title, idx)
            print("%s: '%s'" % (addr, s))
        return 0

    def update(self, ctx):
        if ctx.widget_type == ida_kernwin.BWN_STRINGS:
            return ida_kernwin.AST_ENABLE_FOR_WIDGET
        return ida_kernwin.AST_DISABLE_FOR_WIDGET


klasses = [copy_only_string, print_string]

sw = ida_kernwin.find_widget("Strings window")
if not sw:
    sw = ida_kernwin.open_strings_window(ida_idaapi.BADADDR)

for klass in klasses:
    ida_kernwin.unregister_action(klass.ACTION_NAME)

    if ida_kernwin.register_action(
        ida_kernwin.action_desc_t(
            klass.ACTION_NAME, klass.ACTION_LABEL, klass(), klass.ACTION_SHORTCUT
        )
    ):
        if sw:
            ida_kernwin.attach_action_to_popup(sw, None, klass.ACTION_NAME)
            print(
                "Permanently added '%s' action to 'String window's popup"
                % klass.ACTION_LABEL
            )
