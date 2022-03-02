
from django.db import models

class ProductManager(models.Manager):

    def productos_por_user(self, usuario):
        return self.filter(
            user_created = usuario
        )

    def productos_con_stock(self):
        return self.filter(stok__gt = 0).order_by('-num_sales')

    def productos_por_genero(self, genero):
        #lista productos por generos
        if genero == "m":
            mujer = True
            varon = False
        elif genero == "v":
            mujer = False
            varon = True
        else:
            mujer = True
            varon = True
        return self.filter(woman = mujer, man = varon)