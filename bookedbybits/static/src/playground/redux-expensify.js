
import {createStore, combineReducers} from 'redux';
import uuid from 'uuid';
//combineReducers allow us to create multiple functions/reducers that can be used to decide what to do with our ACTION


const expensesReducerDefaultState=[];


//define reducer for expenses: where store.dispatch(Action function) would pass action value into
const expensesReducer=(state=expensesReducerDefaultState,action)=>
{
    //what to do with action triggered? 
    switch(action.type)
    {
        case 'ADD_EXPENSE':
            //to avoid changing the original state, we cannot do state.push but .concat instead
            //the .concat can also be replaced by a new ES6 feature : spread operator
            //return state.concat(action.expense);
            return [...state,action.expense]
        case 'REMOVE_EXPENSE':
            const id=action.id;
            return state.filter((expense)=>{
                return expense.id!==id;
            })
        case 'EDIT_EXPENSE':
            return state.map((expense)=>{
                if(expense.id===action.id)
                {
                    return {
                        ...expense,
                        ...action.updates
                    }
                }
                else
                {
                    return expense;
                }
            })
            
        default:
            return state;
    }
};




const filtersReducerDefaultState={
    text: '',
    sortBy:'date',
    startDate: undefined,
    endDate: undefined
};
//define reducer for filters: where store.dispatch(Action) would pass value into
const filtersReducer=(state=filtersReducerDefaultState,action)=>
{
    //filtersReducer returns
    //when you are editing an obj, you can't jsut specify
    //one property to change in return statement, it would 
    //cause the entire filters state to only adopt one property
    switch(action.type)
    {
        case 'SET_TEXT_FILTER':
        return {
            ...state,
            text:action.text
        }

        case 'SET_SORT_AMOUNT':
        return {
            ...state,
            sortBy:'Amount'
        }

        case 'SET_SORT_DATE':
        return {
            ...state,
            sortBy:'Date'
        }

        case 'SET_START_DATE':
        return {
            ...state,
            startDate:action.date
        }

        case 'SET_END_DATE':
        return {
            ...state,
            endDate:action.date
        }
       
        default:
            return state;
    }
}



//Defining a function to retrieve visible expenses according
//to certain criteria:







//the expenses, filters key values represent the reducers
const store=createStore(combineReducers({
    expenses:expensesReducer,
    filters:filtersReducer
}))


console.log(store.getState());

//data to track to create expensify app:
const demoState={
    expenses: [{
        id: 'abcdfcs',
        description: 'January Rent',
        note:'This was the final payment for that address',
        amount: 54500,
        createdAt: 0
    }],
    filters: {
        text: 'rent',
        sortBy:'amount',
        startDate:undefined,
        endDate:undefined
    }
};
//expenses property is managed by expensesReducer
//filters property is managed by filtersReducer


//looking at the state above, if we only use one single reducer
//to manage, there would be a lot of burden 

//expenses: 1 reducer , filters: 1 reducer, then combine the 2 to make 1 single store 



/* 
NEXT UP SETTING UP ACTIONS FOR THE REDUCERS 
TO HANDLE 
*/


/* 

List of action generators:

Add_expense (done)
Remove_expense (done)
edit_expense (done)
set_text_filter (done)
sort_by_date (done)
sort_by_amount (done)
set_start_date
set_end_date  


*/


//ADD_EXPENSE
/* for expenses ID, we would generate that our own
using UUID npm -> yarn add uuid@3.1.0. 

When we have database, we can generate that thru it but for now
usin uuid*/
const addExpense=(
    {
        //obj arg destructed
        description= '',
        note='',
        amount=0,
        createdAt=0

    }={}
)=>({
    type: 'ADD_EXPENSE',
    expense: {
        id: uuid(),
        description:description,
        note:note,
        amount,
        createdAt
    }
})




store.subscribe(()=>
{
    console.log(store.getState());
})

//now to send in the AddExpenseaction into both Expenses and filters reducer
// const expenseOne=store.dispatch(addExpense({
//     description:'Rent',
//     amount:100
// }));


// const expenseTwo=store.dispatch(addExpense({
//     description:'Coffee',
//     amount:300
// }));


//console.log(expenseOne);
//second task to create removeExpense action
//retrieve the uuid 


const removeExpense=(
    {      
    //obj arg destructed
       id
    }={}
)=>({
    type: 'REMOVE_EXPENSE',
    id
})

// store.dispatch(removeExpense({
//     id: expenseOne.expense.id
// }));



//action generator for edit expense 
 
const editExpense=(id,updates)=>({
    type: 'EDIT_EXPENSE',
    id,
    updates
})

//reason why we do {amount:600} instead of just 600, is because
//we want to use spread operator in the reducer, and thsi makes it easy to edit the state expense obj
// store.dispatch(editExpense(expenseTwo.expense.id,{amount:600}));



//action generator for set_text_filter 


const setTextFilter=(text='')=>({
    type: 'SET_TEXT_FILTER',
    text
})



// store.dispatch(setTextFilter('date'));

// store.dispatch(setTextFilter('expense'));



//action generators for sort_amount and date 

const sortByAmount=()=>({
    type: 'SET_SORT_AMOUNT'
})


const sortByDate=()=>({
    type: 'SET_SORT_DATE'
})



// store.dispatch(sortByAmount());
// store.dispatch(sortByDate());




//set_start_date
//set_end_date  

//start and end date -> number 


//actipm generator for the dates 

const setStartDate=(date=undefined)=>({
    type: 'SET_START_DATE',
    date 
})

const setEndDate=(date=undefined)=>({
    type: 'SET_END_DATE',
    date 
})


store.dispatch(setStartDate(125));
store.dispatch(setStartDate());

store.dispatch(setEndDate(1250));
store.dispatch(setEndDate());



