

#CONSTANTES DEL PRIMER MODELO 

modelo1_masa_activa= {
    "Molecular Mass of active ion": "g/mol",
    "Active material density": "g/m3",
    "Mass of Active Material": "m^2/g",
    "Potencial steps": "int",
    "Number of electrons": "int",
    "Electric doblue layer capacitance (Trassati)": "int",
    "Reference electrode" : "str",
}

modelo1_area_activa = {
    "Molecular Mass of active ion": "g/mol",
    "Active material density": "g/m3",
    "Geometrical superficial area": "m^2/g",
    "Potencial steps": "int",
    "Number of electrons": "int",
    "Electric doblue layer capacitance (Trassati)": "int",
    "Reference electrode" : "str",
}


modelo1_area_activa_respuestas = {
    "pesomol": "0",
    "densidad": "0",
    "areasup": "0",
    "ventana": "0",
    "DLC": "0",
    "electrones": "0",
    "referencia": "--",
    "velocidades": []
}

modelo1_masa_activa_respuestas= {
    "pesomol": "0",
    "densidad": "0",
    "masalec": "0",
    "ventana": "0",
    "electrones": "0",
    "DLC": "0",
    "referencia": "--",
    "velocidades": []
}

modelos = {
    'MASA_ACTIVA': 'Masa Activa',
    'AREA_ACTIVA': 'Area Activa'
}

FONT_SIZES_PLOTS = {
    'title': 18,
    'subtitle': 15,
    'label': 15,
    'legend': 15,
    'ticks': 13,
    'annotation': 15,
    'annotation_title': 15,
    'annotation_subtitle': 15,
    'annotation_label': 15,
    'annotation_legend': 15,
    'annotation_ticks': 15,
    'annotation_annotation': 15,
}