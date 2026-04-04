(function () {
    const btnbaja=document.querySelectorAll(".btnbaja");

    btnbaja.forEach(btn => {
        btn.addEventListener('click', (e) => { 
            const confirmacion = confirm('¿Desea dar de baja el registro?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
})();