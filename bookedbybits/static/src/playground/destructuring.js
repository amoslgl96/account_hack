

//NEW ES6 FEATURE object DESTRUCTURING : TO BETTER MANAGE calling OBJECTS properties -> using { } curly braces

console.log('test');


const book = {
    title: 'Ego is the Enemy',
    author: 'Ryan Holiday',
    publisher: {
        name:'Penguin'
    }
}


const {name: publisherName = 'Self-Published'} = book.publisher; 


console.log(publisherName);


//function argument obj destructuring
//const add=(data)=>
// {
//     return data.a+data.b;
// }


// console.log(add({a:2,b:3}));


//after obj destructuring:

const add=({a,b})=>
{
    return a+b;
}

console.log(add({a:2,b:3}));




//another exmapel: 

const removeExpense=(
    {      
    //obj arg destructed
       id
    }={}
)=>({
    type: 'REMOVE_EXPENSE',
    id
})

//this is the REDUX REDUCER 

//NOTICE ({id}={})  {} is needed to highlight we are waiting for an obj, if no obj, means by default = {} empty obj and id will hence be empty
//ARRAY destructuring  -> using [ ] brackets


const address=['a','b','c','d'];

const [ ,city,state]=address;

console.log(`you are in ${city} ${state}`);



const item=['coffee (hot)','$2.00','$2.50','$2.75'];

const [itemName, ,mediumPrice]= item;

console.log(`A medium ${itemName} costs ${mediumPrice}`);

