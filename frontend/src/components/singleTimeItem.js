
import './singleTimeItem.css'

const SingleTimeItem = (props) => {
    return (
        <div className="single-count-item">
            <div className="upper-number-box">
                {props.number}
            </div>
            <div className="lower-type-box">
                {props.type}
            </div>
        </div>
    )
}

export default SingleTimeItem;