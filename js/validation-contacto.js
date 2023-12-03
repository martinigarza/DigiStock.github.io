//document.addEventListener('DOMContentLoaded', function () {

   // const form = document.querySelector('#form');
    const validarFormulario = (event) => {
        event.preventDefault();
        
        const email = document.querySelector('#exampleFormControlInput1');
        const consulta = document.querySelector('#exampleFormControlTextarea1');
        
        let validation = true;

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if(email.value.trim() === '' || !emailRegex.test(email.value)){
            //alert("El email no puede estar vacío");
            email.classList.add('error');
            const divError = document.querySelector('#error-email');
            divError.textContent = 'Ingrese una dirección de email válida';
            validation = false;
        } else {
            // Elimina la clase de error y el mensaje de error si el campo es válido
            email.classList.remove('error');
            const divError = document.querySelector('#error-email');
            divError.textContent = '';
        }

        if(consulta.value === ''){
            //alert('La consulta no puede estar vacia');
            consulta.classList.add('error');
            const divError = document.querySelector('#error-consulta');
            divError.textContent = 'La consulta no puede estar vacía';
            validation = false;
        }  else {
            // Elimina la clase de error y el mensaje de error si el campo es válido
            consulta.classList.remove('error');
            const divError = document.querySelector('#error-consulta');
            divError.textContent = '';
        }
        if(validation){
            let data = {
                'email': email.value,
                'consulta': consulta.value,
            };
            
            localStorage.setItem('user', JSON.stringify(data)); 
            
        }
    

         else{
            return false;
        }
    }    
    form.addEventListener('submit', validarFormulario);
    
    
    console.log('Accediendo al localStorage');
    let user = JSON.parse(localStorage.getItem('user'));

    if (user) {
        console.log(`email enviado: ${user.email}`);
        console.log(`Consulta enviada: ${user.consulta}`);
    }
//});
