from django.db import models 

class Localidad(models.Model):

    nombre = models.CharField(primary_key=True, max_length=30)


    def __str__(self):
        return str(self.nombre)


class Direccion(models.Model):

    id = models.SmallIntegerField(primary_key=True)
    calle = models.CharField(max_length=30)
    numero = models.SmallIntegerField()

    localidad = models.ForeignKey(Localidad, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class User(models.Model):

    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)


    def __str__(self):
        return str(self.id)


class Administrador(models.Model):

    mail = models.EmailField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.mail)


class Mapa(models.Model):

    id = models.IntegerField(primary_key=True)
    color = models.SmallIntegerField()


    def __str__(self):
        return str(self.id)


class Salon(models.Model):

    id = models.IntegerField(primary_key=True)
    lugares = models.SmallIntegerField()

    mapa = models.ForeignKey(Mapa, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Negocio(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()

    direccion = models.ForeignKey(Direccion, on_delete=models.RESTRICT)
    administrador = models.ForeignKey(Administrador, on_delete=models.RESTRICT)
    salon = models.ForeignKey(Salon, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Token(models.Model):

    key = models.CharField(primary_key=True, max_length=30)
    activa = models.BooleanField()

    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.key)


class Fecha(models.Model):

    id = models.BigIntegerField(primary_key=True)
    dia = models.DateTimeField()

    negocio = models.ForeignKey(Negocio, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class EstadoReserva(models.Model):

    nombre = models.CharField(primary_key=True, max_length=30)

    fecha = models.ForeignKey(Fecha, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.nombre)


class Cliente(models.Model):

    telefono = models.BigIntegerField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.telefono)


class Reserva(models.Model):

    id = models.BigIntegerField(primary_key=True)

    fecha = models.ForeignKey(Fecha, on_delete=models.RESTRICT)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class CambioEstadoReserva(models.Model):

    id = models.IntegerField(primary_key=True)
    fechaHora = models.DateTimeField()

    estadoReserva = models.ForeignKey(EstadoReserva, on_delete=models.RESTRICT)
    reserva = models.ForeignKey(Reserva, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Horarios(models.Model):

    id = models.IntegerField(primary_key=True)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    horarioReserva = models.TimeField()
    horarioCierre = models.TimeField()


    def __str__(self):
        return str(self.id)


class TipoDia(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)

    estadoReserva = models.ForeignKey(EstadoReserva, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class DetalleFecha(models.Model):

    id = models.BigIntegerField(primary_key=True)

    horarios = models.ForeignKey(Horarios, on_delete=models.RESTRICT)
    fecha = models.ForeignKey(Fecha, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class DetalleDia(models.Model):

    id = models.IntegerField(primary_key=True)

    horarios = models.ForeignKey(Horarios, on_delete=models.RESTRICT)
    tipoDia = models.ForeignKey(TipoDia, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class CambioEstadoCliente(models.Model):

    id = models.IntegerField(primary_key=True)
    fechaHora = models.DateTimeField()

    estadoReserva = models.ForeignKey(EstadoReserva, on_delete=models.RESTRICT)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Sector(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    prioridad = models.SmallIntegerField()

    salon = models.ForeignKey(Salon, on_delete=models.RESTRICT)
    mapa = models.ForeignKey(Mapa, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class TipoMesa(models.Model):

    nombre = models.CharField(primary_key=True, max_length=30)


    def __str__(self):
        return str(self.nombre)


class Mesa(models.Model):

    id = models.IntegerField(primary_key=True)
    lugares = models.SmallIntegerField()

    sector = models.ForeignKey(Sector, on_delete=models.RESTRICT)
    tipoMesa = models.ForeignKey(TipoMesa, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Linea(models.Model):

    id = models.BigIntegerField(primary_key=True)
    x1 = models.SmallIntegerField()
    x2 = models.SmallIntegerField()
    y1 = models.SmallIntegerField()
    y2 = models.SmallIntegerField()

    mapa = models.ForeignKey(Mapa, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class EstadoCarta(models.Model):

    nombre = models.CharField(primary_key=True, max_length=30)


    def __str__(self):
        return str(self.nombre)


class Carta(models.Model):

    id = models.IntegerField(primary_key=True)
    estado = models.CharField(max_length=30)
    fecha = models.TimeField()
    negocio = models.IntegerField()

    negocio = models.ForeignKey(Negocio, on_delete=models.RESTRICT)
    estadoCarta = models.ForeignKey(EstadoCarta, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Categoria(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)

    estadoCarta = models.ForeignKey(EstadoCarta, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Producto(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=30)

    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    estadoCarta = models.ForeignKey(EstadoCarta, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Item(models.Model):

    id = models.IntegerField(primary_key=True)
    precio = models.SmallIntegerField()

    carta = models.ForeignKey(Carta, on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


