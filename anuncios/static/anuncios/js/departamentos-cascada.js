/**
 * Script para cargar departamentos dinámicamente según la dirección seleccionada
 */

document.addEventListener('DOMContentLoaded', function() {
    const direccionSelect = document.getElementById('id_iddireccion');
    const departamentoSelect = document.getElementById('id_iddepartamento');

    if (!direccionSelect || !departamentoSelect) {
        console.warn('Elementos de dirección o departamento no encontrados');
        return;
    }

    // Evento cuando cambia la dirección
    direccionSelect.addEventListener('change', function() {
        const iddireccion = this.value;

        // Limpiar opciones previas
        departamentoSelect.innerHTML = '<option value="">-- Selecciona un departamento --</option>';

        if (!iddireccion) {
            departamentoSelect.disabled = true;
            return;
        }

        // Hacer petición AJAX
        fetch(`/api/departamentos-por-direccion/?iddireccion=${iddireccion}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                if (data.departamentos && data.departamentos.length > 0) {
                    // Agregar las opciones nuevas
                    data.departamentos.forEach(dept => {
                        const option = document.createElement('option');
                        option.value = dept.iddepartamento;
                        option.textContent = dept.departamento;
                        departamentoSelect.appendChild(option);
                    });
                    departamentoSelect.disabled = false;

                    // Si hay un valor guardado anteriormente, seleccionarlo
                    const savedValue = departamentoSelect.dataset.savedValue;
                    if (savedValue) {
                        departamentoSelect.value = savedValue;
                        delete departamentoSelect.dataset.savedValue;
                    }
                } else {
                    departamentoSelect.innerHTML = '<option value="">-- No hay departamentos disponibles --</option>';
                    departamentoSelect.disabled = true;
                }
            })
            .catch(error => {
                console.error('Error al cargar departamentos:', error);
                departamentoSelect.innerHTML = '<option value="">-- Error al cargar departamentos --</option>';
                departamentoSelect.disabled = true;
            });
    });

    // Si ya hay una dirección seleccionada al cargar la página, cargar los departamentos
    if (direccionSelect.value) {
        // Guardar el valor actual del departamento antes de cambiar las opciones
        const currentDeptValue = departamentoSelect.value;
        if (currentDeptValue) {
            departamentoSelect.dataset.savedValue = currentDeptValue;
        }
        
        // Disparar el evento change para cargar los departamentos
        direccionSelect.dispatchEvent(new Event('change'));
    }
});
