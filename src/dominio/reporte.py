class ReporteEmpleados:
    def __init__(self, empleados):
        self.empleados = list(empleados)

    def generar(self):
        return self._formatear(self.empleados, "Reporte general")

    def _formatear(self, empleados, titulo):
        texto = titulo
        if not empleados:
            texto = texto + "\nSin empleados."
        for empleado in empleados:
            if empleado.departamento is None:
                departamento = "Sin departamento"
            else:
                departamento = empleado.departamento.nombre
            texto = texto + f"\n{empleado.id}: {empleado.nombre} | {empleado.correoElectronico} | {departamento}"
        return texto


class ReportePorDepartamento(ReporteEmpleados):
    def __init__(self, departamento):
        super().__init__(departamento.empleados)
        self.departamento = departamento

    def generar(self):
        titulo = f"Departamento: {self.departamento.nombre}"
        return self._formatear(self.empleados, titulo)
