import React from 'react';
import { withRouter } from 'react-router-dom';
import politicianReducer from './reducer-politicians';
import { createStore } from 'redux';

import '../../components/Button/Button.css';
import './DefaultDashboardView.css';
import '../../components/Card/Card.css';

import CustomCard from '../../components/Card/Card';
import TweetsModal from '../../components/TweetsModal/TweetsModal';
import QuickLinksModal from '../../components/QuickLinksModal/QuickLinksModal';
import Dropdown from '../../components/Dropdown/Dropdown';

import { BASE_URL } from '../../constants';


interface DefaultDashboardViewProps {
    history: any;
}

interface DefaultDashboardViewState {
    currentParty: string;
    tweetModalShowing: boolean;
    quickLinksModalShowing: boolean;
    modalName: string;
    // New Attribute for the current sorted order
    sortOrder: string;
    // All three democratic orderings (other than default)
    democratPositiveList: any;
    democratNeutralList: any;
    democratNegativeList: any;
    // All three republican orderings (other than default)
    republicanPositiveList: any;
    republicanNeutralList: any;
    republicanNegativeList: any;
}

class DefaultDashboardView extends React.Component<DefaultDashboardViewProps, DefaultDashboardViewState> {
    constructor(props:any){
        super(props);

        let components = window.location.href.split('/');
        let currentPartyVar='DEMOCRATS';
        let currentCandidateVar = 'none';
        let currentQuickLinksModalVisible = false;
        let currentTweetsModalVisible = false;

        if(components[3] === 'democrats') {
            currentPartyVar = 'DEMOCRATS';
        } else if(components[3] === 'republicans') {
            currentPartyVar = 'REPUBLICANS';
        }else{
            this.props.history.push('/democrats');
        }

        if(components.length === 6) {
            currentCandidateVar = components[4].split('%20')[0]+ ' '+components[4].split('%20')[1];
            if(components[5] === 'quick-links-modal'){
                currentQuickLinksModalVisible = true;
            } else if(components[5] === 'tweets-modal'){
                currentTweetsModalVisible = true;
            }
        }

        this.state={
            currentParty: currentPartyVar,
            tweetModalShowing: currentTweetsModalVisible,
            quickLinksModalShowing: currentQuickLinksModalVisible,
            modalName: currentCandidateVar, 
            sortOrder: "Default", 
            democratPositiveList:[], 
            democratNeutralList:[], 
            democratNegativeList:[],
            republicanPositiveList: [],
            republicanNeutralList: [],
            republicanNegativeList: []
        };

        this.republicanMode = this.republicanMode.bind(this);
        this.democratMode = this.democratMode.bind(this);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.openQuickLinksModal = this.openQuickLinksModal.bind(this);
        this.closeQuickLinksModal = this.closeQuickLinksModal.bind(this);
        this.changeSortingOrder = this.changeSortingOrder.bind(this);
        this.disableScrolling = this.disableScrolling.bind(this);
        this.enableScrolling = this.enableScrolling.bind(this);

        
    }

    republicanMode:any = () => {
        this.props.history.push('/republicans');
        console.log("current url: " + window.location.href.split('/'));
        this.setState({currentParty: 'REPUBLICANS'});
    }

    democratMode:any = () => {
        this.props.history.push('/democrats');
        console.log("current url: " + window.location.href.split('/'));
        this.setState({currentParty: 'DEMOCRATS'}); 
    }

    openModal:any = (cardName:string) => {
        if(this.state.currentParty === "DEMOCRATS") {
            this.props.history.push('/democrats/'+cardName+'/tweets-modal');
        }else {
            this.props.history.push('/republicans/'+cardName+'/tweets-modal');
        }
        this.disableScrolling();
        this.setState({tweetModalShowing: true, modalName: cardName});
    }

    closeModal:any = () => {
        if(this.state.currentParty === "DEMOCRATS") {
            this.props.history.push('/democrats');
        }else {
            this.props.history.push('/republicans');
        }
        this.setState({tweetModalShowing: false, modalName: 'none'});
        this.enableScrolling();
    }

    openQuickLinksModal:any = (cardName:string) => {
        if(!this.state.quickLinksModalShowing) {
            if(this.state.currentParty === "DEMOCRATS") {
                this.props.history.push('/democrats/'+cardName+'/quick-links-modal');
            }else {
                this.props.history.push('/republicans/'+cardName+'/quick-links-modal');
            }
            this.setState({quickLinksModalShowing: true, modalName: cardName});
            this.disableScrolling();
        }
    }

    closeQuickLinksModal:any = () => {
        if(this.state.quickLinksModalShowing){
            if(this.state.currentParty === "DEMOCRATS") {
                this.props.history.push('/democrats');
            }else {
                this.props.history.push('/republicans');
            }
            this.setState({quickLinksModalShowing: false, modalName: 'none'});
            this.enableScrolling();
        }
        this.setState({quickLinksModalShowing: false})
    }

    disableScrolling:any = () => {
        var x=window.scrollX;
        var y=window.scrollY;
        window.onscroll=function(){window.scrollTo(x, y);};
    }
    
    enableScrolling:any = () => {
        window.onscroll=function(){};
    }

    changeSortingOrder:any = (newSortingOrder:any) => {
        this.setState({sortOrder: newSortingOrder});
    }

    componentDidMount() {
        // var baseUrl = "localhost:5000";
        fetch(`${BASE_URL}/get_sorted_ordering/Democrats/positive_percent`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({democratPositiveList: result['order']});
                }
            )

        fetch(`${BASE_URL}/get_sorted_ordering/Democrats/neutral_percent`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({democratNeutralList: result['order']});
                }
            )

        fetch(`${BASE_URL}/get_sorted_ordering/Democrats/negative_percent`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({democratNegativeList: result['order']});
                }
            )

        fetch(`${BASE_URL}/get_sorted_ordering/Republicans/positive_percent`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({republicanPositiveList: result['order']});
                }
            )
    
        fetch(`${BASE_URL}/get_sorted_ordering/Republicans/neutral_percent`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({republicanNeutralList: result['order']});
                }
            ) 

        fetch(`${BASE_URL}/get_sorted_ordering/Republicans/negative_percent`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({republicanNegativeList: result['order']});
                }
            )
    }

    render(){
        const store = createStore(politicianReducer);
        store.dispatch({type: this.state.currentParty+' '+this.state.sortOrder, dim: 150});

        return(
            <div className={this.state.tweetModalShowing || this.state.quickLinksModalShowing ? "black-out":""}>
                <div className={this.state.quickLinksModalShowing ? "black-out":"dashboardPageButtonLocker"}>
                    <button className={this.state.tweetModalShowing || this.state.quickLinksModalShowing ? 'buttonDisabled' : "democratsButton"}
                        onClick={this.democratMode}>
                        Democrats
                    </button>
                    <button className={this.state.tweetModalShowing || this.state.quickLinksModalShowing? 'buttonDisabled' : "republicansButton"}
                        onClick={this.republicanMode}>
                        Republicans
                    </button>
                </div>

                {
                    this.state.tweetModalShowing ? <TweetsModal closeFunction={this.closeModal} name={this.state.modalName}/> : null 
                }

                {
                    this.state.quickLinksModalShowing ? <QuickLinksModal closeFunction={this.closeQuickLinksModal} name={this.state.modalName} /> : null
                }

                <div className={this.state.tweetModalShowing || this.state.quickLinksModalShowing ? "invisible" : this.state.currentParty==='DEMOCRATS' ? "defaultDashboardContainer" : "republicanDashboardContainer"}>
                        {this.state.sortOrder === "Default" && store.getState().map((value) => 
                            <ul key={""+value["id"]} className={this.state.tweetModalShowing? "hidden" : "defaultDashboardCardContainer"}>
                                <CustomCard cardText={value['name']}
                                imageSrc={value["imageSrc"]}
                                linkSrc={value["linkSrc"]}
                                extraInfo={value["linkSrcExtraInfo"]}
                                openModal={()=>this.openModal(value["name"])}
                                openQuickLinksModal={()=>this.openQuickLinksModal(value["name"])}
                                running={value["runningStatus"]}
                                dropOutDate={value["dropOutDate"]}

                                />
                            </ul>

                        )}

                        {this.state.currentParty === 'DEMOCRATS' && this.state.sortOrder === "Positive Sentiment" && this.state.democratPositiveList.map((value) => 
                            <ul key={""+value["id"]} className={this.state.tweetModalShowing? "hidden" : "defaultDashboardCardContainer"}>
                                <CustomCard cardText={value['name']}
                                imageSrc={value["imageSrc"]}
                                linkSrc={value["linkSrc"]}
                                extraInfo={value["linkSrcExtraInfo"]}
                                openModal={()=>this.openModal(value["name"])}
                                openQuickLinksModal={()=>this.openQuickLinksModal(value["name"])}
                                running={value["runningStatus"]}
                                dropOutDate={value["dropOutDate"]}
                                />
                            </ul>

                        )}

                        {this.state.currentParty === 'DEMOCRATS' && this.state.sortOrder === "Neutral Sentiment" && this.state.democratNeutralList.map((value) => 
                            <ul key={""+value["id"]} className={this.state.tweetModalShowing? "hidden" : "defaultDashboardCardContainer"}>
                                <CustomCard cardText={value['name']}
                                imageSrc={value["imageSrc"]}
                                linkSrc={value["linkSrc"]}
                                extraInfo={value["linkSrcExtraInfo"]}
                                openModal={()=>this.openModal(value["name"])}
                                openQuickLinksModal={()=>this.openQuickLinksModal(value["name"])}
                                running={value["runningStatus"]}
                                dropOutDate={value["dropOutDate"]}
                                />
                            </ul>

                        )}

                        {this.state.currentParty === 'DEMOCRATS' && this.state.sortOrder === "Negative Sentiment" && this.state.democratNegativeList.map((value) => 
                            <ul key={""+value["id"]} className={this.state.tweetModalShowing? "hidden" : "defaultDashboardCardContainer"}>
                                <CustomCard cardText={value['name']}
                                imageSrc={value["imageSrc"]}
                                linkSrc={value["linkSrc"]}
                                extraInfo={value["linkSrcExtraInfo"]}
                                openModal={()=>this.openModal(value["name"])}
                                openQuickLinksModal={()=>this.openQuickLinksModal(value["name"])}
                                running={value["runningStatus"]}
                                dropOutDate={value["dropOutDate"]}
                                />
                            </ul>

                        )}

                        {this.state.currentParty === 'REPUBLICANS' && this.state.sortOrder === "Positive Sentiment" && this.state.republicanPositiveList.map((value) => 
                            <ul key={""+value["id"]} className={this.state.tweetModalShowing? "hidden" : "defaultDashboardCardContainer"}>
                                <CustomCard cardText={value['name']}
                                imageSrc={value["imageSrc"]}
                                linkSrc={value["linkSrc"]}
                                extraInfo={value["linkSrcExtraInfo"]}
                                openModal={()=>this.openModal(value["name"])}
                                openQuickLinksModal={()=>this.openQuickLinksModal(value["name"])}
                                running={value["runningStatus"]}
                                dropOutDate={value["dropOutDate"]}
                                />
                            </ul>

                        )}

                        {this.state.currentParty === 'REPUBLICANS' && this.state.sortOrder === "Neutral Sentiment" && this.state.republicanNeutralList.map((value) => 
                            <ul key={""+value["id"]} className={this.state.tweetModalShowing? "hidden" : "defaultDashboardCardContainer"}>
                                <CustomCard cardText={value['name']}
                                imageSrc={value["imageSrc"]}
                                linkSrc={value["linkSrc"]}
                                extraInfo={value["linkSrcExtraInfo"]}
                                openModal={()=>this.openModal(value["name"])}
                                openQuickLinksModal={()=>this.openQuickLinksModal(value["name"])}
                                running={value["runningStatus"]}
                                dropOutDate={value["dropOutDate"]}
                                />
                            </ul>

                        )}

                        {this.state.currentParty === 'REPUBLICANS' && this.state.sortOrder === "Negative Sentiment" && this.state.republicanNegativeList.map((value) => 
                            <ul key={""+value["id"]} className={this.state.tweetModalShowing? "hidden" : "defaultDashboardCardContainer"}>
                                <CustomCard cardText={value['name']}
                                imageSrc={value["imageSrc"]}
                                linkSrc={value["linkSrc"]}
                                extraInfo={value["linkSrcExtraInfo"]}
                                openModal={()=>this.openModal(value["name"])}
                                openQuickLinksModal={()=>this.openQuickLinksModal(value["name"])}
                                running={value["runningStatus"]}
                                dropOutDate={value["dropOutDate"]}
                                />
                            </ul>

                        )}
                        
                </div>

                <div className={this.state.tweetModalShowing || this.state.quickLinksModalShowing ? "invisible":"dropdownLocker"}>
                    <Dropdown title={"Order by"} options={["Default", "Positive Sentiment", "Neutral Sentiment", "Negative Sentiment"]} defaultOption={"Default"} parentChangeFunction={this.changeSortingOrder}/>
                </div>
            </div>
        );
    }
}

export default withRouter(DefaultDashboardView);