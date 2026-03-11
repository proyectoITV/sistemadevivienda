/**
 * Script para generar nombre completo automáticamente
 * A partir de: Apellido Paterno + Apellido Materno + Nombre
 */

document.addEventListener('DOMContentLoaded', function() {
    const apellidoPaternoInput = document.getElementById('id_apellido_paterno');
    const apellidoMaternoInput = document.getElementById('id_apellido_materno');
    const nombreInput = document.getElementById('id_nombre');

    // Validar que los inputs existen
    if (!apellidoPaternoInput || !nombreInput) {
        console.warn('Elementos de nombre no encontrados');
        return;
    }

    function generarNombreCompleto() {
        // Obtener valores y limpiarlos
        const apellidoPaterno = (apellidoPaternoInput.value || '').trim();
        const apellidoMaterno = (apellidoMaternoInput ? (apellidoMaternoInput.value || '').trim() : '');
        const nombre = (nombreInput.value || '').trim();

        // Construir nombre completo
        let nombreCompleto = '';
        if (nombre && apellidoPaterno) {
            if (apellidoMaterno) {
                nombreCompleto = `${nombre} ${apellidoPaterno} ${apellidoMaterno}`;
            } else {
                nombreCompleto = `${nombre} ${apellidoPaterno}`;
            }
        }

        // Aquí podrías mostrar la vista previa o hacer algo con el nombre
        console.log('Nombre Completo:', nombreCompleto);

        // Si hay un elemento para mostrar la vista previa, actualizarlo
        const previewElement = document.getElementById('nombre-completo-preview');
        if (previewElement) {
            previewElement.textContent = nombreCompleto || '(se generará automáticamente)';
        }
    }

    // Agregar listeners a todos los campos
    if (apellidoPaternoInput) {
        apellidoPaternoInput.addEventListener('change', generarNombreCompleto);
        apellidoPaternoInput.addEventListener('keyup', generarNombreCompleto);
    }

    if (apellidoMaternoInput) {
        apellidoMaternoInput.addEventListener('change', generarNombreCompleto);
        apellidoMaternoInput.addEventListener('keyup', generarNombreCompleto);
    }

    if (nombreInput) {
        nombreInput.addEventListener('change', generarNombreCompleto);
        nombreInput.addEventListener('keyup', generarNombreCompleto);
    }

    // Generar nombre completo al cargar la página
    generarNombreCompleto();
});
