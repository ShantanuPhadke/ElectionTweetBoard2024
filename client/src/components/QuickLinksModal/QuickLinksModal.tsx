import React from 'react';
import './QuickLinksModal.css';
import { BASE_URL } from '../../constants';

// Interface for the Props for the QuickLinksModal
interface QuickLinksModalProps {
    closeFunction: any;
    name: string;
}

// Interface for the State for the QuickLinksModal
interface QuickLinksModalState {
    links: any;
    error: any;
}

class QuickLinksModal extends React.Component<QuickLinksModalProps, QuickLinksModalState>{
    constructor(props) {
        super(props);
        this.state={links:[], error:null};
        this.closeTwice = this.closeTwice.bind(this);
    }

    componentDidMount(){
        fetch(`${BASE_URL}/get_current_links/`+this.props.name)
        .then(res => res.json())
        .then(
            (result) => {
                this.setState({
                    links: result["links"]
                });
            },
            (error) => {
                this.setState({
                    links: ["Error!"],
                    error
                });
            }
        )
    }

    closeTwice = () => {
        this.props.closeFunction();
        this.props.closeFunction();
    }

    render() {
        return (
            <div className="quickLinksModalLocker2">
                <h5 className="quickLinksTitle"> Quick Links for {this.props.name} </h5>
                <div className={"close"} onClick={this.closeTwice}/>
                <div className="quickLinksLocker">
                    {
                        this.state.links.map(function(link){
                            if(link[0][0].substring(0,8) === 'https://'){
                                return <li key={link} className={"quickLink"}><a className={"quickLink"} href={link[0][0]} target={'_blank'}>{link[0][1]}</a></li>;
                            }
                            return null;
                        })
                    }
                </div>
                
            </div>
        );
    }
}

export default QuickLinksModal;