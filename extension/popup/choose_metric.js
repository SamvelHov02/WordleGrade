const checkAuth = async () => {
    const token = localStorage.getItem('token');

    if (!token){
        console.log("No token found");
        return null;
    }

    try{
        const resp = await fetch('http://localhost:8000/api/me', {
            headers : {'Authorization' : `Bearer ${token}`}
        });
        
        // Token might be out of date
        if (!resp.ok){
            console.log("Token out of date");
            localStorage.removeItem('token');
            return null;
        }

        return await resp.json();
    }
    catch (err){
        console.error("Auth check failed:", err);
        return null;
    }
}

const initPage = async () => {
    const user = await checkAuth();

    if (user) showLoggedInHeader(user);
}


const showLoggedInHeader = (user) => {
    console.log("User is logged in");
    // Remove default header children
    const rootElement = document.querySelector('.header');
    const elementsToRemove = document.querySelectorAll('.header-icon');
    elementsToRemove.forEach((el) => rootElement.removeChild(el));

    // Append new nodes
    const profileElement = document.createElement('img');
    profileElement.src = "assets/user.svg";
    profileElement.alt = "Profile";
    profileElement.width = "32";
    profileElement.height = "32"
    rootElement.appendChild(profileElement);
}

const changeMetric = (clicked) => {
    const prevMetric = sessionStorage.getItem('metric');
    if (clicked === prevMetric) return;
    
    const prevNode = document.getElementById(prevMetric);
    let newMetric = null;    
    let newNode = null;

    if (prevMetric === 'expected'){
        newMetric = 'actual';
        newNode = document.getElementById(newMetric);
    } else{
        newMetric = 'expected';
        newNode = document.getElementById(newMetric);
    }

    // Update the states
    sessionStorage.setItem('metric', newMetric);
    prevNode.dataset.state = "inactive"
    newNode.dataset.state = "active";
}

// Add eventListeners
const headerElements = document.querySelectorAll('.header-icon');
headerElements.forEach((el) => {
    const clickedElement = el.id;
    el.addEventListener("click", () => {
        // Go to Clicked page
        window.location.href = `${clickedElement}.html`;
    });
    el.addEventListener("contextmenu", (e) => {
        e.preventDefault();
        e.stopPropagation();
    });
});

const metricElements = document.querySelectorAll('.metric');
metricElements.forEach((el) => {
    const clickedMetric = el.id;
    el.addEventListener("click", () => changeMetric(clickedMetric));
    el.addEventListener("contextmenu", (e) => {
        e.preventDefault();
        e.stopPropagation();
    });
})

initPage();