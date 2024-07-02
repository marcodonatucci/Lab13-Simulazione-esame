from database.DB_connect import DBConnect
from model.state import State
from model.edges import edges


class DAO:

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT  YEAR(s.`datetime`) as year
FROM sighting s """
            cursor.execute(query)
            for row in cursor:
                result.append(row['year'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT  s.shape  as shape 
FROM sighting s
WHERE YEAR(s.`datetime`) = %s"""
            cursor.execute(query, (year,))
            for row in cursor:
                result.append(row['shape'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getStates():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT  s.*
FROM state s """
            cursor.execute(query)
            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(year, shape, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT  n.state1 as id1, n.state2 as id2, COUNT(s.id) as weight
FROM neighbor n, sighting s
WHERE (n.state1 = s.state or n.state2 = s.state) and n.state1 < n.state2 and YEAR(s.`datetime` ) = %s and s.shape = %s
GROUP BY id1, id2"""
            cursor.execute(query, (year, shape))
            for row in cursor:
                result.append(edges(idMap[row['id1']], idMap[row['id2']], row['weight']))
            cursor.close()
            cnx.close()
        return result

#     @staticmethod
#     def getWeights(year, shape, idMap):
#         cnx = DBConnect.get_connection()
#         result = []
#         if cnx is None:
#             print("Connessione fallita")
#         else:
#             cursor = cnx.cursor(dictionary=True)
#             query = """SELECT  n.state1 as id1, n.state2 as id2, COUNT(s.id) as weight
# FROM neighbor n, sighting s, sighting s2
# WHERE n.state1 = s.state and YEAR(s.`datetime` ) = %s and YEAR(s.`datetime` ) = YEAR(s2.`datetime`) and s2.state = n.state2 and s.state < s2.state and s.shape = s2.shape and s.shape = %s
# GROUP BY id1, id2
# """
#             cursor.execute(query, (year, shape))
#             for row in cursor:
#                 result.append()
#             cursor.close()
#             cnx.close()
#         return result

