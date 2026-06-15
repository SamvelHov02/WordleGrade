import '../style/KeyboardRow.css';

function KeyboardRow({values, colors, setinput}){
    const changeInput = (char) => {
        if (char !== 'DELETE' && char !== 'ENTER'){
            setinput(prev => prev + char);
        } else if (char === 'DELETE'){
            setinput(prev => prev.slice(0, -1))
        }
    }

    return(
        <div className='keyboard-row'>
            {Array.from(values, (c, i) => ( 
                <button key={c} className='keyboard-key' data-key={c} data-color={colors?.c ?? ''} onClick={() => changeInput(c)} > 
                    {c}
                </button>
                ))}
        </div>
    );
}

export default KeyboardRow;