from abc import ABC#importar ABCMeta
from abc import abstractmethod#importar abstractmethod
import json#importar json
import os#importar os
from datetime import date, datetime, timedelta#importar date para manejo de fechas
from SASFU import CronogramaAcademico#importar De SASFU una clase 
class Autenticable(ABC):#Interfaz Autenticable
    @abstractmethod#Método iniciar sesión
    def iniciar_sesion(self):
        pass
    @abstractmethod#Método cerrar sesión
    def cerrar_sesion(self):
        pass

class AsignarSede(ABC):#Interfaz AsignarSede
    @abstractmethod#Método asignar sede
    def asignar_sede(self, aspirante, codigo_sala, fecha):
        pass

class Cargable(ABC):#Interfaz Cargable
    @abstractmethod#Método cargar datos
    def cargar_datos(self):
        pass

class SolicitudAsistencia(ABC):#Interfaz SolicitudAsistencia
    @abstractmethod#Método crear solicitud asistencia
    def crear_solicitud_asistencia(self, asunto: str):
        pass
    @abstractmethod#Método estado solicitud
    def estado_solicitud(self):
        pass

class GestorSede(ABC):#Interfaz GestorSede
    @abstractmethod#Método notificar sede
    def notificar_sede(self):
        pass
    @abstractmethod#Método imprimir documentación sede
    def imprimir_documentacion_sede(self, sede: str):
        pass

class GestionProceso(ABC):#Interfaz GestionProceso
    @abstractmethod#Método abrir inscripciones
    def abrir_inscripciones(self, fecha_inicio: date, fecha_fin: date):
        pass
    @abstractmethod#Método cerrar inscripciones
    def cerrar_inscripciones(self):
        pass
    @abstractmethod#Método inscripciones activas
    def inscripciones_activas(self):
        pass
    @abstractmethod#Método abrir evaluación
    def abrir_evaluaciones(self, fecha_inicio: date, fecha_fin: date):
        pass
    @abstractmethod#Método cerrar evaluación
    def cerrar_evaluaciones(self):
        pass
    @abstractmethod#Método evaluación activa
    def evaluaciones_activas(self):
        pass
    @abstractmethod#Método abrir postulaciones
    def abrir_postulaciones(self, fecha_inicio: date, fecha_fin: date):
        pass
    @abstractmethod#Método cerrar postulaciones
    def cerrar_postulaciones(self):
        pass
    @abstractmethod#Método postulaciones activas
    def postulaciones_activas(self):
        pass
    
class RegistroInscripcion(ABC):#Interfaz RegistroInscripcion
    def registrar_inscripcion(self, facultad: str, carrera: str):
        pass

class Usuario(Autenticable, ABC):#Clase Abstracta Usuario
    def __init__(self, cedula_pasaporte: str, nombre: str, apellido: str, correo: str):
        self.cedula_pasaporte = cedula_pasaporte
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
    def iniciar_sesion(self):#Valor por defecto para usuarios que no implementan autenticación
        raise NotImplementedError("Este usuario no implementa autenticación")
    def cerrar_sesion(self):#Valor por defecto para usuarios que no implementan autenticación
        raise NotImplementedError("Este usuario no implementa autenticación")

class Repositorio(ABC):#Interfaz Repositorio
    @abstractmethod#Método leer datos
    def leer_todos(self):
        pass
    @abstractmethod#Método guardar datos
    def guardar_todos(self, datos):
        pass

def validar_fecha_laboral(fecha_str):#Función de validar fecha 
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    if fecha.weekday() >= 5:#No pertenece al fin de semana
        return None
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    return dias[fecha.weekday()]

class RepositorioAspirantesJSON(Repositorio):#Repositorio JSON y Chain of Responsibility
    def __init__(self, archivo="aspirantes_universidad.json"):#Leer archivo JSON
        base_dir = os.path.dirname(os.path.abspath(__file__))#Directorio base
        self.archivo = os.path.join(base_dir, archivo)
        if not os.path.exists(self.archivo):#Crear archivo si no existe
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
    def leer_todos(self):#Leer base de datos
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print("ERROR EN EL JSON:", e)
            raise
    def guardar_todos(self, datos):#Guardar base de datos
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

class RepositorioSolicitudesJSON(Repositorio):#Repositorio JSON de solicitudes y Chain of Responsibility
    def __init__(self, archivo="solicitudes_asistencia.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.archivo = os.path.join(base_dir, archivo)
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
    def leer_todos(self):#Leer base de datos
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    def guardar_todos(self, datos):#Guardar base de datos
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

class ServicioAutenticacion:#Clase ServicioAutenticacion, Inyección de dependencias y Chain of Responsibility
    def __init__(self, repositorio: Repositorio):
        self.repositorio = repositorio
    def crear_usuario(self, cedula, usuario: str, contrasena: str):#Método crear usuario
        if not contrasena:
            raise ValueError("La contraseña no puede estar vacía")
        aspirantes = self.repositorio.leer_todos()
        for a in aspirantes:#Buscar aspirante por cédula
            if a["numero_identidad"] == cedula:
                if "usuario" in a:
                    raise ValueError("El usuario ya existe")
                if usuario != cedula:# Validar que el usuario sea igual a la cédula o pasaporte
                    raise ValueError("El usuario debe ser igual a la cédula o pasaporte")
                a["usuario"] = usuario
                a["contrasena"] = contrasena
                self.repositorio.guardar_todos(aspirantes)
                return
        raise ValueError("No existe aspirante con esa identificación")
    def iniciar_sesion(self, usuario: str, contrasena: str):#Método iniciar sesión
        aspirantes = self.repositorio.leer_todos()
        for a in aspirantes:#Buscar usuario y contraseña
            if a.get("usuario") == usuario and a.get("contrasena") == contrasena:
                print("Inicio de sesión exitoso")
                return True
        print("Credenciales incorrectas")
        return False

class ServicioCambioContrasena:#Clase ServicioCambioContrasena, Inyección de dependencias y Chain of Responsibility
    def __init__(self, repositorio: Repositorio):
        self.repositorio = repositorio
    def actualizar_contrasena(self, cedula, contrasena_actual, nueva_contrasena, confirmar):#Método actualizar contraseña
        if nueva_contrasena != confirmar:
            raise ValueError("Las contraseñas nuevas no coinciden")
        aspirantes = self.repositorio.leer_todos()
        for a in aspirantes:#Buscar aspirante por cédula
            if a["numero_identidad"] == cedula:#Encontrado aspirante
                if a.get("contrasena") != contrasena_actual:#Verificar contraseña actual
                    raise ValueError("Contraseña actual incorrecta")
                a["contrasena"] = nueva_contrasena
                self.repositorio.guardar_todos(aspirantes)#Guardar datos
                return
        raise ValueError("Usuario no encontrado")

class SistemaFacade:#Clase SistemaFacade y Patrón Facade
    def __init__(self):
        self.repo = RepositorioAspirantesJSON()
        self.auth = ServicioAutenticacion(self.repo)
        self.cambio_contrasena = ServicioCambioContrasena(self.repo)
    def registrar_usuario(self, cedula, usuario, contrasena):#Registrar usuario
        self.auth.crear_usuario(cedula, usuario, contrasena)
    def login(self, usuario, contrasena):#Iniciar sesión
        return self.auth.iniciar_sesion(usuario, contrasena)
    def cambiar_contrasena(self, cedula, contrasena_actual, nueva_contrasena, confirmar):#Cambiar contraseña
        self.cambio_contrasena.actualizar_contrasena(cedula, contrasena_actual, nueva_contrasena, confirmar)

class Administrador(Usuario, AsignarSede, Cargable, GestionProceso):#Clase Hija Administrador de Usuario
    def __init__(self, cedula, nombre, apellido, correo, cargo):
        super().__init__(cedula, nombre, apellido, correo)
        self.cargo = cargo
        self.cronograma = None
        self.fases = {# Diccionario de fases y secuencia
            "inscripcion": {"inicio": None, "fin": None},
            "evaluacion": {"inicio": None, "fin": None},
            "postulacion": {"inicio": None, "fin": None}
        }
        self.orden_fases = ["inscripcion", "evaluacion", "postulacion"]
    def iniciar_sesion(self):#Iniciar sesión
        print(f"Bienvenido Administrador {self.nombre}")
    def cerrar_sesion(self):#Cerrar sesión
        print(f"Hasta luego Administrador {self.nombre}")
    def asignar_sede(self, aspirante, codigo_sala, fecha):#Asignar sede
        dia = validar_fecha_laboral(fecha)#Validar fecha
        if dia is None:#No puede ser fines de semana
            print("No se puede asignar sede en fines de semana.")
            return
        ruta_salas = os.path.join(os.path.dirname(__file__), "horarios_evaluacion.json")
        if not os.path.exists(ruta_salas):
            print("No existe la base de datos de horarios.")
            print("Primero debe generar los horarios.")
            return
        with open(ruta_salas, "r", encoding="utf-8") as f:#Leer base de datos de salas
            salas = json.load(f)
        sala = next((s for s in salas if s["codigo"] == codigo_sala), None)#Buscar sala por codigo
        if not sala:#Codigo no válido
            print("Código de sala no válido.")
            return
        if sala["cantidad"] <= 0:#Verificar cupos disponibles
            print("No hay cupos disponibles en esta sala.")
            return
        if sala["matriz"] != aspirante.inscripciones.get("matriz"):#Validar matriz
            print("La matriz de la sala no coincide con la inscripción del aspirante.")
            return
        repo = RepositorioAspirantesJSON()#Acceder al repositorio de aspirantes
        aspirantes_db = repo.leer_todos()
        for a in aspirantes_db:#Buscar aspirante y asignar sede
            if a["numero_identidad"] == aspirante.cedula_pasaporte:
                a["sede_asignada"] = {
                    "facultad": sala["facultad"],#Facultad asignada
                    "aula": sala["aula"],#Aula asignada
                    "horario": sala["horario"],#Horario de evaluación
                    "matriz": sala["matriz"],#Matriz de la sede
                    "codigo": sala["codigo"],#Codigo de la sala
                    "fecha": fecha,#Fecha de evaluación
                    "dia": dia#Dia de la semana
                }
                sala["cantidad"] -= 1#Disminuir cupo de la sala
                repo.guardar_todos(aspirantes_db)#Guardar cambios del aspirante
                #Guardar salas actualizadas
                with open(ruta_salas, "w", encoding="utf-8") as f:
                    json.dump(salas, f, indent=4, ensure_ascii=False)
                print("Sede asignada correctamente.")
                return
        print("No se encontró al aspirante en la base de datos.")
    def cargar_datos(self):#Cargar datos
        print("El administrador está cargando datos...")
    def gestionar_soporte(self, solicitud_id):#Gestionar solicitudes derivadas por soporte
        repo = RepositorioSolicitudesJSON()#Repositorio de solicitudes
        solicitudes = repo.leer_todos()#Leer todas las solicitudes
        solicitud = next((s for s in solicitudes if s["id"] == solicitud_id), None)
        if not solicitud:#Verificar si la solicitud existe
            print(f"No se encontró la solicitud con ID {solicitud_id}.")
            return
        print("\n=== Gestionando Solicitud ===")
        print(f"ID: {solicitud['id']}")
        print(f"Cédula Aspirante: {solicitud['cedula_aspirante']}")
        print(f"Asunto: {solicitud.get('asunto', solicitud.get('mensaje',''))}")
        print(f"Tipo actual: {solicitud.get('tipo', 'No asignado')}")
        estado_actual = (
            "Pendiente" if solicitud.get("estado") is None
            else "Aceptada" if solicitud.get("estado")
            else "Rechazada"
        )
        print(f"Estado actual: {estado_actual}")
        tipo = input("Ingrese tipo de solicitud (tecnico/academico/grave): ").lower()
        solicitud["tipo"] = tipo#Asignar tipo de solicitud
        if tipo in ["tecnico", "academico", "grave"]:#Validar tipo
            decision = input("¿Aceptar la solicitud? (s/n): ").lower()
            if decision == "s":#Aceptar solicitud
                solicitud["estado"] = True
                print(f"Solicitud ID {solicitud_id} aceptada como '{tipo}'.")
            elif decision == "n":#Rechazar solicitud
                solicitud["estado"] = False
                print(f"Solicitud ID {solicitud_id} rechazada como '{tipo}'.")
            else:#Opción inválida
                print("Opción inválida, no se modificó el estado.")
        else:#Tipo inválido
            solicitud["estado"] = False
            print(f"Tipo '{tipo}' no válido. Solicitud rechazada automáticamente.")
        repo.guardar_todos(solicitudes)#Guardar cambios en el repositorio
    def _abrir_fase(self, fase, fecha_inicio, fecha_fin):#Abrir fase
        if fecha_inicio > fecha_fin:#Fecha inicio no puede ser mayor a fecha fin
            raise ValueError("La fecha inicio no puede ser mayor a la fecha fin")
        if self.fases[fase]["inicio"] is not None:#Validar si la fase ya está abierta
            raise ValueError(f"{fase.capitalize()} ya fue abierta")
        idx = self.orden_fases.index(fase)#Obtener índice de la fase
        if idx > 0:# Validar que la fase anterior esté cerrada
            fase_anterior = self.orden_fases[idx - 1]#Obtener fase anterior
            if self.fases[fase_anterior]["fin"] is None:#Validar si la fase anterior está cerrada
                raise ValueError(f"No se puede abrir {fase} antes de cerrar {fase_anterior}")
        self.fases[fase]["inicio"] = fecha_inicio#Abrir fase con fechas
        self.fases[fase]["fin"] = fecha_fin#Cerrar fase con fechas
        print(f"{fase.capitalize()} abierta desde {fecha_inicio} hasta {fecha_fin}")
    def _cerrar_fase(self, fase):#Cerrar fase
        if self.fases[fase]["inicio"] is None:#Validar si la fase está abierta
            print(f"No se puede cerrar {fase} que no se ha abierto")
            return
        self.fases[fase]["fin"] = date.today()#Cerrar fase con fecha actual
        print(f"{fase.capitalize()} cerrada")
    def _fase_activa(self, fase):#Verificar si fase está activa
        inicio = self.fases[fase]["inicio"]#Fecha inicio
        fin = self.fases[fase]["fin"]#Fecha fin
        if not inicio or not fin:#Si no hay fechas, fase no está activa
            return False
        hoy = date.today()#Fecha actual
        return inicio <= hoy <= fin#Verificar si la fase está activa
    def abrir_inscripciones(self, fecha_inicio, fecha_fin):#Abrir inscripciones
        self._abrir_fase("inscripcion", fecha_inicio, fecha_fin)
    def cerrar_inscripciones(self):#Cerrar inscripciones
        self._cerrar_fase("inscripcion")
    def inscripciones_activas(self):#Verificar si inscripciones están activas
        return self._fase_activa("inscripcion")
    def abrir_evaluaciones(self, fecha_inicio, fecha_fin):#Abrir evaluación
        self._abrir_fase("evaluacion", fecha_inicio, fecha_fin)
    def cerrar_evaluaciones(self):#Cerrar evaluación
        self._cerrar_fase("evaluacion")
    def evaluaciones_activas(self):#Verificar si evaluación está activa
        return self._fase_activa("evaluacion")
    def abrir_postulaciones(self, fecha_inicio, fecha_fin):#Abrir postulaciones
        self._abrir_fase("postulacion", fecha_inicio, fecha_fin)
    def cerrar_postulaciones(self):#Cerrar postulaciones
        self._cerrar_fase("postulacion")
    def postulaciones_activas(self):#Verificar si postulaciones están activas
        return self._fase_activa("postulacion")
    def elegir_periodo(self):
        print("=== Elegir periodo académico ===")
        anio = input("Ingrese el año lectivo (ej: 2025): ")
        periodo = input("Ingrese el periodo (1 o 2): ")
        try:
            self.cronograma = CronogramaAcademico(anio, periodo)
            print("Periodo cargado correctamente.")
        except Exception as e:
            print("Error:", e)
    def mostrar_fechas_inscripciones(self):
        if self.cronograma is None:
            print("Primero debe elegir un periodo.")
            return
        fechas = self.cronograma.obtener_fechas("inscripcion")
        print("=== Fechas de Inscripción ===")
        print("Inicio:", fechas["inicio"])
        print("Fin:", fechas["fin"])



class Aspirante(Usuario, Cargable, SolicitudAsistencia, GestorSede, RegistroInscripcion):#Clase Hija Aspirante de Usuario
    def __init__(self, cedula, nombre, apellido, correo, telefono, titulo, nota_grado):
        super().__init__(cedula, nombre, apellido, correo)
        self.telefono = telefono
        self.titulo = titulo
        self.nombre = nombre
        self._nota_grado = None
        self.nota_grado = nota_grado
        self.inscripciones = {}#Guardar inscripciones
        self._nota_evaluacion = 0#Nota de evaluación por defecto 0 
        self.dio_evaluacion = False#Confirma si dio la evaluación
        ruta_fac = os.path.join(os.path.dirname(__file__), "ofertas.json")#Ruta del archivo ofertas.json
        try:#Cargar facultades y carreras desde JSON
            with open(ruta_fac, "r", encoding="utf-8") as f:#Abrir archivo JSON
                datos = json.load(f)#Cargar datos JSON
            self.facultades_carreras = {}#Diccionario facultades y carreras
            for item in datos:#Recorrer datos JSON
                fac = item["Facultad"]
                car = item["Carrera"]
                mat = item["Matriz"]
                cod = item["Codigo"]
                if fac not in self.facultades_carreras:#Agregar facultad si no existe
                    self.facultades_carreras[fac] = []#Lista de carreras
                if all(c["carrera"] != car or c["matriz"] != mat for c in self.facultades_carreras[fac]):#Evitar duplicados
                    self.facultades_carreras[fac].append({"carrera": car, "matriz": mat, "codigo": cod})
        except Exception as e:#Manejo de errores al cargar JSON
            print("Error cargando facultades y carreras:", e)
            self.facultades_carreras = {}#Diccionario vacío en caso de error
    @property#Propiedad nota grado
    def nota_grado(self):
        return self._nota_grado
    @nota_grado.setter#Setter nota grado con validación
    def nota_grado(self, valor):
        if not (0 <= valor <= 10):
            raise ValueError("La nota debe estar entre 0 y 10.")
        self._nota_grado = valor
    @property##Propiedad nota evaluación
    def nota_evaluacion(self):
        return self._nota_evaluacion
    @nota_evaluacion.setter
    def nota_evaluacion(self, valor):
        if not (0 <= valor <= 1000):
            raise ValueError("La nota de evaluación debe estar entre 0 y 1000.")
        self._nota_evaluacion = valor
        self.dio_evaluacion = valor > 0
    def iniciar_sesion(self):
        print(f"Aspirante {self.nombre} inició sesión.")
    def cerrar_sesion(self):
        print(f"Aspirante {self.nombre} cerró sesión.")
    def cargar_datos(self):
        print("El aspirante ha cargado sus datos.")
    def notificar_sede(self):
        repo = RepositorioAspirantesJSON()
        aspirantes = repo.leer_todos()
        for a in aspirantes:#Buscar aspirante por cédula
            if a["numero_identidad"] == self.cedula_pasaporte:#Encontrado aspirante
                sede_info = getattr(self, "sede_asignada", None)
                if sede_info:#Si hay sede asignada
                    print(f"Aspirante {self.nombre} notificado de su sede:")
                    print(f"  Sede: {sede_info['sede']}")
                    print(f"  Facultad: {sede_info['facultad']}")
                    print(f"  Carrera: {sede_info['carrera']}")
                    print(f"  Horario: {sede_info['hora_dia']}")
                    print(f"  Evaluación: del {sede_info['fecha_inicio_eval']} al {sede_info['fecha_fin_eval']}")
                else:#No tiene sede asignada
                    print(f"Aspirante {self.nombre} aún no tiene sede asignada.")
                return
        print(f"Aspirante {self.nombre} no se encontró en la base de datos.")
    def imprimir_documentacion_sede(self, sede):#Imprimir documentación sede
        print(f"Aspirante {self.nombre} imprime documentación para la sede: {sede}")
    def registrar_inscripcion(self, facultad: str, carrera: str, matriz: str):#Registrar inscripción
        facultad_lc = facultad.strip().lower()#Buscar facultad en minúsculas
        carrera_lc = carrera.strip().lower()#Buscar carrera en minúsculas
        matriz_lc = matriz.strip().lower()#Buscar matriz en minúsculas
        facultad_encontrada = None#Buscar facultad
        for fac in self.facultades_carreras:#Recorrer facultades
            if fac.lower() == facultad_lc:#Comparar en minúsculas para permitir mayúsculas diferentes
                facultad_encontrada = fac
                break
        if not facultad_encontrada:#Si no se encontró la facultad
            print(f"No se encontró la facultad '{facultad}'.")
            return
        carrera_obj = next(
            (c for c in self.facultades_carreras[facultad_encontrada]
            if c["carrera"].lower() == carrera_lc and c["matriz"].lower() == matriz_lc),
            None
        )
        if not carrera_obj:#Si no se encontró la carrera con la matriz correcta
            print(f"No se encontró la carrera '{carrera}' en la matriz '{matriz}'.")
            return
        self.inscripciones = {
            "facultad": facultad_encontrada,
            "carrera": carrera_obj["carrera"],
            "matriz": carrera_obj["matriz"]
        }
        codigo = carrera_obj["codigo"]
        repo = RepositorioAspirantesJSON()
        aspirantes = repo.leer_todos()
        for a in aspirantes:#Recorrer los aspirantes
            if a["numero_identidad"] == self.cedula_pasaporte:
                a["inscripcion"] = self.inscripciones
                a["codigo_carrera"] = codigo
                repo.guardar_todos(aspirantes)#Guardar datos
                print(f"Aspirante {self.nombre} inscrito en {facultad_encontrada} - {carrera_obj['carrera']} ({carrera_obj['matriz']})")
                return
        print("No se encontró al aspirante en la base de datos.")
    def crear_solicitud_asistencia(self, asunto):#Crear solicitud de asistencia
        repo = RepositorioSolicitudesJSON()#Instancia del repositorio
        solicitudes = repo.leer_todos()#Leer todas las solicitudes
        nueva = {
            "id": len(solicitudes) + 1,
            "cedula_aspirante": self.cedula_pasaporte,
            "asunto": asunto,
            "estado": None,
            "fecha": datetime.now().isoformat()
        }
        solicitudes.append(nueva)
        repo.guardar_todos(solicitudes)
        print(f"Aspirante {self.nombre} creó una solicitud de asistencia.")
    def estado_solicitud(self):#Estado de la Solicitud
        repo = RepositorioSolicitudesJSON()
        solicitudes = repo.leer_todos()
        for s in solicitudes:#Recorrer las solicitudes
            if s["cedula_aspirante"] == self.cedula_pasaporte:#Mostrar solo sus solicitudes
                print(f"Asunto: {s['asunto']} | Estado: {s['estado']}")
                return
        print("No tiene solicitudes registradas.")

class Soporte(Usuario):#Clase Hija Soporte de Usuario
    def iniciar_sesion(self):#Iniciar sesión
        print(f"Soporte {self.nombre} inició sesión.")
    def cerrar_sesion(self):#Cerrar sesión
        print(f"Soporte {self.nombre} cerró sesión.")
    def responder_solicitud(self, id_solicitud, aceptar: bool):#Responder solicitud
        repo = RepositorioSolicitudesJSON()#Instancia del repositorio
        solicitudes = repo.leer_todos()#Leer todas las solicitudes
        for s in solicitudes:#Buscar solicitud por ID
            if s["id"] == id_solicitud:#Solicitud encontrada
                if s["estado"] is not None:#Verificar si ya fue respondida
                    print("La solicitud ya fue respondida.")
                    return
                s["estado"] = aceptar#Actualizar estado
                repo.guardar_todos(solicitudes)#Guardar datos
                if aceptar:#Respuesta aceptada
                    print("Solicitud aceptada por Soporte.")
                else:#Respuesta rechazada
                    print("Solicitud rechazada por Soporte.")
                return
        print("Solicitud no encontrada.")

class ManejadorAsistencia(ABC):#Clase abstracta ManejadorAsistencia y Patrón Chain of Responsibility
    def __init__(self, siguiente=None):
        self.siguiente = siguiente
    @abstractmethod#Método manejar solicitud
    def manejar(self, solicitud):
        pass

class SoporteHandler(ManejadorAsistencia):#Clase SoporteHandler
    def __init__(self, usuario, siguiente=None):#Inicializar con usuario y siguiente manejador
        super().__init__(siguiente)
        self.usuario = usuario
    def manejar(self, solicitud):#Manejar solicitud
        if solicitud == "tecnico":#Solicitud técnica
            print(f"Soporte {self.usuario.nombre} resolvió el problema técnico")
        elif self.siguiente:#Pasar al siguiente manejador si existe
            print(f"Soporte {self.usuario.nombre} escala al Administrador")
            self.siguiente.manejar(solicitud)

class AdministradorHandler(ManejadorAsistencia):#Clase AdministradorHandler
    def __init__(self, usuario, siguiente=None):#Inicializar con usuario y siguiente manejador
        super().__init__(siguiente)
        self.usuario = usuario
    def manejar(self, solicitud):#Manejar solicitud
        if solicitud in ["academico", "grave"]:#Solicitud académica o grave
            print(f"Administrador {self.usuario.nombre} resolvió el problema")
        else:#Pasar al siguiente manejador si existe
            print("Solicitud no válida")
