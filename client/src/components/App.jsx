import { useState, useEffect } from 'react';
import '../style/App.css';
import Game from './Game';
import Keyboard from './Keyboard';
import Alert from './Alert';
import { updateCharcters, addElement, gameOver } from '../utils/App.js';

function App() {
  // initialize an Object with each letter set to white 
  const [characters, setCharacters] = useState(() => 
    Object.fromEntries(
      Array.from({ length : 26 }, (_, i) => [String.fromCharCode(65 + i), 'white'])
    )
  );
  const [guesses, setGuesses] = useState(new Array(6).fill(null));
  const [patterns, setPatterns] = useState(new Array(6).fill(null));
  const [input, setInput] = useState('');
  const [wordList, setWordList] = useState([]);
  const [alertText, setAlertText] = useState('');

  const over = gameOver(guesses, patterns);

  const inWordList = (word) => {
    word = word.toLowerCase();
    const index = wordList.indexOf(word);
    return index > -1 
  }

  // Fetches the word list 
  useEffect(() => {
    fetch('static/words.json')
      .then(res => res.json())
      .then(data => setWordList(data.words))
  }, []);

  useEffect(() => {
    if (over) {
      const handleGameOver = async () => {
        const res = await fetch('/api/grade', {
          method : 'POST',
          headers : {'Content-Type' : 'application/json'},
          body : JSON.stringify({game : guesses.filter(e => e !== null), metric : 'expected'})
        })

        const data = await res.json();
        const newAlert = over + `, performance grade : ${data.grade}`;
        setAlertText(newAlert);
        setTimeout(() => setAlertText(''), 2000);
      }

      handleGameOver();
      return;
    };

    const handleKeyUp = async (e) => {
      if (e.key === 'Enter'){
        if (input.length === 5 && inWordList(input)) {
          const oldInput = input;
          const res = await fetch(`/api/pattern?guess=${oldInput}`);
          const data = await res.json(); 
          const pattern = data.pattern;

          const newGuesses = addElement(oldInput, guesses);
          const newPatterns = addElement(pattern, patterns);
          
          setInput('');
          setGuesses(newGuesses);
          setCharacters(prev => updateCharcters(oldInput, pattern, prev));
          setPatterns(newPatterns);
          // setAlertText(gameOver(newGuesses, newPatterns))

          // Play the animations
        } else if (input.length === 5 && !inWordList(input)){
          // Play animations
          // Add some animation class and remove after it finishes.
          setAlertText('Not in Word List');
          setTimeout(() => setAlertText(''), 2000);
        } else if (!inWordList(input)){
          setAlertText('Not Enough Letters');
          setTimeout(() => setAlertText(''), 2000);
        }
      } else if (e.key === 'Backspace'){
        setInput(prev => prev.slice(0, -1));
      } else if (input.length < 5 && e.key.match(/^[a-zA-Z]$/)){
        setInput(prev => prev + e.key.toUpperCase())
      }
    }

    window.addEventListener('keyup', handleKeyUp);
    return () => window.removeEventListener('keyup', handleKeyUp)
  }, [input, over]);


  return (
    <>
      <section className="Main-Area">
        <h1> Samvel's Wordle</h1>
        <Game guesses={guesses} input={input} patterns={patterns} />
        <Alert message={alertText} />
        <Keyboard characters={characters} setinput={setInput}/>
      </section>
    </>
  );
}

export default App
