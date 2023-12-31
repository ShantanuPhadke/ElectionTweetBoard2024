import React from 'react';
import './Button.css';

// Interface for the Props for the Button
interface CustomButtonProps {
    buttonText: string;
    class: string;
}

// Interface for the State for the Button
interface CustomButtonState {

}

class CustomButton extends React.Component<CustomButtonProps, CustomButtonState> {

    render(){
        return <button className={this.props.class}>
                {this.props.buttonText}
               </button>
    }
}

export default CustomButton;