import '../style/Keyboard.css';
import KeyboardRow from './KeyboardRow';

function Keyboard({ characters, setinput }){
    const row1 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'];
    const row2 = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'];
    const row3 = ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'DELETE'];
    const keyboard = [row1, row2, row3];

    console.log(keyboard);
    return (
        <div className='Keyboard'>
            {Array.from({ length : 3}, (_, i) => (
                <KeyboardRow key={i + 1} values={keyboard[i]} colors={characters} setinput={setinput}/>
            ))}

        </div>
    );
}

export default Keyboard;