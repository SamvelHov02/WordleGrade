import '../style/Letter.css';

function Letter({letter, id, color, win, delay}){
    return (
        <span className="row-letter" data-color={color} > 
            {letter}
        </span>
    );
}

export default Letter;