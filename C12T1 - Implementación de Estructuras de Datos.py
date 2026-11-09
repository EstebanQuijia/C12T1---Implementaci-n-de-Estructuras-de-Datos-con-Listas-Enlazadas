# =====================================================================
# TEMA 6: Listas Enlazadas, Pilas y Colas (Parte 1)
# Resolución de Problemas con Listas Enlazadas Simples (Sin librerías externas)
# =====================================================================

# =====================================================================
# PROBLEMA 1: Sistema de Gestión de Procesos del Sistema Operativo
# =====================================================================

class Proceso:
    """Nodo que representa un proceso en el sistema operativo."""
    def __init__(self, id_proc, nombre, estado, tiempo_creacion, tiempo_cpu):
        self.id_proc = id_proc
        self.nombre = nombre
        self.estado = estado  # 'listo', 'en ejecucion', 'bloqueado', 'terminado'
        self.tiempo_creacion = tiempo_creacion
        self.tiempo_cpu = tiempo_cpu
        self.siguiente = None

class ListaProcesos:
    """Lista enlazada para gestionar procesos del SO."""
    def __init__(self):
        self.cabeza = None

    def agregar_proceso(self, id_proc, nombre, estado, t_creacion, t_cpu):
        nuevo = Proceso(id_proc, nombre, estado, t_creacion, t_cpu)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def cambiar_estado(self, id_proc, nuevo_estado):
        actual = self.cabeza
        while actual:
            if actual.id_proc == id_proc:
                actual.estado = nuevo_estado
                print(f"[P1] Proceso {id_proc} ({actual.nombre}) cambió a: {nuevo_estado}")
                return True
            actual = actual.siguiente
        return False

    def eliminar_terminados(self):
        """Elimina todos los procesos cuyo estado sea 'terminado'."""
        while self.cabeza and self.cabeza.estado == 'terminado':
            print(f"[P1] Eliminando proceso terminado: ID {self.cabeza.id_proc}")
            self.cabeza = self.cabeza.siguiente
        
        actual = self.cabeza
        while actual and actual.siguiente:
            if actual.siguiente.estado == 'terminado':
                print(f"[P1] Eliminando proceso terminado: ID {actual.siguiente.id_proc}")
                actual.siguiente = actual.siguiente.siguiente
            else:
                actual = actual.siguiente

    def mover_al_inicio(self, id_proc):
        """Mueve un proceso al principio de la lista (simula alta prioridad)."""
        if not self.cabeza or self.cabeza.id_proc == id_proc:
            return
        
        anterior = None
        actual = self.cabeza
        while actual and actual.id_proc != id_proc:
            anterior = actual
            actual = actual.siguiente
            
        if actual:
            anterior.siguiente = actual.siguiente
            actual.siguiente = self.cabeza
            self.cabeza = actual
            print(f"[P1] Proceso {id_proc} movido al inicio por prioridad.")

    def mostrar_procesos(self):
        print("\n--- LISTA DE PROCESOS ---")
        actual = self.cabeza
        while actual:
            print(f"ID: {actual.id_proc} | Nombre: {actual.nombre} | Estado: {actual.estado} | CPU: {actual.tiempo_cpu}s")
            actual = actual.siguiente
        print("-" * 35)

    def calcular_tiempo_espera_promedio(self):
        actual = self.cabeza
        total_espera = 0
        contador = 0
        tiempo_acumulado = 0
        while actual:
            total_espera += tiempo_acumulado
            tiempo_acumulado += actual.tiempo_cpu
            contador += 1
            actual = actual.siguiente
        return (total_espera / contador) if contador > 0 else 0.0


# =====================================================================
# PROBLEMA 2: Editor de Texto Básico con Operaciones de Línea
# =====================================================================

class NodoLinea:
    def __init__(self, texto):
        self.texto = texto
        self.siguiente = None

class EditorTexto:
    def __init__(self):
        self.cabeza = None

    def insertar_linea(self, posicion, texto):
        nuevo = NodoLinea(texto)
        if posicion == 1:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            return
        
        actual = self.cabeza
        idx = 1
        while actual and idx < posicion - 1:
            actual = actual.siguiente
            idx += 1
            
        if actual:
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
        else:
            self.agregar_al_final(texto)

    def agregar_al_final(self, texto):
        nuevo = NodoLinea(texto)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def mostrar_documento(self):
        print("\n--- EDITOR DE TEXTO ---")
        actual = self.cabeza
        idx = 1
        while actual:
            print(f"{idx:2d} | {actual.texto}")
            actual = actual.siguiente
            idx += 1
        print("-" * 25)

    def guardar_archivo(self, nombre_archivo):
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            actual = self.cabeza
            while actual:
                f.write(actual.texto + '\n')
                actual = actual.siguiente
        print(f"[P2] Documento guardado en '{nombre_archivo}'.")

    def cargar_archivo(self, nombre_archivo):
        try:
            self.cabeza = None
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    self.agregar_al_final(linea.strip())
            print(f"[P2] Documento cargado exitosamente.")
        except FileNotFoundError:
            print(f"[P2] El archivo '{nombre_archivo}' no fue encontrado.")


# =====================================================================
# PROBLEMA 3: Sistema de Gestión de Polinomios
# =====================================================================

class TerminoPolinomio:
    def __init__(self, coeficiente, exponente):
        self.coeficiente = coeficiente
        self.exponente = exponente
        self.siguiente = None

class Polinomio:
    def __init__(self):
        self.cabeza = None

    def agregar_termino(self, coef, exp):
        if coef == 0:
            return
        nuevo = TerminoPolinomio(coef, exp)
        if not self.cabeza or self.cabeza.exponente < exp:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            return
        
        actual = self.cabeza
        anterior = None
        while actual and actual.exponente > exp:
            anterior = actual
            actual = actual.siguiente
            
        if actual and actual.exponente == exp:
            actual.coeficiente += coef
        else:
            nuevo.siguiente = actual
            if anterior:
                anterior.siguiente = nuevo
            else:
                self.cabeza = nuevo

    def mostrar(self):
        if not self.cabeza:
            return "0"
        resultado = []
        actual = self.cabeza
        first = True
        while actual:
            c = actual.coeficiente
            e = actual.exponente
            if c == 0:
                actual = actual.siguiente
                continue
            signo = " + " if c > 0 and not first else " - " if c < 0 and not first else "" if c > 0 else "-"
            c_val = abs(c)
            term = f"{c_val if c_val != 1 or e == 0 else ''}x^{e}" if e > 1 else (f"{c_val if c_val != 1 else ''}x" if e == 1 else f"{c_val}")
            resultado.append(signo + term)
            first = False
            actual = actual.siguiente
        return "".join(resultado) if resultado else "0"

    def evaluar(self, x):
        total = 0
        actual = self.cabeza
        while actual:
            total += actual.coeficiente * (x ** actual.exponente)
            actual = actual.siguiente
        return total


# =====================================================================
# PROBLEMA 4: Hoja de Cálculo Dispersa
# =====================================================================

class Celda:
    def __init__(self, fila, columna, valor):
        self.fila = fila
        self.columna = columna
        self.valor = valor
        self.siguiente = None

class HojaCalculoDispersa:
    def __init__(self):
        self.cabeza = None

    def insertar_actualizar(self, fila, columna, valor):
        actual = self.cabeza
        while actual:
            if actual.fila == fila and actual.columna == columna:
                actual.valor = valor
                return
            actual = actual.siguiente
        
        nuevo = Celda(fila, columna, valor)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo

    def mostrar_tabular(self, max_filas=3, max_cols=3):
        print("\n--- HOJA DE CÁLCULO DISPERSA ---")
        grid = [[0 for _ in range(max_cols)] for _ in range(max_filas)]
        actual = self.cabeza
        while actual:
            if actual.fila < max_filas and actual.columna < max_cols:
                grid[actual.fila][actual.columna] = actual.valor
            actual = actual.siguiente
            
        for i, fila in enumerate(grid):
            print(f"F{i} | " + " ".join([f"{val:3}" for val in fila]))
        print("-" * 30)


# =====================================================================
# EJECUCIÓN DE PRUEBAS
# =====================================================================
if __name__ == "__main__":
    print("=== PRUEBAS TEMA 6: LISTAS ENLAZADAS ===")
    
    # Prueba Problema 1
    so = ListaProcesos()
    for i in range(1, 11):
        so.agregar_proceso(i, f"Proc_{i}", "listo", i, i * 2)
    so.cambiar_estado(3, "en ejecucion")
    so.mover_al_inicio(5)
    so.mostrar_procesos()
    
    # Prueba Problema 2
    editor = EditorTexto()
    editor.insertar_linea(1, "Primera línea de prueba")
    editor.insertar_linea(2, "Segunda línea añadida")
    editor.mostrar_documento()
    
    # Prueba Problema 3
    p1 = Polinomio()
    p1.agregar_termino(3, 2)
    p1.agregar_termino(5, 0)
    print(f"Polinomio P(x) = {p1.mostrar()}")
    print(f"Evaluado en x=2: {p1.evaluar(2)}")
    
    # Prueba Problema 4
    hoja = HojaCalculoDispersa()
    hoja.insertar_actualizar(0, 1, 50)
    hoja.insertar_actualizar(2, 2, 120)
    hoja.mostrar_tabular(3, 3)
    