import '../style/GameRow.css';
import Letter from './Letter';


function GameRow({word, pattern, win, shake, flip, onShakeEnd, onFlipEnd}){
    const className = `game-row ${shake ? 'shake' : ''} ${win ? 'win' : ''} ${flip ? 'flip' : ''}` 

    return (
        <div 
            className={className} 
            onAnimationEnd={onShakeEnd}
        > 
            { Array.from({ length : 5 }, (_, i) => { 
                const letter = word?.[i] ?? '';
                const color  = pattern?.[i] ||  '';
                // Update to include a data-color for pattern
                return <Letter letter={letter} color={color} win={win} delay={`${i * 100}ms`} flip={flip} onFlipEnd={onFlipEnd}/>   
            })}
        </div>
    );
}

export default GameRow;
