# Archivo: Implex.gpr.py

register(QUICKREPORT,
    id='implex',  # ID único
    name=_("Implex Calculator"),
    description=_("Calculates Implex (Pedigree Collapse) per generation"),
    gramps_target_version='6.0', 
    version = '0.1.1',
    status=STABLE,
    fname='Implex.py',
    authors=["Antonio Arias"],
    authors_email=["antonio@arias.name"],
    category=CATEGORY_QR_PERSON,
    runfunc = 'run'
)

