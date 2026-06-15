import '../style/Letter.css';

function Letter({letter, id}){
    return (
        <span className="row-letter" >
            {letter}
        </span>
    );
}

export default Letter;