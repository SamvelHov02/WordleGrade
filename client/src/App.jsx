import { useState, useEffect } from 'react'
import './App.css'
import Game from './Game';
import Keyboard from './Keyboard';
import Alert from './Alert';

function App() {
  // initialize an Object with each letter set to white 
  const initChars = Object.fromEntries(
    Array.from({ length : 26 }, (_, i) => [String.fromCharCode(65 + i), 'white'])
  );

  const [count, setCount] = useState(0);
  const [characters, setCharacters] = useState(initChars);
  const [guesses, setGuesses] = useState(new Array(6).fill(null));
  const [input, setInput] = useState('');
  const [wordList, setWordList] = useState([]);
  const [alertText, setAlertText] = useState('');

  const addGuess = (newGuess) => {
    setGuesses(prev => {
      const nextEmpty = prev.findIndex(g => g === null);
      if (nextEmpty === -1) return prev;
      const updated = [...prev];
      updated[nextEmpty] = newGuess;
      return updated;
    })
  }

  const inWordList = (word) => {
    word = word.toLowerCase();
    const index = wordList.indexOf(word);
    console.log(index);
    return index > -1 
  }

  // Fetches the word list 
  useEffect(() => {
    fetch('static/words.json')
      .then(res => res.json())
      .then(data => setWordList(data.words))
  }, []);

  useEffect(() => {
    const handleKeyUp = (e) => {
      console.log(e.key);
      if (e.key === 'Enter'){
        // Submit the guess
        if (input.length === 5 && inWordList(input)) {
          addGuess(input)
          setInput('')
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
  }, [input]);


  return (
    <>
      <section className="Main-Area">
        <h1> Samvel's Wordle</h1>
        <Game guesses={guesses} input={input} />
        <Alert message={alertText} />
        <Keyboard characters={characters} setinput={setInput}/>
      </section>
    </>
  );
}

export default App
