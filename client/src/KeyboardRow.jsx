import './KeyboardRow.css';

function KeyboardRow({values, colors}){
    return(
        <div className='keyboard-row'>
            {Array.from(values, (c, i) => ( 
                <button key={c} className='keyboard-key' data-key={c} data-color={colors?.c ?? ''} > 
                    {c}
                </button>
                ))}
        </div>
    );
}

export default KeyboardRow;