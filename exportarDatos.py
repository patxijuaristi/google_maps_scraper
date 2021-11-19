# -*- coding: utf-8 -*-

import xlwt

class ExportarDatosMaps:
    
    def __init__(self, nombreFichero, ruta, listaLugares):
        self.nombreFichero = nombreFichero
        self.ruta = ruta
        self.listaLugares = listaLugares
    
    def exportarExcel(self):
        writeBook= xlwt.Workbook(encoding='utf-8')
        sheet = writeBook.add_sheet("document",cell_overwrite_ok=True)
        style = xlwt.XFStyle()

        sheet.write(0, 0, 'KEYWORD')
        sheet.write(0, 1, 'NAME')
        sheet.write(0, 2, 'CATEGORY')
        sheet.write(0, 3, 'DIRECTION')
        sheet.write(0, 4, 'PHONE')
        sheet.write(0, 5, 'WEB')
        sheet.write(0, 6, 'PLUS CODE')
        sheet.write(0, 7, 'OPEN HOURS')
        sheet.write(0, 8, 'STARS')
        sheet.write(0, 9, 'REVIEWS')

        cont=1
        for lugar in self.listaLugares:
            sheet.write(cont, 0, lugar.keyword)
            sheet.write(cont, 1, lugar.nombre)
            sheet.write(cont, 2, lugar.categoria)
            sheet.write(cont, 3, lugar.direccion)
            sheet.write(cont, 4, lugar.telefono)
            sheet.write(cont, 5, lugar.web)
            sheet.write(cont, 6, lugar.pluscode)
            sheet.write(cont, 7, lugar.horario)
            sheet.write(cont, 8, lugar.estrellas)
            sheet.write(cont, 9, lugar.resenas)
            cont = cont + 1

        writeBook.save(self.ruta+self.nombreFichero)