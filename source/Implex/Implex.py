from gramps.gen.simple import SimpleAccess, SimpleDoc
from gramps.gui.plug.quick import QuickTable
from gramps.gen.const import GRAMPS_LOCALE as glocale
_ = glocale.translation.gettext

def run(database, document, person):
    """
    Función principal del QuickReport.
    Gramps llama a esto automáticamente.
    """
    # Setup simple access functions
    sdb = SimpleAccess(database)
    sdoc = SimpleDoc(document)

    # Validation
    if not person:
        sdoc.header1("Error")
        sdoc.paragraph("No person selected.")
        return

    # Set title
    sdoc.header1(f"Implex: {person.get_primary_name().get_name()}")
    sdoc.paragraph(_("Quick analysis of unique vs. known ancestors."))
    sdoc.paragraph("")

    # Create results table
    stab = QuickTable(sdb)
    stab.columns("Gen", "Theoretical", "Known", "Unique", "Implex")

    # Get ancestors from initial person
    ancestros_actuales = [person.get_handle()]
    
    # Iterate for 12 gens
    for gen in range(1, 12): # Vamos hasta 11 generaciones
        siguiente_gen_handles = []
        
        # Iteramos sobre todos los ancestros de la generación actual
        # IMPORTANTE: Si 'ancestros_actuales' tiene duplicados, los procesamos varias veces.
        # Esto es necesario para detectar cruces en generaciones profundas.
        for handle in ancestros_actuales:
            p = database.get_person_from_handle(handle)
            if p:
                for fam_handle in p.get_parent_family_handle_list():
                    familia = database.get_family_from_handle(fam_handle)
                    if familia:
                        # Si existe el padre, lo añadimos (aunque ya esté en la lista)
                        if familia.get_father_handle():
                            siguiente_gen_handles.append(familia.get_father_handle())
                        # Si existe la madre, la añadimos
                        if familia.get_mother_handle():
                            siguiente_gen_handles.append(familia.get_mother_handle())

        # Si no hay nadie en la siguiente generación, paramos
        if not siguiente_gen_handles:
            break
        
        # CÁLCULOS MATEMÁTICOS
        num_teoricos = 2 ** gen
        
        # Conocidos: Cantidad total de padres encontrados (incluyendo repetidos)
        num_conocidos = len(siguiente_gen_handles)
        
        # Únicos: Eliminamos duplicados para ver cuántas personas físicas son
        num_unicos = len(set(siguiente_gen_handles))
        
        # Implexo: Solo calculamos si tenemos datos conocidos
        implexo_str = "-"
        if num_conocidos > 0:
            # Fórmula: (Total encontrados - Únicos) / Total encontrados
            implexo = (num_conocidos - num_unicos) / num_conocidos
            implexo_str = "{:.1f}%".format(implexo * 100)


        # Escribir en la tabla
        stab.row(
            f"G{gen}", 
            str(num_teoricos), 
            str(num_conocidos),
            str(num_unicos), 
            implexo_str
        )

        ancestros_actuales = siguiente_gen_handles

    stab.write(sdoc)
    sdoc.paragraph(_("\nPedigree Collapse (Implex) is calculated as (known-unique)/kwnon % of ancestors per generation."))    