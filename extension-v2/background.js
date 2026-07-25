const validWords = fetch('valid-wordle-words.json').then(r => r.json());

browser.runtime.onMessage.addEventListener((msg, sender, sendResponse) => {
    if (msg.type === "GRADE_GAME"){
        const game = msg.game;
        const target = msg.target;
        const grade = grade(game, target);
        sendResponse(grade);
    }
});


const getPattern = (guess, target) => {
    let pattern = ['-', '-','-','-','-'];
    // Green and Gray trivialy checked
    guess.forEach((char, i) => {
        if (char === target[i]){
            pattern = pattern.subarray(0, i) + 'G' + pattern.substring(i+1);
        } else if (!target.includes(char)){
            pattern = pattern.substring(0, i) + 'B' + pattern.substring(i+1);
        } 

    });

    // Yellow chars more tricky since the number of yellow tiles for one character shouldn't exceed number in target
    // E.g. target : CREST and guess : EERIE only the first E tile should be yellow
    let indicesLeft = pattern.filter(el => el === '-');
    let charsLeft = indicesLeft.map(idx => target[idx]);

    indicesLeft.forEach((idx, i) => {
        if (charsLeft.includes(guess[idx])){
            pattern[idx] = "Y";
            charsLeft[i] = "";
        } else {
            pattern[idx] = "B";
        }
    });

    return pattern;
}

const removeInvalidWords = (words, guess, target) => {
    const pattern = getPattern(guess, target);

    let greenChars = ['-', '-', '-', '-', '-'];
    let greyChars  = [];
    const yellowChars = {};

    pattern.forEach((color, i) => {
        if (color === 'G') {
            greenChars[i] = guess[i];
        } else if (!yellowChars[color] && color === 'B') greyChars.push(guess[i]);
        else {
            if (!yellowChars[color]) {
                yellowChars[color] = {
                    count : 1, 
                };
            } else {
                yellowChars[color].count++
            }
        }
    });

    let remainingWords = [];

    words.forEach((w) => {
        const arrW = w.split("");

        let add = true;
        // Check that green places
        arrW.some((c, i) => {
            if (greyChars.includes(c)) {add = false; return true};
            if (greenChars[i] !== '-' && c !== greenChars[i]) {add = false; return true};
            
            // Yellow Chars check
            if (yellowChars[color] && yellowChars[color].count > 0){
                yellowChars[color].count--;
            } else if (yellowChars[color].count <= 0) {add = false; return true};
        });

        if (add) remainingWords.push(w);
    });

    return remainingWords;
}

const informationGain = (words, guess) => {
    const N = words.length;

    // Treat each remaining word as target and partition into buckets based on produced pattern
    const buckets = {} 

    words.forEach((w) => {
        const pattern = getPattern(guess, w);
        
        const newCount = buckets[pattern] ? buckets[pattern] + 1 : 1;
        
        buckets[pattern] = newCount;
    });

    let S = 0

    // Calculate the expected information gain
    for (const [pat, count] of Object.entries(buckets)){
       S -= count * Math.log2(count);
    }
    
    return Math.log2(N) - (S/N);
}


const optimalGuess = (words) => {
    const wordsIG = {};
    words.forEach((w) => {
        wordsIG[w] = informationGain(words, w);
    });

    // Sort the words by most information gain:
    const sorted = Object.entries(wordsIG).sort((a, b) => b[1] - a[1]);
    const wordsSorted = sorted.map(([word]) => word);

    return {
        ordered : wordsSorted,
        informationGains : wordsIG
    };
}


const grade = (game, target) => {
    let gradeAcc;
    game.forEach((g, i) => {
        const optimal = optimalGuess(validWords);
        validWords = removeInvalidWords(validWords, g, target);
        if (i === 0) return;

        const optimalWord = optimal.ordered[0];
        const guessGain = optimal.informationGains[g];
        const optimalGain = optimal.informationGains[optimalWord];

        gradeAcc += guessGain / optimalGain;

        // Convert Numeric grade to a char grade.
    });

    gradeAcc = gradeAcc / game.length;

    let charGrade;
    if (gradeAcc >= 0.9) charGrade = 'A';
    else if (gradeAcc >= 0.75) charGrade = 'B';
    else if (gradeAcc >= 0.6) charGrade = 'C';
    else if (gradeAcc >= 0.45) charGrade = 'D';
    else charGrade = 'F';

    return {charGrade};
}