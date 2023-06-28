def split_str(files: list, position: int) -> list:
        """
        Toma la dirección de proporcionada y devuelve solo el nombre y la extención del archivo

        files: Lista de direcciones de los archivos.
        position: Numero de posicion del input asociado.

        """
        bubble = []
        for i in range(len(files[0])):
            x = files[0][i].split('/')
            bubble.append(x[position]) 
        return bubble
        