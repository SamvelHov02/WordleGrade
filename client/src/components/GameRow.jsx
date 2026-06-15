import '../style/GameRow.css';
import Letter from './Letter';


function GameRow({word}){
    return (
        <div className='game-row'>
            { Array.from({ length : 5 }, (_, i) => { 
                const letter = word?.[i] ?? '';
                return <Letter letter={letter} />
            })}
        </div>
    );
}

export default GameRow;
