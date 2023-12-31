import React from 'react';
import './DroppedLabel.css';

// Interface for the Props for the Button
interface DroppedLabelProps {
    dropOutDate: string;
}

// Interface for the State for the Button
interface DroppedLabelState {

}

class DroppedLabel extends React.Component<DroppedLabelProps, DroppedLabelState> {

    render() {
        return(
            <div className={"dropped_div"}>
                DROPPED OUT - {this.props.dropOutDate}
            </div>
        );
    }
}

export default DroppedLabel;