import '../style/Letter.css';

function Letter({letter, id, color, win, delay}){
    console.log(`Delay is ${delay}`);
    return (
        <span 
            className="row-letter" 
            data-color={color} 
            style={win ? {animationDelay : delay} : undefined}
            > 
            {letter}
        </span>
    );
}

export default Letter;