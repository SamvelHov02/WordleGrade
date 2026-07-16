sessionStorage.setItem('metric', 'expected');

const waitFor = (selector) => {
  return new Promise((resolve) => {
    const exists = document.querySelector(selector);
    if (exists) return resolve(exists);

    const obs = new MutationObserver(() => {
      const el = document.querySelector(selector);
      if (el) {obs.disconnect(); resolve(el); }
    });
    obs.observe(document.body, {childList : true, subtree : true});
  });
}

const config = {
    attributes : true,
    attributeFilter : ["data-state"],
    subtree : true,
    childList : false
}

const game = new Array(6).fill(null);

const callback = async (mutations) => {
    console.log("Get's to the callback");
    // console.log(`The game is ${game} : check 1`);
    const index = game.findIndex(e => e === null);
    const rowElement = document.querySelector(`[aria-label="Row ${index + 1}"]`);   
    // console.log(`The selected row is ${rowElement}`);
    const tiles = rowElement.querySelectorAll('[class^=Tile-module_tile_]');

    let guess = "";
    let pattern = true;
    let submittedTags = ["correct", "absent", "present"];
    let submitted = true;

    for (const tile of tiles){
      // Need to check that all children have a value since mutationObserver callback runs even if only one letter is entered
      console.log(`${tile.className}`);
      if (tile.innerText){ 
        console.log(tile.innerText);
        guess += tile.innerText;
        let dataState = tile.getAttribute('data-state');
        console.log(`The data-state is ${dataState}`);
        pattern = pattern &&  dataState === 'correct';
        submitted = submitted && submittedTags.includes(dataState);
      } else {
        return;
      }
    }

    // Append guess only after submittion
    if (submitted){
      game[index] = guess;
      console.log(`The game thus far is ${game}`);
    } else {
      return;
    }

    // Send Grading request once 
    if (pattern){
        console.log(`The game was won with that guess, ${guess} : good job`);
        const metric = sessionStorage.getItem('metric');
        const token=  await browser.storage.local.get('token');
        const res = await fetch('http://localhost:8000/api/grade', {
          method : 'POST',
          headers : {'Content-Type' : 'application/json', 'Authorization' : `Bearer ${token.token}`},
          body : JSON.stringify({game : game.filter(e => e !== null), metric : metric})
        })

        const data = await res.json();
    
        const rootElement = document.querySelector('.ToastContainer-module_toastContainer__SIgMB');
        const innerElement = rootElement.querySelector('.ToastContainer-module_toaster__TYGMD');
        // add new alert with grade for a short time
        const alertMessage = document.createElement('div');
        alertMessage.className = 'Toast-module_toast__iiVsN';
        alertMessage.innerText = `Performance grade : ${data.grade}`;
        innerElement.appendChild(alertMessage);
  }
}

console.log("Starts observing!!");
const mutation = new MutationObserver(callback);

(async () => {
  const targetNode = await waitFor('[class^=Board-module_board_]');
  console.log(`Observing on the node ${targetNode}`);
  mutation.observe(targetNode, config);
})()

