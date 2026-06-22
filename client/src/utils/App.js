/**
 * @param {string} guess - The guess submited 
 * @param {string} pattern - The pattern produced by the guess
 * @param {Object} characters - An object with mapping for a letter to color
 */
export const updateCharcters = (guess, pattern, characters) => {
    const newCharacters = {...characters};
    for (let i = 0; i < guess.length; i++){
        const char  = guess[i];
        const color = pattern[i];
        const prevColor = characters.char;
        
        switch (color){
            case 'green':
                newCharacters[char] = color;
                break;
            case 'yellow':
                if (characters.char !== 'green'){
                    newCharacters[char] = 'yellow';
                }
                break;
            default:
                if (prevColor !== 'green' && prevColor !== 'yellow'){
                    newCharacters[char] = 'black';
                } 
                break;
        }
    } 

    return newCharacters;
}


/**
 * 
 * @param {string} guess - The guess to add to the list 
 * @param {Array} list - The list of guesses
 * 
 * @return {Array} - Updated list of guesses 
 */
export const addElement = (el, list) => {
    const nextEmpty = list.findIndex(g => g === null);
    if (nextEmpty === -1) return list;
    const updated = [...list];
    updated[nextEmpty] = el;
    return updated;
}

/**
 * 
 * @param {Array} guesses - The guesses player has made
 * @param {Array} patterns -  The patterns the guesses have produced
 * @returns {String} - ENUM like return based on the game state
 */
export const gameOver = (guesses, patterns) => {
    // If first render
    if (guesses.every(g => g === null)) return '';

    // Find the last pattern    
    const pattern = patterns.findLast(g => g !== null);
    const elements = Object.values(pattern);

    if (elements.every(g => g === 'green')){
        return 'Victory';
    }

    if (guesses.every(g => g !== null)) {
        return 'Defeat!';        
    } else {
        return '';
    }
}