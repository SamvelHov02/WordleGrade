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

// Note : Maybe change to Object {1 : {word : crane, pattern : gbygb}}
const game = [];

const callback = async (mutations) => {
    console.log("Get's to the callback");
    // console.log(`The game is ${game} : check 1`);
    const index = game.length;
    const rowElement = document.querySelector(`[aria-label="Row ${index + 1}"]`);   
    // console.log(`The selected row is ${rowElement}`);
    const tiles = rowElement.querySelectorAll('[class^=Tile-module_tile_]');

    let guess = "";
    let pattern = "";
    let submittedTags = ["correct", "absent", "present"];
    let submitted = true;
    console.log(tiles);

    for (const tile of tiles){
      // Need to check that all children have a value since mutationObserver callback runs even if only one letter is entered
      if (tile.innerText){ 
        guess += tile.innerText;
        let dataState = tile.getAttribute('data-state');

        switch (dataState) {
          case "correct":
            pattern += "g";
            break;
          case "absent":
            pattern += "b";
            break;
          case "present":
            pattern += "y";
            break;
          default:
            return;
        }

        submitted = submitted && submittedTags.includes(dataState);
      } else {
        return;
      }
    }

    // Append guess only after submittion
    if (submitted){
      game.push({ guess, pattern });
      console.log(`The game thus far is ${game}`);
    } else {
      return;
    }

    let grade;

    if (pattern.split("").every(l => l==='g')){
        console.log(`The game was won with that guess, ${guess} : good job`);
        const metric = sessionStorage.getItem('metric');
        grade = await browser.runtime.sendMessage({
          type : "GRADE_GAME",
          game : game,
        });
    } else if (game.length === 6) {
      // Game was lost — all six guesses used and none solved it. Grade what was played.
      console.log(`The game was lost :(`);
      const metric = sessionStorage.getItem('metric');
      grade = await browser.runtime.sendMessage({
        type : "GRADE_GAME",
        game : game,
      });
  }

    // Only show a toast once the game is over and we have a grade back.
    if (grade){
      const rootElement = document.querySelector('.ToastContainer-module_toastContainer__SIgMB');
      const innerElement = rootElement.querySelector('.ToastContainer-module_toaster__TYGMD');
      const alertMessage = document.createElement('div');
      alertMessage.className = 'Toast-module_toast__iiVsN';
      alertMessage.innerText = `Performance grade : ${grade}`;
      innerElement.appendChild(alertMessage);

      setTimeout(() => {
        alertMessage.remove();
      }, 2000);
    }
}

console.log("Starts observing!!");
const mutation = new MutationObserver(callback);

(async () => {
  const targetNode = await waitFor('[class^=Board-module_board_]');
  console.log(`Observing on the node ${targetNode}`);
  mutation.observe(targetNode, config);
})()
