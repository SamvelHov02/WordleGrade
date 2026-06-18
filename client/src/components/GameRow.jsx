import '../style/GameRow.css';
import Letter from './Letter';


function GameRow({word, pattern}){
    return (
        <div className='game-row'>
            { Array.from({ length : 5 }, (_, i) => { 
                const letter = word?.[i] ?? '';
                const color  = pattern?.[i] ||  '';
                // Update to include a data-color for pattern
                return <Letter letter={letter} color={color} />
            })}
        </div>
    );
}

export default GameRow;
