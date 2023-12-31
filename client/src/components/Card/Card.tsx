import React from 'react';
import './Card.css';
import LazyImage from '../LazyImage/LazyImage';
import DroppedLabel from '../DroppedLabel/DroppedLabel';
import { BASE_URL } from '../../constants';

// Interface for the Props for the Button
interface CustomCardProps {
    cardText: string;
    imageSrc: string;
    linkSrc: string;
    extraInfo: string;
    openModal: any;
    openQuickLinksModal: any;
    // 12-06-19: New prop for indicating a drop-out
    running: boolean;
    dropOutDate: string;
}

// Interface for the State for the Button
interface CustomCardState {
    positiveProportion: number;
    neutralProportion: number;
    negativeProportion: number;
    isLoaded: boolean;
}

class CustomCard extends React.Component<CustomCardProps, CustomCardState> {
    constructor(props){
        super(props);
        this.state={positiveProportion: 20, negativeProportion:40, neutralProportion: 30, isLoaded:false};
    }

    linkStyle = {
        color: 'white',
        fontSize: '14px'
    };

    componentDidMount() {
        /*fetch(`http://127.0.0.1:5000/`)
        .then(res => {
            console.log('res = ' + JSON.stringify(res.body));
            return res.json();
        })
        .then(
            (result) => {
                console.log('result = ' + JSON.stringify(result));
            },
            (error) => {
                console.log('error = ' + error);
            }
        )*/

        fetch(`${BASE_URL}/get_latest_sentiments/`+ this.props.cardText)
        .then(res => {
            console.log('res = ' + JSON.stringify(res));
            return res.json();
        })
        .then(
            (result) => {
                console.log('result = ' + JSON.stringify(result));
                this.setState({
                    isLoaded: true,
                    positiveProportion: result['positive_sentiment_percent'] ,
                    neutralProportion: result['neutral_sentiment_percent'] ,
                    negativeProportion: result['negative_sentiment_percent'] 
                });
            },
            // Note: it's important to handle errors here
            // instead of a catch() block so that we don't swallow
            // exceptions from actual bugs in components.
            (error) => {
                console.log('error = ' + error);
                this.setState({
                    isLoaded: false,
                    positiveProportion: 0,
                    neutralProportion: 0,
                    negativeProportion: 100
                });
            }
        )
    }

    render() {
        return(
        <div className={"card"}>
            <h3 className={"title"}>{this.props.cardText}</h3>
            <LazyImage imageSrc={this.props.imageSrc}
            height={150}
            width={150}
            linkSrc={this.props.linkSrc}
            linkSrcExtraInfo={this.props.extraInfo}
            linkStyleClass={this.linkStyle}/>

            {this.props.running && <div className={"bar"}>
                <div className={"emptybar"}></div>
                <div className={"filledbar"} style={{background: 'linear-gradient(90deg, rgb(111,191,144, 0.7) 0%, rgb(111,191,144,0.7) ' + (this.state.positiveProportion/2.0) + '%, rgb(111,183,191,0.7) ' + this.state.positiveProportion + '%, rgb(111,183,191,0.7) ' + (this.state.positiveProportion+this.state.neutralProportion/4)+'%, rgb(111,183,191,0.7)' + (this.state.positiveProportion+(3*this.state.neutralProportion/4))+ '%, rgb(191,119,111,0.7)' + (this.state.positiveProportion + this.state.neutralProportion) + '%, rgb(191,119,111,0.7) 100%)'}}></div>
            </div>}

            {!this.props.running && <div className={"droppedOutLabel"}>
                <DroppedLabel dropOutDate={this.props.dropOutDate}/>
            </div>}

            <div className={"circleLocker"}>
                <div className={"circle"} style={{backgroundColor: '#6FBF90'}}>
                    {this.state.positiveProportion}%
                </div>
                <div className={"circle"} style={{backgroundColor: '#6FB7BF'}}>
                    {this.state.neutralProportion}%
                </div>
                <div className={"circle"} style={{backgroundColor: '#BF776F'}}>
                    {this.state.negativeProportion}%
                </div>
            </div>
            <div className={"cardButtonLocker"}>
                <button className={"tweetInfoButton"} onClick={this.props.openModal}>
                    Tweets Info
                </button>
                <button className={"tweetInfoButton"} onClick={this.props.openQuickLinksModal}>
                    Quick Links
                </button>
            </div>
        </div>
        );
    }
}

export default CustomCard;