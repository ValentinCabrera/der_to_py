from django.db import models 

class Jugador(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)


    def __str__(self):
        return str(self.id)


class Equipo(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.()
    abreviatura = models.CharField(max_length=30)

    jugador = models.ForeignKey(Jugador, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Estado(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)

    jugador = models.ForeignKey(Jugador, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


class Posicion(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)

    jugador = models.ForeignKey(Jugador, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id)


