
import { createStore } from 'redux';



//create the store to hold onto state 
//state arg is set with a default obj
//returns state 
// const store=createStore((state={count:0},action)=>
// {
//     switch(action.type)
//     {
//         case 'INCREMENT':
//             const incrementBy=typeof action.incrementBy==='number'?action.incrementBy:1;
//             return {count: state.count + incrementBy}
        
//         case 'DECREMENT':
//             const decrementBy=typeof action.decrementBy==='number'?action.decrementBy:1;
//             return {count: state.count - decrementBy}

//         case 'RESET':
//             return {count: 0}

//         default:
//             return state;
//     }
// });




//retrieve from store , state obj
//console.log(store.getState());


//Actions - objects that get send to the store ( increment , decrement , reset )
//I'd like to increment the count / reset the count to zero 



//CAPS - convention for redux
//eg of defining an increment action:
//store.dispatch({type: 'INCREMENT' });
//dispatch arg takes in an obj, then it sends this obj to createStore as second argument 


// console.log(store.getState());



// store.dispatch({type:'DECREMENT'});
// store.dispatch({type:'DECREMENT'});

// console.log(store.getState());


// store.dispatch({type:'RESET'});
// console.log(store.getState());


/*********************************How to set up redux container to detect changes aka listener  */


//usiong .subscribe()
// const unsubscribe=store.subscribe(()=>{
//     console.log(store.getState());
// });
// //whenever store gets updated, .subscribe is triggered , it returns anotehr function that allows you
// //to unsubscribe.

// store.dispatch({type: 'INCREMENT' });
// store.dispatch({type: 'DECREMENT' });

// unsubscribe();

// store.dispatch({type: 'INCREMENT' });
// store.dispatch({type: 'INCREMENT' });




/**************************************************add Additional stuff onto Action' arg obj */

/*
dispatch, other than the mandatory type property, you can add any number of other properties to pass
to the state container */

// store.dispatch({
//     type: "INCREMENT",
//     incrementBy: 5
// })

// console.log(store.getState());

// store.dispatch({
//     type: "DECREMENT",
//     decrementBy: 5
// })

// console.log(store.getState());



/**************************************************ACTION GENERATOR -> FUNCTION that generates action object*/

// const add=(data)=>
// {
//     return data.a+data.b;
// }


// console.log(add({a:2,b:3}));


//after obj destructuring:

// const add=({a,b},c)=>
// {
//     return a+b+c;
// }

// console.log(add({a:2,b:3},100));



//action generator without applying obj destructuring 
// const incrementCount = (payload={})=>(
//     {
//        type: 'INCREMENT',
//        incrementBy: typeof payload.incrementBy==='number'?payload.incrementBy:1
//     }
// )




//REDUCER: (decides what to do based on the action)

// const store=createStore((state={count:0},action)=>
// {
//     switch(action.type)
//     {
//         case 'INCREMENT':
//             return {count: state.count + action.incrementBy}
        
//         case 'DECREMENT':
//             return {count: state.count - action.decrementBy}

//         case 'RESET':
//             return {count: 0}

//         default:
//             return state;
//     }
// });

// //action generator with obj destructuring 

// const incrementCount=({incrementBy=1}={})=>
// (
//     {
//         //implicit return because one-liner object
//         type: 'INCREMENT',
//         incrementBy:incrementBy
//     }
// )

// const decrementCount=({decrementBy=1}={})=>
// (
//     {
//         //implicit return 
//         type: 'DECREMENT',
//         decrementBy: decrementBy
//     }
// )


// store.dispatch(incrementCount({
//     incrementBy: 5
// }))

// console.log(store.getState());


// store.dispatch(decrementCount(
//     {
//         //send in extra action information to process
//         decrementBy:5
//     }
// ))

// console.log(store.getState());


// store.dispatch(decrementCount());
// console.log(store.getState());


/*****************************************WHAT IS A REDUCER-> DECIDES WHAT TO DO WITH YOUR ACTION
 * LIKE CHANGE STATES.
 * IN AN APPLICATION, WE WILL DEFINE MULTIPLE REDUCERS LIKE IN OUR EXPENSIFY APP 
 * 
 * RULES:
 * 
 * 1) REDUCERS has to be PURE FUNCTIONS -> only uses values passed into it as argument 
 * 
 * UNPURE function -> meaning a global variable being used in a function block scope.
 * 
 * 2)Never change state or action -> do not mutate it. Remember the prevState rationale!
 */



//Reducer function:
const countReducer=(state={count:0},action)=>
{
    switch(action.type)
    {
        case 'INCREMENT':
            return {count: state.count + action.incrementBy}
        
        case 'DECREMENT':
            return {count: state.count - action.decrementBy}

        case 'RESET':
            return {count: 0}

        default:
            return state;
    }
}


const store=createStore(countReducer);