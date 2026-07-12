let submit = document.getElementById('login-form');

submit.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data  = Object.fromEntries(formData.entries());

    const resp = await fetch('http://localhost:8000/api/login', {
        method : 'POST',
        headers : {'Content-Type' : 'application/json' },
        body : JSON.stringify(data)
    });

    if (!resp.ok){
        console.log("Gets here");
        // Remove existing alerts.
        const rootElement = document.querySelector('.root');
        rootElement.querySelector('.alert')?.remove();
        
        // Add alert Node
        const alertElement = document.createElement('div');
        alertElement.className = 'alert';
        alertElement.textContent = 'Username or password was incorrect';
        rootElement.appendChild(alertElement);
        
        // Remove after a short period of time 
        setTimeout(() => {
            rootElement.removeChild(alertElement)
        }, 2000);
        return;
    } 

    const respBody = await resp.json();
    localStorage.setItem('token', respBody.token);
    window.location.href = "choose_metric.html";
});