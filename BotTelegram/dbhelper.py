import pyodbc
import re
import telebot
from telebot import types

class DBHelper:

    def getLogins(self):

        server = ''
        database = ''
        username = ''
        password = ''
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()
        
        
        storedProc = "Exec [dbo].[TB_ListarLoginsAtivos]"
    
        # Execute Stored Procedure With Parameters
        cursor.execute( storedProc )

        rows = cursor.fetchall()
        return rows

    def getInstancia(self):

        server = ''
        database = ''
        username = ''
        password = ''
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()
        
        
        storedProc = "Exec [dbo].[TB_ListarInstancias]"
    
        # Execute Stored Procedure With Parameters
        cursor.execute( storedProc )

        rows = cursor.fetchall()
        
        return rows

    def getLoginsComDefeito(self):

        server = ''
        database = ''
        username = ''
        password = ''
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()
        
        
        storedProc = "Exec [dbo].[TB_ListarLoginsDefeituosos]"
    
        # Execute Stored Procedure With Parameters
        cursor.execute( storedProc )

        rows = cursor.fetchall()
        return rows

    def getAutenticador(self, idAutenticador):

        server = ''
        database = ''
        username = ''
        password = ''
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()
        
        
        storedProc = "SELECT * FROM TBAcesso where ativo = 1 and idTelegram = ?"
        params = (idAutenticador)
        # Execute Stored Procedure With Parameters
        cursor.execute( storedProc, params )
        

        rows = cursor.fetchall()
        print(rows)
        if rows:
            #print(rows)
            return True
        else:
            return False
            #print("Deu Ruim")


    def getProcesso(self):

        server = ''
        database = ''
        username = ''
        password = ''
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()

        #cursor.execute('SELECT * FROM Processo where processo = {} and ativo = {}')
        cursor.execute('SELECT id, nome, ativo, rodando FROM processo where ativo = 1')
        rows = cursor.fetchall()
        return rows
    
    def getRegistroCliente (self,processo):

        server = ''
        database = ''
        username = ''
        password = ''
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()

        storedProc = "Exec [dbo].[TB_ListarRegistroInstancia] @idProcesso = ?"
        params = (processo)
    
        # Execute Stored Procedure With Parameters
        cursor.execute( storedProc, params )

        row = cursor.fetchone()
        if row:
            string = ("Processados: " + str(row[1]) + " Erros: " + str(row[2]) + " Porcentagem: " +str(row[0]))
            return string
        else:
            string = "Vendas não encontrada"
        return string
    
    def getBacklog(self):

        server = ''
        database = ''
        username = ''
        password = ''
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = conn.cursor()
        
        
        storedProc = "Exec [dbo].[RS_VERIFICA_BACKLOG_GERAL]"
    
        # Execute Stored Procedure With Parameters
        cursor.execute( storedProc )

        rows = cursor.fetchall()
        return rows