let submit = document.getElementById('signup-form');

submit.addEventListener('submit', async (e) => {
    e.preventDefault();  
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    const resp = await fetch('http://localhost:8000/api/register', {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(data)
    });
    
    if (!resp.ok) {
        console.log("Registration Failed");
        
        // Remove existing alert
        const rootElement = document.querySelector('.root');
        rootElement.querySelector('.alert')?.remove();

        // Add Alert Node
        const alertElement = document.createElement('div');
        alertElement.textContent = "Username is already taken";
        alertElement.className = 'alert';
        rootElement.appendChild(alertElement);

        // Remove the alert after a while
        setTimeout(() => {
            rootElement.removeChild(alertElement);
        }, 2000);
        return;
    }

    // Succesfull registration should log-in
    const respBody = await resp.json();
<<<<<<< HEAD
    await browser.storage.local.set({'token' : respBody.token});
=======
    localStorage.setItem('token', respBody.token);
>>>>>>> 9d5d82c08b44bbbbd5b6bb189b5f0b6e167d5a52
    window.location.href = "choose_metric.html";
});