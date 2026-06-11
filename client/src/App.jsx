import { useState, useEffect } from 'react'
import './App.css'
import Game from './Game';
import Keyboard from './Keyboard';

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
    const index = wordList.indexOf(word)
    return index > -1 
  }

  // Fetches the word list 
  useEffect(() => {
    fetch('/word.json')
      .then(res => res.json())
      .then(data => setWordList(data))
  });

  useEffect(() => {
    const handleKeyUp = (e) => {
      console.log(e.key);
      if (e.key === 'Enter'){
        // Submit the guess
        if (input.length === 5 && inWordList(input)) {
          addGuess(input)
          setInput('')
        } else if (!inWordList(input)){
          // Play animations
          // Add some animation class and remove after it finishes.
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
        <Keyboard characters={characters} setinput={setInput}/>
      </section>
    </>
  );
}

export default App
