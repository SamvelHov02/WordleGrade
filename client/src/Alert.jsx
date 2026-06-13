import './Alert.css';
import { useState } from 'react';

function Alert({ message }){
    return (
        <>
            {message && <div className='alert'>{message}</div>}
        </>
    );
}

export default Alert;