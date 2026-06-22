import '../style/Game.css';
import GameRow from './GameRow';

function Game({ guesses, input, patterns, winRow, shakeRow, onShakeEnd }){
    return (
        <div className='game-container'>
            {guesses.map((guess, i) => {
                const currRow = guess === null && guesses[i - 1] !== null;
                const word = guess ?? (currRow ? input : '');

                return (
                    <GameRow key={i} 
                        word={word} 
                        pattern={patterns[i]} 
                        win={winRow === i}
                        shake={shakeRow === i}
                        onShakeEnd={onShakeEnd}
                    />
                )
            })}
        </div>
    );
}

export default Game;