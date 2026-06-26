const config = {
    attributes : true,
    subtree : true,
    childList : false
}

const game = new Array(6).fill(null);

const callback = (mutations) => {
    const index = game.findIndex(e => e === null);
    const rowElement = document.querySelector(`[aria-label="Row ${index + 1}"]`);   
}