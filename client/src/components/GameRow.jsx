import '../style/GameRow.css';
import Letter from './Letter';


function GameRow({word, pattern, win, shake, onShakeEnd}){
    const className = `game-row ${shake ? 'shake' : ''} ${win ? 'win' : ''}` 

    return (
        <div 
            className={className} 
            onAnimationEnd={onShakeEnd}
        > 
            { Array.from({ length : 5 }, (_, i) => { 
                const letter = word?.[i] ?? '';
                const color  = pattern?.[i] ||  '';
                // Update to include a data-color for pattern
                return <Letter letter={letter} color={color} win={win} delay={`${i * 100}ms`}/>   
            })}
        </div>
    );
}

export default GameRow;
