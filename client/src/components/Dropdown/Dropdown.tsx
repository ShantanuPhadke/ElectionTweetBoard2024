import React from 'react';
import './Dropdown.scss';

// Interface for the Props for the Button
interface DropdownProps {
    title: string;
    options: any;
    defaultOption: string;
    parentChangeFunction: any;
}

// Interface for the State for the Button
interface DropdownState {
    isOpen: boolean;
    labelItem: string;
    democratPositiveList: any;
}

class Dropdown extends React.Component<DropdownProps, DropdownState> {
    constructor(props){
        super(props);
        this.state = {isOpen: false, labelItem: this.props.defaultOption, democratPositiveList:[]};
        // binding functions
        this.toggleDropdown = this.toggleDropdown.bind(this);
        this.renderDataDropDown = this.renderDataDropDown.bind(this);
        this.chooseItem = this.chooseItem.bind(this);
    }

    chooseItem(label){
        this.setState({labelItem: label, isOpen: false});
        this.props.parentChangeFunction(label);
    }

    toggleDropdown(){
        this.setState({isOpen: !this.state.isOpen});
        console.log("In toggle dropdown! New value of isOpen: " + this.state.isOpen);
    }

    /*componentDidMount() {
        fetch('https://www.electiontweetboard.com/get_sorted_ordering/Democrats/positive_percent')
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({democratPositiveList: result['order']});
                }
            )
    }*/

    renderDataDropDown(item, index){
        const {value, label} = {value: index, label: item};
        return (
            <li
                key={index}
                value={value}
                onClick={() => this.chooseItem(label)}
            >
                {label}
            </li>
        );
    }

    render() {

            return (
            <div className={"dropdown {this.state.isOpen ? 'open' : ''}"}>
                <span className="dropdownLabel">Ordered By</span>
                {this.state.isOpen && <ul className="dropdown-menu">
                    {this.props.options.map(this.renderDataDropDown)}
                </ul>}
                <button className="dropdown-toggle" type="button" onClick={this.toggleDropdown}>
                    {this.state.labelItem}
                <span className="caret"></span>
                </button>
            </div>
        );
    }
}

export default Dropdown;