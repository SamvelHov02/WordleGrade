// This script injects the tab into 

const createTab = () => {
    const wrapper = document.createElement('div');
    wrapper.className = 'grade-wrapper';

    const tab = document.createElement('div');
    tab.className = 'grade-slide-up';
    
    const panel = document.createElement('div');
    panel.className = 'grade-panel';

    const title = document.createElement('p');
    title.className = 'grade-title';
    title.textContent = 'WordleGrade';

    const hint = document.createElement('p');
    hint.className = 'grade-hint';
    hint.textContent = 'Click on a guess to see remaining words and best next word';

    const wordList = document.createElement('div');
    wordList.className = 'grade-wordlist';

    const footer = document.createElement('div');
    footer.className = 'grade-footer';
    
    const redditShare = document.createElement('span');
    redditShare.className = 'grade-share-reddit';
    
    redditShare.addEventListener('click', async () => {
        if (window.stats) {
            // Builds the emoji patterns for each guess
            const patternStrings = window.game.map((g) => {
                let row = "";
                for (const tile of g.tileStates) {
                    switch (tile){
                        case 'correct':
                            row += '🟩';
                            break;
                        case 'present':
                            row += '🟨';
                            break;
                        default:
                            row += '⬛';
                    }
                }
                return row;
            });

            let text = `WordleGrade ${window.stats.length}/6 \n\n14855\n`;

            patternStrings.forEach((p, i) => {
                text += p + ` >!${window.stats[i].guess}!< ${window.stats[i].remainingWords.length} \n`;
            });

            await navigator.clipboard.writeText(text);
        }
    });

    const discordShare = document.createElement('span');
    discordShare.className = 'grade-share-discord';
    discordShare.addEventListener('click', async () => {
        if (window.stats){
            const patternStrings = window.game.map((g) => {
                let row = "";

                for (const tile of g.tileStates){
                    switch (tile){
                        case 'correct':
                            row += '🟩';
                            break;
                        case 'present':
                            row += '🟨';
                            break;
                        default:
                            row += '⬛';
                    }
                }
                return row;
            });

            let text = `WordleGrade ${window.stats.length}/6 \n\n14855\n`;

            patternStrings.forEach((p, i) => {
                text += p + ` ||${window.stats[i].guess}|| ${window.stats[i].remainingWords.length} \n`;
            });

            await navigator.clipboard.writeText(text);
        }
    });

    footer.append(redditShare, discordShare);
    panel.append(title, hint, wordList, footer);
    wrapper.append(tab, panel);
    document.body.appendChild(wrapper);
    
    const dropDown = document.createElement('div');
    dropDown.className = 'grade-drop-down';

    const showStats = (word, rowEl) => {
        // Reset previous dropDown
        dropDown.innerHTML = ""
        // "Unselect" previous words
        wordList.querySelectorAll('.grade-word')
            .forEach((el) => el.classList.remove('selected'));
        rowEl.classList.add('selected');

        // drop-down element with stats info
        // Should have general stats like : # remaining words and the best next guess also
        // should have a div with remaining words

        const head = document.createElement('span');
        head.className = 'drop-down-head';

        const remainingWordsWrap = document.createElement('span');
        remainingWordsWrap.className = 'grade-remaining-words';
        
        const remainingWordsInd = document.createElement('p');
        remainingWordsInd.className = 'indicator-remaining-words';
        remainingWordsInd.textContent = 'REMAINING WORDS';

        const remainingWordsVal = document.createElement('p');
        remainingWordsVal.className = 'value-remaining-words';

        remainingWordsWrap.append(remainingWordsInd, remainingWordsVal);
        
        const optimalNextGuessWrap = document.createElement('span');
        optimalNextGuessWrap.className = 'grade-optimal-next';

        const optimalNextGuessInd = document.createElement('p');
        optimalNextGuessInd.className = 'indicator-optimal-next';
        optimalNextGuessInd.textContent = 'BEST NEXT GUESS';

        const optimalNextGuessVal = document.createElement('p');
        optimalNextGuessVal.className = 'value-optimal-next';

        optimalNextGuessWrap.append(optimalNextGuessInd, optimalNextGuessVal);

        const body = document.createElement('div');
        body.className = 'drop-down-body';

        // Need to give values to the different element, however only after game is finished, listen for message from 
        if (window.stats) {
            const selectedIdx = rowEl.id;
            console.log(`The index selected is ${selectedIdx}`);
            const stat = window.stats[selectedIdx];

            console.log(stat.remainingWords.length);
            remainingWordsVal.textContent = stat.remainingWords.length;
            optimalNextGuessVal.textContent = stat.nextOptimal;
            
            // append each remaining word to the list 
            stat.remainingWords.forEach((w) => {
                const wordEl = document.createElement('span');
                wordEl.className = 'grade-candidate-word';
                wordEl.textContent = w;

                body.appendChild(wordEl);
            });
        } else {
            // Hide information
            remainingWordsVal.textContent = 'n/a';
            optimalNextGuessVal.textContent = 'n/a';
            body.textContent = 'Stats available after game is finsihed';
        }

        head.append(remainingWordsWrap, optimalNextGuessWrap);
        dropDown.append(head, body);

        // The dropdown needs to be appended to the correct place in the panel, i.e. after rowEl
        rowEl.after(dropDown);
    }

    const addGuess = (word, states) => {
        const row = document.createElement('button');
        row.className = 'grade-word';
        row.type = 'button';

        const index = document.querySelectorAll('.grade-word').length;
        row.id = index;
        
        console.log(word);

        [...word].forEach((letter, i) => {
            const tile = document.createElement('span');
            tile.className = 'grade-letter';
            const state = states && states[i];

            if (state === 'correct' || state === 'present') {
                tile.classList.add(state);
            }

            tile.textContent = letter;
            row.appendChild(tile);
        });

        row.addEventListener('click', () => showStats(word, row));
        wordList.appendChild(row);
    }

    return { addGuess };
}

(async () => {
    const { addGuess } = createTab();
    document.addEventListener('myext:new-guess', (e) => {
        console.log("Gets the event");
        console.log(e.detail);
        addGuess(e.detail.guess, e.detail.pattern);
    });
})()