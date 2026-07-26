browser.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.type === "GRADE_GAME"){
        console.log("Gets to the start of grading");
        const game = msg.game;
        const res = grade(game).then(res => sendResponse(res));
        return true;
    }
});


const removeInvalidWords = (words, guessObj) => {
    const guess    = guessObj.guess.toLowerCase();
    // getPattern emits G/Y/B, so normalise the observed pattern to match.
    const observed = guessObj.pattern.toUpperCase();

    // A word is still possible iff guessing `guess` against it as the target
    // would reproduce the exact pattern we actually saw.
    return words.filter(w => getPattern(guess, w.toLowerCase()) === observed);
}

const getPattern = (guess, target) => {
    guess  = guess.split("");
    target = target.split("");
    const pattern = ['-', '-', '-', '-', '-'];

    // Pass 1: greens. Consume matched target letters so they can't be reused as yellow.
    guess.forEach((char, i) => {
        if (char === target[i]) {
            pattern[i] = 'G';
            target[i] = null;      // mark as used up
        }
    });

    // Pass 2: yellows / greys on the remaining tiles.
    // The number of yellow tiles for one character shouldn't exceed the number in target.
    // E.g. target : CREST and guess : EERIE only the first E tile should be yellow.
    guess.forEach((char, i) => {
        if (pattern[i] === 'G') return;          // already green
        const j = target.indexOf(char);          // an unused matching letter left?
        if (j !== -1) {
            pattern[i] = 'Y';
            target[j] = null;                     // consume it
        } else {
            pattern[i] = 'B';
        }
    });

    return pattern.join("");  // e.g. "GBYBB" — a string, good as a bucket key
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


const grade = (game) => {
    return fetch('valid-wordle-words.json')
        .then(res => res.json())
        .then(validWords => {
            let gradeAcc = 0;
            game.forEach((g, i) => {
                // Skip i === 0: the first guess has no prior information to be
                // graded against, and running optimalGuess on the full ~13k word
                // list is an O(N^2) computation we'd only throw away.
                if (i > 0) {
                    const optimal = optimalGuess(validWords);
                    const optimalWord = optimal.ordered[0];
                    const optimalGain = optimal.informationGains[optimalWord];

                    // Compute the actual guess's IG directly — it may not be in the
                    // candidate set, since default Wordle allows inconsistent guesses.
                    const guessGain = informationGain(validWords, g.guess.toLowerCase());

                    // If no information remains to be gained (e.g. one candidate left),
                    // the guess can't do better than optimal → treat as a perfect ratio.
                    const ratio = optimalGain > 0 ? Math.min(1, guessGain / optimalGain) : 1;
                    gradeAcc += ratio;
                }

                // Narrow the candidate set using this guess's feedback for the next round.
                validWords = removeInvalidWords(validWords, g);
            });

            console.log("Gets to the end of game");

            // Guess 0 isn't graded, so only game.length - 1 guesses contribute.
            const gradedCount = game.length - 1;
            gradeAcc = gradedCount > 0 ? gradeAcc / gradedCount : 1;

            let charGrade;
            if (gradeAcc >= 0.9) charGrade = 'A';
            else if (gradeAcc >= 0.75) charGrade = 'B';
            else if (gradeAcc >= 0.6) charGrade = 'C';
            else if (gradeAcc >= 0.45) charGrade = 'D';
            else charGrade = 'F';

            return charGrade;
        });
}