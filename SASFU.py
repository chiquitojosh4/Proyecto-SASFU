'''Proyecto sobre el sistema de gestion de cupos universitarios'''
'''Sustainable application system for universities'''
'''SASFU'''
from abc import ABC#impotar ABCMeta
from abc import abstractmethod#importar abstractmethod
import json
from datetime import datetime, date

class Iniciar_fase(ABC):#Interfaz Iniciar_fase
    @abstractmethod
    def iniciar(self):
        pass

class Finalizar_fase(ABC):#Interfaz Finalizar_fase
    @abstractmethod
    def finalizar(self):
        pass

class Universidad(Iniciar_fase,Finalizar_fase):#Clase Universidad que hereda de Iniciar_fase y Finalizar_fase
    Pais = "Ecuador"
    def __init__(self, nombre:str, provincia:str, canton:str, direccion:str, enlace:str,universidad:str,tipo:str):
        self.nombre = nombre
        self.provincia = provincia
        self.canton = canton
        self.direccion = direccion
        self.enlace = enlace
        self.universidad = universidad
        self.tipo = tipo
    @property
    def universidad(self):#Getter universidad
        return self._universidad
    @universidad.setter
    def universidad(self, valor:str):#Setter universidad con validacion
        valor=valor.upper()
        valores_permitidos = ["PUBLICA", "PRIVADA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad debe ser uno de los siguientes: {valores_permitidos}.")             
        self._universidad = valor
    @property
    def tipo(self):#Getter tipo
        return self._tipo
    @tipo.setter
    def tipo(self, valor:str):#Setter tipo con validacion
        valor=valor.upper()
        valores_permitidos = ["NORMAL", "TECNICA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad publica debe ser uno de los siguientes: {valores_permitidos}.")             
        self._tipo = valor
    def iniciar(self):#Metodo iniciar la universidad
        print(f"La universidad {self.nombre} ha iniciado su admisión en {self.Pais}.")
    def finalizar(self):#Metodo finalizar la universidad
        print(f"La universidad {self.nombre} ha finalizado su admisión en {self.Pais}.")

class Oferta_Academica(Universidad):#Clase Oferta_Academica
    def __init__(self, carrera:str, cantidad:int, codigo:int, modalidad_oferta:str):
        self.carrera = carrera
        self.cantidad = cantidad
        self.codigo = codigo
        self.modalidad_oferta = modalidad_oferta
        self.cupos = cantidad
        self.postulantes = []
    @property
    def cantidad(self):#Getter cantidad
        return self._cantidad
    @cantidad.setter
    def cantidad(self, valor:int):#Setter cantidad con validacion
        if valor < 0:
            raise ValueError("La cantidad de cupos no puede ser negativa.")
        self._cantidad = valor  
    def crear_oferta(self):#Metodo crear_oferta
        print(f"La oferta académica para la carrera de {self.carrera} con {self.cantidad} cupos ha sido creada.")
    def esta_disponible(self): #Método esta_disponible
        return self.cantidad > 0
    def validar_modalidad(self): #Método validar_modalidad
        modalidades_validas = ["Presencial", "Virtual", "Híbrida"]
        if self.modalidad_oferta not in modalidades_validas:
            raise ValueError("Modalidad no válida")
    def validar_codigo(self): #Método validar_codigo
        if self.codigo <= 0:
            raise ValueError("El código debe ser un número positivo")
    def verificar_cupos(self): #Método verificar_cupos
        disponibles = self.cupos - len(self.postulantes)
        print(f"Cupos restantes para {self.carrera}: {disponibles}")
    
class Periodo(Iniciar_fase,Finalizar_fase):#Clase Periodo que hereda de Iniciar_fase y Finalizar_fase
    def __init__(self, Ano_Lectivo:str, Semestre:str):#Atributos de la clase Periodo
        self.Ano_Lectivo = Ano_Lectivo
        self.Semestre = Semestre
        print("Los datos del periodo fueron ingresados con éxitos")
    def iniciar(self):#Metodo iniciar el peridodo
        print(f"El periodo {self.Ano_Lectivo} - {self.Semestre} ha iniciado.")
    def finalizar(self):#Metodo finalizar el periodo
        print(f"El periodo {self.Ano_Lectivo} - {self.Semestre} ha finalizado.")

class CronogramaAcademico:#Clase Cronograma Academico
    def __init__(self, anio, periodo):#Atributos de la Clase Cronograma Academico
        self.clave = f"{anio}-{periodo}"
        with open("cronograma_oficial.json", "r", encoding="utf-8") as f:
            cronogramas = json.load(f)
        if self.clave not in cronogramas:
            raise ValueError("No existe cronograma para este periodo")
        self.fases = self._convertir_fechas(cronogramas[self.clave])
    def _convertir_fechas(self, fases):#Metodo convertir a fecha
        for fase in fases:
            fases[fase]["inicio"] = datetime.strptime(
                fases[fase]["inicio"], "%Y-%m-%d"
            ).date()
            fases[fase]["fin"] = datetime.strptime(
                fases[fase]["fin"], "%Y-%m-%d"
            ).date()
        return fases
    def fase_activa(self, fase):#Metodo fase activa
        hoy = date.today()
        return self.fases[fase]["inicio"] <= hoy <= self.fases[fase]["fin"]
    def obtener_fechas(self, fase):#Metodo obtener fecha
        return self.fases[fase]
    def mostrar_estado_fases(self):#Metodo mostrar estado de fecha
        estado = {}
        hoy = date.today()
        for fase, info in self.fases.items():
            estado[fase] = {
                "inicio": info["inicio"],
                "fin": info["fin"],
                "activa": info["inicio"] <= hoy <= info["fin"]
            }
        return estado

class Inscripcion(Iniciar_fase,Finalizar_fase):#Clase Inscripcion que hereda de Iniciar_fase y Finalizar_fase
    def __init__(self, carrera: str, facultad: str):
        self.carrera = carrera
        self.facultad = facultad
    def iniciar(self):#Metodo iniciar la inscripción
        print("Las inscripciones universitarias han comenzado.")
    def finalizar(self):#Metodo finalizar la inscripción
        print("Las inscripciones universitarias han finalizado.")

class tipo_de_examen(ABC):#Clase base
    @abstractmethod
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        pass
    @abstractmethod
    def descripcion(self) -> str:
        pass
#Tipos de examen
class mixto(tipo_de_examen):
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        return int((respuestas_correctas / total_preguntas) * 1000)
    def descripcion(self) -> str:
        return "Examen mixto (conocimiento general y área)"

class por_area(tipo_de_examen):
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        return int((respuestas_correctas / total_preguntas) * 1000)
    def descripcion(self) -> str:
        return "Examen por área de conocimiento"

class general(tipo_de_examen):
    def calcular_resultado(self, respuestas_correctas: int, total_preguntas: int) -> int:
        return int((respuestas_correctas / total_preguntas) * 1000)
    def descripcion(self) -> str:
        return "Examen de conocimiento general"

class ExamenFactory:#Factory Method
    @staticmethod
    def crear_examen(tipo: str) -> tipo_de_examen:
        tipo = tipo.lower()
        if tipo == "mixto":
            return mixto()
        elif tipo == "area":
            return por_area()
        elif tipo == "general":
            return general()
        else:
            raise ValueError("Tipo de examen no válido")

class Evaluacion:#Clase que usa la fábrica para obtener el tipo de examen
    def __init__(self, tipo_examen: tipo_de_examen):
        self.tipo_examen = tipo_examen
        self._puntaje = 0
    def aplicar_examen(self, respuestas_correctas: int, total_preguntas: int):
        self._puntaje = self.tipo_examen.calcular_resultado(respuestas_correctas, total_preguntas)
    def mostrar_resultado(self):
        print(self.tipo_examen.descripcion())
        print(f"Puntaje obtenido: {self._puntaje}/1000")

class Postulacion(Iniciar_fase, Finalizar_fase):#Clase que notifica a múltiples observadores
    def __init__(self, carrera: str, aspirante ):
        from Usuario import Aspirante
        if not isinstance(aspirante, Aspirante):
            raise TypeError("Debe ser un objeto Aspirante")
        self.carrera = carrera
        self.aspirante = aspirante
        self._nota_final = 0
        self.detalle_puntos = {}
    def iniciar(self):#Metodo iniciar la postulación
        print("Las postulaciones universitarias han comenzado.")
    def finalizar(self):#Metodo finalizar la postulación
        print("La postulación ha finalizado.")
    def calcular_nota_situacion(self):#Metodo calcular la nota de situación
        if self.aspirante.nacionalidad.upper() == "ECUATORIANO":#Si es Ecuatoriano
            self.nota_final = int((self.aspirante.nota_grado * 0.5 + self.aspirante._nota_evaluacion * 0.5) * 10)  
        else:#Si es extranjero
            self.nota_final = int(self.aspirante._nota_evaluacion * 10)  
        puntos = 0#Puntos de extras
        detalle = {}
        if getattr(self.aspirante, "condicion_socioeconomica", False):
            puntos += 15
            detalle["condicion_socioeconomica"] = 15
        if getattr(self.aspirante, "ruralidad", False):
            puntos += 5
            detalle["ruralidad"] = 5
        if getattr(self.aspirante, "territorialidad", False):
            puntos += 10
            detalle["territorialidad"] = 10
        if getattr(self.aspirante, "discapacidad", False):
            puntos += 5
            detalle["discapacidad"] = 5
        if getattr(self.aspirante, "bono_jgl", False):
            puntos += 5
            detalle["bono_jgl"] = 5
        if getattr(self.aspirante, "victima_violencia", False):
            puntos += 5
            detalle["victima_violencia"] = 5
        if getattr(self.aspirante, "migrantes_retornados", False):
            puntos += 5
            detalle["migrantes_retornados"] = 5
        if getattr(self.aspirante, "femicidio", False):
            puntos += 5
            detalle["femicidio"] = 5
        if getattr(self.aspirante, "enfermedades_catastroficas", False):
            puntos += 5
            detalle["enfermedades_catastroficas"] = 5
        if getattr(self.aspirante, "casa_acogida", False):
            puntos += 5
            detalle["casa_acogida"] = 5
        if getattr(self.aspirante, "pueblos_nacionalidades", False):
            puntos += 10
            detalle["pueblos_nacionalidades"] = 10
        self.nota_final += puntos
        self.detalle_puntos = detalle
        return {"nota_final": self.nota_final, "detalle_puntos": detalle}
    def reporte_postulaciones(lista_postulantes, carrera):#Metodo de reporte de postulaciones
        reporte = []
        for asp in lista_postulantes:
            postulacion = Postulacion(asp, carrera)
            postulacion.calcular_nota()
            reporte.append({
                "nombre": asp.nombre,
                "cedula": asp.cedula,
                "carrera": carrera,
                "nota_final": postulacion.nota_final,
                "detalle_puntos": postulacion.detalle_puntos
            })
        return reporte

class Servicio_web(Oferta_Academica):#Clase Servicio_web que hereda de Oferta_Academica
    Pais = "Ecuador"
    def __init__(self, provincia:str, enlace:str, carrera:str, cantidad:int):
        super().__init__(carrera, cantidad)
        self.nombre = provincia
        self.enlace = enlace 
        self.estado = "PENDIENTE"
    @property
    def estado(self):#Getter estado
        return self._estado
    @estado.setter
    def estado(self, valor:str):#Setter estado
        valor=valor.upper()
        valores_permitidos = ["PENDIENTE", "APROBADA", "RECHAZADA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El estado debe ser uno de los siguientes: {valores_permitidos}.")             
        self._estado = valor
    def estado_servicio(self):#Metodo estado_servicio
        print(f"El servicio web de la provincia de {self.nombre} está activo.")
        if self.estado=="APROBADA":#Verifica si la oferta academica fue aceptada
            print("La oferta academica fue aceptada.")   
        elif self.estado=="RECHAZADA":#Verifica si la oferta academica fue rechazada
            print("La oferta academica fue rechazada.")
        else:#Verifica si la oferta academica esta pendiente
            print("La oferta academica está pendiente de revisión.")  
    
