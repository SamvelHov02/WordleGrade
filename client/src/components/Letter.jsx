import '../style/Letter.css';

function Letter({letter, id, color, win, delay, flip, onFlipEnd}){
    const colors = {
        green : '#6aaa64',
        yellow : '#c9b458',
        black : '#787c7e' 
    }
    return (
        <span 
            className="row-letter" 
            data-color={color} 
            style={win || flip ? {animationDelay : delay, '--target-color' : colors[color]} : undefined}
            onAnimationEnd={onFlipEnd}
            > 
            {letter}
        </span>
    );
}

export default Letter;