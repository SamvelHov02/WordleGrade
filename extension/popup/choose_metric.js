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