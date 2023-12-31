const politicianReducer = (state, action) => {
    switch(action.type) {
        case 'DEMOCRATS Default':
            return [
                {
                    "id": 1,
                    "initials": "JB",
                    "name": "Joe Biden",
                    "imageSrc": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Joe_Biden_%2848548455397%29_%28rotated%29.jpg",
                    "imageHeight": action.dim,
                    "imageWidth": action.dim,
                    "linkSrc": "https://commons.wikimedia.org/wiki/File:Joe_Biden_(48548455397)_(rotated).jpg",
                    "linkSrcExtraInfo": "Gage Skidmore from Peoria, AZ, USA",
                    "runningStatus": true,
                    "dropOutDate": ""
                },
                {
                    "id": 2,
                    "initials": "MW",
                    "name": "Marianne Williamson",
                    "imageSrc": "https://upload.wikimedia.org/wikipedia/commons/8/83/Marianne_Williamson_Profile.jpg",
                    "imageHeight": action.dim,
                    "imageWidth": action.dim,
                    "linkSrc": "https://commons.wikimedia.org/wiki/File:Marianne_Williamson_Profile.jpg",
                    "linkSrcExtraInfo": "Supearnesh [CC BY-SA 4.0]",
                    "runningStatus": true,
                    "dropOutDate": ""
                },
                {
                    "id": 3,
                    "initials": "DP",
                    "name": "Dean Phillips",
                    "imageSrc": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Dean_Phillips%2C_official_portrait%2C_116th_Congress.jpg",
                    "imageHeight": action.dim,
                    "imageWidth": action.dim,
                    "linkSrc": "https://commons.wikimedia.org/wiki/File:Dean_Phillips,_official_portrait,_116th_Congress.jpg",
                    "linkSrcExtraInfo": "Eric Connolly - phillips.house.gov",
                    "runningStatus": true,
                    "dropOutDate": ""
                }
            ];
        case 'REPUBLICANS Default':
            return [
                {
                    "id": 4,
                    "initials": "DT",
                    "name": "Donald Trump",
                    "imageSrc": "https://upload.wikimedia.org/wikipedia/commons/5/53/Donald_Trump_official_portrait_%28cropped%29.jpg",
                    "imageHeight": action.dim,
                    "imageWidth": action.dim,
                    "linkSrc": "https://commons.wikimedia.org/wiki/File:Donald_Trump_official_portrait_(cropped).jpg",
                    "linkSrcExtraInfo": "Shealah Craighead [Public domain]",
                    "runningStatus": true,
                    "dropOutDate": ""
                },
                {
                    "id": 5,
                    "initials": "NH",
                    "name": "Nikki Haley",
                    "imageSrc": "https://upload.wikimedia.org/wikipedia/commons/5/53/Nikki_Haley_2023_%28cropped%29.jpg",
                    "imageHeight": action.dim,
                    "imageWidth": action.dim,
                    "linkSrc": "https://commons.wikimedia.org/wiki/File:Nikki_Haley_2023_(cropped).jpg",
                    "linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
                    "runningStatus": true,
                    "dropOutDate": ""
                },
                {
                    "id": 6,
                    "initials": "VR",
                    "name": "Vivek Ramaswamy",
                    "imageSrc": "https://upload.wikimedia.org/wikipedia/commons/9/96/Vivek_Ramaswamy_by_Gage_Skidmore.jpg",
                    "imageHeight": action.dim,
                    "imageWidth": action.dim,
                    "linkSrc": "https://commons.wikimedia.org/wiki/File:Vivek_Ramaswamy_by_Gage_Skidmore.jpg",
                    "linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
                    "runningStatus": true,
                    "dropOutDate": ""
                },
                {
                    "id": 7,
                    "initials": "AH",
                    "name": "Asa Hutchinson",
                    "imageSrc": "https://upload.wikimedia.org/wikipedia/commons/6/69/Asa_Hutchinson_by_Gage_Skidmore.jpg",
                    "imageHeight": action.dim,
                    "imageWidth": action.dim,
                    "linkSrc": "https://commons.wikimedia.org/wiki/File:Asa_Hutchinson_by_Gage_Skidmore.jpg",
                    "linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
                    "runningStatus": true,
                    "dropOutDate": ""
                },
                {
                    "id": 8,
                    "initials": "RD",
                    "name": "Ron DeSantis",
                    "imageSrc": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Ron_DeSantis_in_October_2023.jpg",
                    "imageHeight": action.dim,
                    "imageWidth": action.dim,
                    "linkSrc": "https://commons.wikimedia.org/wiki/File:Ron_DeSantis_in_October_2023.jpg",
                    "linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
                    "runningStatus": true,
                    "dropOutDate": ""
                },
                {
                    "id": 9,
                    "initials": "CC",
                    "name": "Chris Christie",
                    "imageSrc": "https://upload.wikimedia.org/wikipedia/commons/7/72/Chris_Christie_%2853297980082%29_%28cropped%29.jpg",
                    "imageHeight": action.dim,
                    "imageWidth": action.dim,
                    "linkSrc": "https://commons.wikimedia.org/wiki/File:Chris_Christie_(53297980082)_(cropped).jpg",
                    "linkSrcExtraInfo": "Gage Skidmore from Surprise, AZ, United States of America",
                    "runningStatus": true,
                    "dropOutDate": ""
                }
            ];
        default:
            return [];
    }
}

export default politicianReducer;