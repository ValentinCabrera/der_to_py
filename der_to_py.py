import json

class Entidad():
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.nombre = kwargs.get("nombre")
        self.atributos = kwargs.get("atributos", {})
        self.relaciones = kwargs.get("relaciones", {})

    def get_django_atributo(self, atributo):
        tipo = ""
        pk = None

        try:
            pk = atributo["primaryKey"]

        except: 
            pass
        

        if atributo["tipo"] == "INTEGER":
            tipo = "IntegerField"

        elif atributo["tipo"] == "BIGINT":
            tipo = "BigIntegerField"

        elif atributo["tipo"] == "SMALLINT":
            tipo = "SmallIntegerField"

        elif atributo["tipo"] == "MAIL":
            tipo = "EmailField"

        elif atributo["tipo"] == "TEXT":
            tipo = "TextField"

        elif atributo["tipo"] == "BOOLEAN":
            tipo = "BooleanField"

        elif atributo["tipo"] == "DATE":
            tipo = "DateField"

        elif atributo["tipo"] == "TIME":
            tipo = "TimeField"

        elif atributo["tipo"] == "DATETIME":
            tipo = "DateTimeField"

        if pk:
            tipo += "(primary_key=True)"

        else:
            tipo += "()"

        if atributo["tipo"] == "VARCHAR":
            tipo = "CharField("

            if pk:
                tipo += "primary_key=True, "

            tipo += "max_length=30)"

        code = f"    {atributo['nombre']} = models.{tipo}"

        return code

    def get_django_atributos(self):
        code = ""

        for i in self.atributos:
            code += '\n' + self.get_django_atributo(i) 

        return code
    
    def get_modelo(self, destino):
        for i in entidades:
            if i.id == destino:
                return i.nombre
    
    def get_django_relacion(self, relacion):
        modelo = self.get_modelo(relacion["destino"])
        atributo = modelo[0].lower() + modelo[1:]
        

        code = f"    {atributo} = models.ForeignKey({modelo}, on_delete=models.RESTRICT)"

        return code
    
    def get_django_relaciones(self):
        code = ""

        for i in self.relaciones:
            code += '\n' + self.get_django_relacion(i)

        return code
    
    def get_django_str(self):
        return self.atributos[0]["nombre"]

    def get_django_model(self):
        code = f"""class {self.nombre}(models.Model):
{self.get_django_atributos()}
{self.get_django_relaciones()}

    def __str__(self):
        return str(self.{self.get_django_str()})
"""

        return code
    
    def get_relaciones(self):
        relaciones = []

        for i in self.relaciones:
            relaciones.append(i["destino"])

        return relaciones

file_name = "ModeloER.mdj"
f = open(file_name, 'r')

dic = json.load(f)

datos = {}

for i in dic["ownedElements"]:
    if i["_type"] == "ERDDataModel":
        datos = i
        break

datos = datos ["ownedElements"]

der = datos[0]["ownedViews"]
entidades_totales = datos[1:]

modelos = []

for i in der:
    modelos.append(i["model"]['$ref'])

def get_entidad(dic):
    entidad = {"id":dic["_id"], "nombre":dic["name"]}

    try:
        dato = dic["columns"]
        atributos = []

        for i in dato:
            try:
                atributo = {"nombre":i["name"], "tipo":i["type"]}

                try:
                    atributo["primaryKey"] = i["primaryKey"]

                except:
                    pass

                try:
                    i["foreignKey"]

                except:
                    atributos.append(atributo)

            except:
                pass
        
        else:
            entidad["atributos"] = atributos
        
    except:
        pass

    try:
        dato = dic["ownedElements"]
        relaciones = []

        for i in dato:
            if i["_id"] in modelos:
                destino = i["end2"]["reference"]["$ref"]
                cardinalidad = "1..1"

                try:
                    cardinalidad = i["end2"]["cardinality"]

                except:
                    pass

                relaciones.append({"destino":destino, "cardinalidad":cardinalidad})

        else:
            if relaciones != []:
                entidad["relaciones"] = relaciones

    except:
        pass

    return entidad

entidades = []

for i in entidades_totales:
    if i["_id"] in modelos:
        entidades.append(Entidad(**get_entidad(i)))

def verificar_orden(entidades):
    for i in range(len(entidades)):
        for k in entidades[i:]:
            if k.id in entidades[i].get_relaciones():
                return False
            
    return True


def ordenamiento_topologico(desordenadas):

    ordenadas = []

    for i in desordenadas:
        if i.relaciones == {}:
            ordenadas.append(i)
            desordenadas.remove(i)

    dependientes = []


    for i in desordenadas:
        for j in dependientes:
            if i.id in j.get_relaciones():
                posicion = dependientes.index(j)
                dependientes = dependientes[:posicion] + [i] + dependientes[posicion:] 

                break
        else:
            dependientes.append(i)

    ordenadas = ordenadas + dependientes


    if not verificar_orden(ordenadas):
        return ordenamiento_topologico(ordenadas)

    return ordenadas

entidades = ordenamiento_topologico(entidades)


models_file = "from django.db import models \n\n"

for i in entidades:
    models_file += i.get_django_model() + '\n\n'


with open("models.py", "w") as f:
    f.write(models_file)