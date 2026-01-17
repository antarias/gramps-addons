# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2026 Antonio Arias
#

# -------------------------------------------------------------------------
#
# Gtk modules
#
# -------------------------------------------------------------------------
from gi.repository import Gtk

# -------------------------------------------------------------------------
#
# Gramps modules
#
# -------------------------------------------------------------------------
from gramps.gui.editors import EditPerson
from gramps.gui.listmodel import ListModel, NOSORT
from gramps.gen.plug import Gramplet
from gramps.gen.plug.report.utils import find_spouse
from gramps.gen.display.name import displayer as name_displayer
from gramps.gen.utils.db import get_birth_or_fallback, get_death_or_fallback
from gramps.gen.datehandler import get_date
from gramps.gen.display.place import displayer as place_displayer
from gramps.gen.errors import WindowActiveError
from gramps.gen.const import GRAMPS_LOCALE as glocale
from gramps.gui.widgets.persistenttreeview import PersistentTreeView

_ = glocale.translation.gettext


class FSConnectPerson(Gramplet):

    def init(self):
        self.gui.WIDGET = self.build_gui()
        self.gui.get_container_widget().remove(self.gui.textview)
        self.gui.get_container_widget().add(self.gui.WIDGET)
        self.gui.WIDGET.show()

    def build_gui(self):
        """
        Build the GUI interface.
        """
        tip = _("Double-click on a row to edit the selected child.")
        self.set_tooltip(tip)
        top = PersistentTreeView(self.uistate, __name__)
        titles = [
            (
                "",
                NOSORT,
                50,
            ),
            (_("Property"), 1, 100),
            (_("Date"), 2, 100),
            (_("Gramps Value"), 3, 250),
            (_("FS Date"), 4, 100),
            (_("FS Value"), 5, 250),
        ]
        self.model = ListModel(top, titles)
        return top

    def main(self):
        active_handle = self.get_active("Person")
        self.model.clear()
        if active_handle:
            self.display_person(active_handle)
        else:
            self.set_has_data(False)    


    def display_person(self, active_handle):
        """
        Display the children of the active person.
        """
        active_person = self.dbstate.db.get_person_from_handle(active_handle)
        # for family_handle in active_person.get_family_handle_list():
        #     family = self.dbstate.db.get_family_from_handle(family_handle)
        #     self.display_family(family, active_person)
        self.set_has_data(self.model.count > 0)            