import React from 'react';
import './TweetsModal.css';
import 'font-awesome/css/font-awesome.min.css';
import { LineChart } from 'react-chartkick';
import 'chartkick/chart.js';

import { BASE_URL } from '../../constants';

// react-router import
import { withRouter } from 'react-router-dom'

// Interface for the Props for the TweetsModal
interface TweetsModalProps {
    closeFunction: any;
    name: string;
    history: any;
}

// Interface for the State for the TweetsModal
interface TweetsModalState {
    modalMode: number;
    dateMode: number;
    positiveSampleTweets: any;
    negativeSampleTweets: any;
    error: any;
    sentimentsOverTimeData: any;
    currentStateHoveredOver: string;
    currentStateHoveredOverScore: number;
    /*stateDataLoaded: boolean;
    stateData: any;*/
}

class TweetsModal extends React.Component<TweetsModalProps, TweetsModalState> {
    constructor(props){
        super(props);
        this.state = {modalMode: 0, dateMode:3, positiveSampleTweets: ['Positive Sample Tweet #1'], negativeSampleTweets: ['Negative Sample Tweet #1'], error: null, sentimentsOverTimeData:[], currentStateHoveredOver:'none', currentStateHoveredOverScore: 0.0}; //stateData: "Before Pulled", stateDataLoaded: false};
        // Binding the switching between modes functions
        this.switchToModeZero = this.switchToModeZero.bind(this);
        this.switchToModeOne = this.switchToModeOne.bind(this);
        this.switchToModeTwo = this.switchToModeTwo.bind(this);

        // Binding the switching between the date range functions
        this.switchToOneDay = this.switchToOneDay.bind(this);
        this.switchToOneWeek = this.switchToOneWeek.bind(this);
        this.switchToOneMonth = this.switchToOneMonth.bind(this); 
        this.switchToMax = this.switchToMax.bind(this);

        // Binding the mouseOver and mouseOut functions
        this.stateHoveredOver = this.stateHoveredOver.bind(this);
        this.stateHoveredOutOf = this.stateHoveredOutOf.bind(this);

        // Functions for returning only a portion of the sentimentsOverTime series data
        this.getCutUpData = this.getCutUpData.bind(this);

        // Function for deciding whether to display individual time range buttons or not
        this.sentimentsOverTimeButtonClass = this.sentimentsOverTimeButtonClass.bind(this);

        // Functions for getting the response thumbs up thumbs down logo styles/sizes etc
        this.responsiveLogoSizes = this.responsiveLogoSizes.bind(this);
    }

    componentDidMount() {
        fetch(`${BASE_URL}/get_latest_tweets/`+this.props.name, {mode: 'cors', headers: {'Access-Control-Allow-Origin': '*'}})
        .then(res => res.json())
        .then(
            (result) => {
                //console.log(this.props.name);
                //console.log(result);
                this.setState({
                    positiveSampleTweets:result['positive_tweets_sample'],
                    negativeSampleTweets:result['negative_tweets_sample']
                });
            // Note: it's important to handle errors here
            // instead of a catch() block so that we don't swallow
            // exceptions from actual bugs in components.
            
            },
            (error) => {
                console.log(error);
                this.setState({
                    positiveSampleTweets: ["Error Occurred!"],
                    negativeSampleTweets: ["Error Occurred!"],
                    error
                });
            }
        )

        fetch(`${BASE_URL}/get_sentiment_snapshots/`+this.props.name, {mode:'cors', headers: {'Access-Control-Allow-Origin': '*'}})
        .then(res => res.json())
        .then(
            (result) => {
                this.setState({
                    sentimentsOverTimeData: result["sentiment_time_data"],
                    dateMode: 3,
                });
            },
            (error) => {
                console.log(error);
                this.setState({
                    sentimentsOverTimeData: [{
                            "name": "Positive Sentiment",
                            "data": {"2017-05-13": 20, "2017-05-14": 50} 
                        },
                        {
                            "name": "Neutral Sentiment",
                            "data": {"2017-05-13": 30, "2017-05-14": 20}
                        },
                        {
                            "name": "Negative Sentiment",
                            "data": {"2017-05-13": 50, "2017-05-14": 30} 
                        }
                    ],
                    error
                });
            } 
        )

        /*fetch("http://localhost:5000/get_all_state_sentiments/"+this.props.name, {mode:'cors', headers: {'Access-Control-Allow-Origin': '*'}})
        .then(res => res.json())
        .then(
            (result) => {
                this.setState({
                    stateDataLoaded: true,
                    stateData: result['state_scores']
                });
            },
            (error) => {
                console.log("Map data pulled in!");
                this.setState({
                    stateDataLoaded: false,
                    stateData: "Error Occurred!",
                    error
                })
            }
        )*/
    }

    // Functions for switching between individual modals
    switchToModeZero(){
        if (this.props.name === "Joe Biden" || this.props.name === "Marianne Williamson" || this.props.name === "Dean Phillips"){
            this.props.history.push('/democrats/'+this.props.name+'/tweets-modal/sample-tweets');
            this.setState({modalMode: 0}); 
        }else{
            this.props.history.push('/republicans/'+this.props.name+'/tweets-modal/sample-tweets');
            this.setState({modalMode: 0});
        }
    }

    switchToModeOne(){
        if (this.props.name === "Joe Biden" || this.props.name === "Marianne Williamson" || this.props.name === "Dean Phillips"){
            this.props.history.push('/democrats/'+this.props.name+'/tweets-modal/sentiments-over-time/one-week');
            this.setState({modalMode: 1}); 
        }else{
            this.props.history.push('/republicans/'+this.props.name+'/tweets-modal/sentiments-over-time/one-week');
            this.setState({modalMode: 1});
        }
    }

    switchToModeTwo(){
        if (this.props.name === "Joe Biden" || this.props.name === "Marianne Williamson" || this.props.name === "Dean Phillips"){
            this.props.history.push('/democrats/'+this.props.name+'/tweets-modal/sentiments-by-geography');
            this.setState({modalMode: 2}); 
        }else{
            this.props.history.push('/republicans/'+this.props.name+'/tweets-modal/sentiments-by-geography');
            this.setState({modalMode: 2});
        }
    }

    // Functions for switching between the date ranges
    switchToOneDay(){
        if (this.props.name === "Joe Biden" || this.props.name === "Marianne Williamson" || this.props.name === "Dean Phillips"){
            if(Object.keys(this.state.sentimentsOverTimeData[0]['data']).length >= 1){
                this.props.history.push('/democrats/'+this.props.name+'/tweets-modal/sentiments-over-time/one-day');
                this.setState({dateMode: 0}); 
            }
        }else{
            if(Object.keys(this.state.sentimentsOverTimeData[0]['data']).length >= 1){
                this.props.history.push('/republicans/'+this.props.name+'/tweets-modal/sentiments-over-time/one-day');
                this.setState({dateMode: 0});
            }
        }
    }

    switchToOneWeek(){
        if (this.props.name === "Joe Biden" || this.props.name === "Marianne Williamson" || this.props.name === "Dean Phillips"){
            if(Object.keys(this.state.sentimentsOverTimeData[0]['data']).length >= 7){
                this.props.history.push('/democrats/'+this.props.name+'/tweets-modal/sentiments-over-time/one-week');
                this.setState({dateMode: 1}); 
            }
        }else{
            if(Object.keys(this.state.sentimentsOverTimeData[0]['data']).length >= 7){
                this.props.history.push('/republicans/'+this.props.name+'/tweets-modal/sentiments-over-time/one-week');
                this.setState({dateMode: 1});
            }
        }
    }

    switchToOneMonth(){
        if (this.props.name === "Joe Biden" || this.props.name === "Marianne Williamson" || this.props.name === "Dean Phillips"){
            if(Object.keys(this.state.sentimentsOverTimeData[0]['data']).length >= 30){
                this.props.history.push('/democrats/'+this.props.name+'/tweets-modal/sentiments-over-time/one-month');
                this.setState({dateMode: 2}); 
            }
        }else{
            if(Object.keys(this.state.sentimentsOverTimeData[0]['data']).length >= 30){
                this.props.history.push('/republicans/'+this.props.name+'/tweets-modal/sentiments-over-time/one-month');
                this.setState({dateMode: 2});
            }
        }
    }

    switchToMax(){
        if (this.props.name === "Joe Biden" || this.props.name === "Marianne Williamson" || this.props.name === "Dean Phillips"){
            this.props.history.push('/democrats/'+this.props.name+'/tweets-modal/sentiments-over-time/max');
            this.setState({dateMode: 3}); 
        }else{
            this.props.history.push('/republicans/'+this.props.name+'/tweets-modal/sentiments-over-time/max');
            this.setState({dateMode: 3});
        }
    }

    // Helper methods for calculating only sentiments over 1 day, 1 week, and 1 month to display
    getCutUpData(allSentimentsOverTime, numDays){
        const currentAllSentimentsLength = Object.values(allSentimentsOverTime[0]['data']).length;
        const relevantDates = Object.keys(allSentimentsOverTime[0]['data']).slice(currentAllSentimentsLength-numDays);
        const relevantPositivePercents = Object.values(allSentimentsOverTime[0]['data']).slice(currentAllSentimentsLength-numDays);
        const relevantNeutralPercents = Object.values(allSentimentsOverTime[1]['data']).slice(currentAllSentimentsLength-numDays);
        const relevantNegativePercents = Object.values(allSentimentsOverTime[2]['data']).slice(currentAllSentimentsLength-numDays);

        const cutPositiveData = {};
        cutPositiveData['name'] = "Positive Sentiment";
        cutPositiveData['data'] = {};
        const cutNeutralData = {};
        cutNeutralData['name'] = "Neutral Sentiment";
        cutNeutralData['data'] = {};
        const cutNegativeData = {};
        cutNegativeData['name'] = "Negative Sentiment";
        cutNegativeData['data'] = {};
        for(var index = 0; index < relevantDates.length; index+=1){
            cutPositiveData['data'][relevantDates[index]] = relevantPositivePercents[index];
            cutNeutralData['data'][relevantDates[index]] = relevantNeutralPercents[index];
            cutNegativeData['data'][relevantDates[index]] = relevantNegativePercents[index];
        }

        const allCutData = [cutPositiveData, cutNeutralData, cutNegativeData];
        return allCutData;

    }

    stateHoveredOver(stateSymbol, stateScore){
        //console.log('in stateHoveredOver');
        const stateSymbolsToNames = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 
        'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachussetts', 'MD': 'Maryland', 'ME': 'Maine', 'MN': 'Minnesota', 'MO': 'Missouri',
        'MI': 'Michigan', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire',
        'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
        'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont',
        'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'};
        this.setState({currentStateHoveredOver: stateSymbolsToNames[stateSymbol], 
            currentStateHoveredOverScore: stateScore});
    }

    stateHoveredOutOf(){
        this.setState({currentStateHoveredOver: 'none'});
    }

    // This function will be called by the individual buttons in order to determine whether
    // they should be visible or not.
    sentimentsOverTimeButtonClass(numDaysOfData, requiredDateMode){
        console.log('this.state.dateMode = ' + this.state.dateMode);
        if(this.state.sentimentsOverTimeData.length === 0 || Object.keys(this.state.sentimentsOverTimeData[0]['data']).length < numDaysOfData){
            return "buttonNotShown";
        }else if(this.state.dateMode === requiredDateMode){
            return "timeActive";
        }return "timeOptionButton";
    }

    // methods for responsively assigning a complete to the thumbs up and
    // thumbs down logos

    responsiveLogoSizes(currentScreenWidth){
        if(currentScreenWidth >= 320 && currentScreenWidth < 768){
            return '60px';
        }/*else if(currentScreenWidth >= 375 && currentScreenWidth < 768){
            return '80px';
        }*/else if(currentScreenWidth >= 768 && currentScreenWidth < 1024){
            return '120px';
        }else if(currentScreenWidth === 1024){
            return '150px';
        }
        return '180px';
    }

    render(){
        /* default font size => 180px */
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const lineChartWidth = 0.8*windowWidth + "px";
        const lineChartHeight = 0.5*windowHeight+"px";
        //const windowHeight = window.innerHeight;
        return(
            <div className={"modalLocker"}>
                <div className={"tabButtonsLocker"}>
                    <button className={(this.state.modalMode === 0) ? "modeActive":"modalOptionButton"} onClick={this.switchToModeZero}>
                        Sample Tweets
                    </button>
                    <button className={(this.state.modalMode === 1) ? "modeActive":"modalOptionButton"} onClick={this.switchToModeOne}>
                        Sentiments Over Time
                    </button>
                </div>
                <div className={"close"} onClick={this.props.closeFunction}/>
                <div className={(this.state.modalMode === 0) ? "sampleTweets" : "lockerHidden"}>
                    <div className={"positiveTweetsMasterLocker"}>
                        {
                            windowWidth<= 1024 && windowHeight >= windowWidth &&
                            <div className={"fa fa-thumbs-up"} style={{fontSize: this.responsiveLogoSizes(windowWidth), position: 'absolute', bottom: '15%', left: '30%', color: '#6FBF90'}}/>
                        }

                        {
                            windowWidth <= 1024 && windowHeight < windowWidth &&
                            <div className={"fa fa-thumbs-up"} style={{fontSize: this.responsiveLogoSizes(windowHeight), position: 'absolute', bottom: '9%', left: '35%', color: '#6FBF90'}}/>
                        }

                        {
                            windowWidth > 1024 &&
                            <div className={"fa fa-thumbs-up"} style={{fontSize:this.responsiveLogoSizes(windowHeight), marginLeft: '5%', marginTop: 'auto', marginBottom: 'auto', marginRight: '1%', color: '#6FBF90'}}/>
                        }
                        
                        <div className={"positiveTweetsLocker"}>
                                {this.state.positiveSampleTweets.length >= 1 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[0]}</p></div>
                                }
                                {
                                  this.state.positiveSampleTweets.length >= 2 &&
                                    <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[1]}</p></div>
                                } 
                                {this.state.positiveSampleTweets.length >= 3 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[2]}</p></div>
                                }
                                {this.state.positiveSampleTweets.length >= 4 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[3]}</p></div>
                                }
                                {this.state.positiveSampleTweets.length >= 5 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[4]}</p></div>
                                }
                                {this.state.positiveSampleTweets.length >= 6 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[5]}</p></div>
                                }
                                {this.state.positiveSampleTweets.length >= 7 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[6]}</p></div>
                                }
                                {this.state.positiveSampleTweets.length >= 8 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[7]}</p></div>
                                }
                                {this.state.positiveSampleTweets.length >= 9 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[8]}</p></div>
                                }
                                {this.state.positiveSampleTweets.length >= 10 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[9]}</p></div>
                                }
                                {this.state.positiveSampleTweets.length >= 11 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[10]}</p></div>
                                }
                                {this.state.positiveSampleTweets.length >= 12 &&
                                   <div className={"tweetCard"}><p>{this.state.positiveSampleTweets[11]}</p></div>
                                } 
                        </div>
                    </div>

                    <div className={"negativeTweetsMasterLocker"}>
                        {
                            windowWidth <= 1366 && windowHeight >= windowWidth &&
                            <div className={"fa fa-thumbs-down"} style={{fontSize: this.responsiveLogoSizes(windowWidth), position: 'absolute', bottom: '15%', right: '30%', color: '#BF776F'}}/>
                        }

                        {
                            windowWidth <= 1024 && windowWidth > windowHeight &&
                            <div className={"fa fa-thumbs-down"} style={{fontSize: this.responsiveLogoSizes(windowHeight), position: 'absolute', bottom: '9%', right: '35%', color: '#BF776F'}}/> 
                        }

                        {
                            windowWidth > 1024 && 
                            <div className={"fa fa-thumbs-down"} style={{fontSize: this.responsiveLogoSizes(windowHeight), marginLeft: '5%', marginTop: 'auto',marginRight: '1%', marginBottom: 'auto', color: '#BF776F'}}/>
                        }
                        
                        <div className={"negativeTweetsLocker"}>
                                {this.state.negativeSampleTweets.length >= 1 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[0]}</p></div>
                                }
                                {
                                  this.state.negativeSampleTweets.length >= 2 &&
                                    <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[1]}</p></div>
                                } 
                                {this.state.negativeSampleTweets.length >= 3 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[2]}</p></div>
                                }
                                {this.state.negativeSampleTweets.length >= 4 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[3]}</p></div>
                                }
                                {this.state.negativeSampleTweets.length >= 5 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[4]}</p></div>
                                }
                                {this.state.negativeSampleTweets.length >= 6 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[5]}</p></div>
                                }
                                {this.state.negativeSampleTweets.length >= 7 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[6]}</p></div>
                                }
                                {this.state.negativeSampleTweets.length >= 8 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[7]}</p></div>
                                }
                                {this.state.negativeSampleTweets.length >= 9 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[8]}</p></div>
                                }
                                {this.state.negativeSampleTweets.length >= 10 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[9]}</p></div>
                                }
                                {this.state.negativeSampleTweets.length >= 11 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[10]}</p></div>
                                }
                                {this.state.negativeSampleTweets.length >= 12 &&
                                   <div className={"tweetCard"}><p>{this.state.negativeSampleTweets[11]}</p></div>
                                }
                            </div>
                        </div>
                    </div>
                <div className={(this.state.modalMode === 1) ?  "sentimentsOverTime" : "lockerHidden"} >
                    <div className={"graphLocker"}>
                        <h1> Sentiments Over Time for {this.props.name} </h1>
                        {   /* Case for showing just the most recent day of sentiment data */
                            this.state.dateMode === 0 &&
                            <LineChart width={lineChartWidth} height={lineChartHeight} data={this.getCutUpData(this.state.sentimentsOverTimeData,1)} xtitle="Time" ytitle="Percentage" messages={{empty: "No data"}} colors={['#6FBF90', '#6FB7BF', '#BF776F']} />
                        }

                        {
                            /* Case for showing the most recent week of sentiment data */
                            this.state.dateMode === 1 &&
                            <LineChart width={lineChartWidth} height={lineChartHeight} data={this.getCutUpData(this.state.sentimentsOverTimeData,7)} xtitle="Time" ytitle="Percentage" messages={{empty: "No data"}} colors={['#6FBF90', '#6FB7BF', '#BF776F']} />
                        }

                        {
                            /* Case for showing the most recent month (30 days for now) of sentiment data */
                            this.state.dateMode === 2 &&
                            <LineChart width={lineChartWidth} height={lineChartHeight} data={this.getCutUpData(this.state.sentimentsOverTimeData,30)} xtitle="Time" ytitle="Percentage" messages={{empty: "No data"}} colors={['#6FBF90', '#6FB7BF', '#BF776F']} />
                        }

                        {
                            /* Case for showing the maximum possible amount of sentiment data over time */
                            this.state.dateMode === 3 &&
                            <LineChart width={lineChartWidth} height={lineChartHeight} data={this.state.sentimentsOverTimeData} xtitle="Time" ytitle="Percentage" messages={{empty: "No data"}} colors={['#6FBF90', '#6FB7BF', '#BF776F']} />
                        }
                        
                        <button className={this.sentimentsOverTimeButtonClass(1, 0)} onClick={this.switchToOneDay}>
                            1 Day
                        </button>
                        <button className={this.sentimentsOverTimeButtonClass(7, 1)} onClick={this.switchToOneWeek}>
                            1 Week
                        </button>
                        <button className={this.sentimentsOverTimeButtonClass(30, 2)} onClick={this.switchToOneMonth}>
                            1 Month
                        </button>
                        <button className={this.sentimentsOverTimeButtonClass(0, 3)} onClick={this.switchToMax}>
                            Max
                        </button>
                    </div>
                </div>
            </div>

        )
    }
}

export default withRouter(TweetsModal);