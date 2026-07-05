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
const elements = document.querySelectorAll('.metric');
elements.forEach((el) => {
    const clickedMetric = el.id;
    el.addEventListener("click", () => changeMetric(clickedMetric));
    el.addEventListener("contextmenu", (e) => {
        e.preventDefault();
        e.stopPropagation();
    });
})