
import './singleTimeItem.css'

import { useMemo } from 'react';

const SingleTimeItem = (props) => {
    const twoDigits = useMemo(() => {
        return props.number < 10 ? "0" + props.number.toString() : props.number.toString()
    },[props.number]);
    return (
        <div className="single-count-item">
            <div className="upper-number-box">
                {twoDigits}
            </div>
            <div className="lower-type-box">
                {props.type}
            </div>
        </div>
    )
}

export default SingleTimeItem;