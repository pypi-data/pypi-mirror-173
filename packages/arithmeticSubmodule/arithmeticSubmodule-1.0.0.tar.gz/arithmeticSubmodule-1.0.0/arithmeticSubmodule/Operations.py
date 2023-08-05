class Operations:

    def __init__(self, list_1, list_2):
        self.list_1 = list_1
        self.list_2 = list_2

    def private_check_lists(self):
        
        isList1ItemsCorrect = [el1 for el1 in self.list_1 if (isinstance(el1, float) or isinstance(el1, int))]
        
        #Si alguno de los elementos de v1 no tiene el formato correcto la longitud de isList1ItemsCorrect no será la misma que la de data["v1"]
        if (len(isList1ItemsCorrect) != len(self.list_1)):
            raise ValueError("El formato de alguno de los elementos de v1 no es correcto")
        
        isList2ItemsCorrect = [el1 for el1 in self.list_2 if (isinstance(el1, float) or isinstance(el1, int))]    
        
        #Si alguno de los elementos de v2 no tiene el formato correcto la longitud de isList2ItemsCorrect no será la misma que la de data["v2"]
        if(len(isList2ItemsCorrect) != len(self.list_2)):
            raise ValueError("El formato de alguno de los elementos de v2 no es correcto")

    def public_sum(self):

        #Se comprueban si los elementos de ambas listas tienen el formato correcto. Si no lo tienen no se continua ejecutando y se lanza un ValueError
        self.private_check_lists()
        return  [round(el1+el2,3) for el1, el2 in zip(self.list_1, self.list_2)]

    def public_rest(self):

        #Se comprueban si los elementos de ambas listas tienen el formato correcto. Si no lo tienen no se continua ejecutando y se lanza un ValueError 
        self.private_check_lists()
        return  [round(el1-el2,3) for el1, el2 in zip(self.list_1, self.list_2)]

    def public_mult(self):

        #Se comprueban si los elementos de ambas listas tienen el formato correcto. Si no lo tienen no se continua ejecutando y se lanza un ValueError 
        self.private_check_lists()
        return [round(el1*el2,3) for el1, el2 in zip(self.list_1, self.list_2)]

    def public_div(self):
        
        #Se comprueban si los elementos de ambas listas tienen el formato correcto. Si no lo tienen no se continua ejecutando y se lanza un ValueError
        self.private_check_lists()

        #Si alguno de los elementos de list_2 es 0 sería una división por 0, se lanza un ValueError y no se ejecuta la operación de división
        isList2ItemsCero = [el1 for el1 in self.list_2 if (el1 != 0)]
        if(len(isList2ItemsCero) != len(self.list_2)):
           raise ValueError("Alguno de los elementos divisores de v2 es 0")

        return [round(el1/el2,3) for el1, el2 in zip(self.list_1, self.list_2)]
 
