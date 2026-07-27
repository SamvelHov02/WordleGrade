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
    
    panel.append(title, hint, wordList);
    wrapper.append(tab, panel);
    document.body.appendChild(wrapper);
    
    // TODO : need function that can add Guesses and also render them
    const showStats = (word, rowEl) => {
        // "Unselect" previous words
        wordList.querySelectorAll('.grade-word')
            .forEach((el) => el.classList.remove('selected'));
        rowEl.classList.add('selected');

        // drop-down element with stats info
        // Should have general stats like : # remaining words and the best next guess also
        // should have a div with remaining words
        const dropDown = document.createElement('grade-drop-down');
        const remainingWords

    }

    const addGuess = (word, states) => {
        const row = document.createElement('button');
        row.className = 'grade-word';
        row.type = 'button';

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