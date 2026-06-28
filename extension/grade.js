const config = {
    attributes : true,
    attributeFilter : ["data-state"],
    subtree : true,
    childList : false
}

const game = new Array(6).fill(null);

const callback = async (mutations) => {
    const index = game.findIndex(e => e === null);
    const rowElement = document.querySelector(`[aria-label="Row ${index + 1}"]`);   

    let guess = "";
    let pattern = true;

    for (const tile of rowElement.children){
      guess += tile.innerText;
      pattern = pattern && tile.getAttribute('data-state') === 'correct';
    }

    game[index] = guess;

    // Send Grading request once 
    if (pattern){
        const res = await fetch('http://localhost:8000/api/grade', {
          method : 'POST',
          headers : {'Content-Type' : 'application/json'},
          body : JSON.stringify({game : game.filter(e => e !== null), metric : 'expected'})
        })

        const data = await res.json();
    
        const rootElement = document.querySelector('.ToastContainer-module_gameToaster_SIgMB');
        const innerElement = rootElement.querySelector('.ToastContainer-module_toaster__TYGMD');
        // add new alert with grade for a short time
        const alertMessage = document.createElement('div');
        alertMessage.className = 'Toast-module_toast__iiVsN';
        alertMessage.innerText = `Performance grade : ${data.grade}`;
        innerElement.appendChild(alertMessage);
  }
}

const mutation = new MutationObserver(callback);

mutation.observe()

