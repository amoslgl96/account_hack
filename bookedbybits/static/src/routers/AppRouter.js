import React from 'react';
//named exports from react-router 
import {BrowserRouter, Route, Switch} from 'react-router-dom';

import Header from '../components/Header';
import ExpenseDashboardPage from '../components/ExpenseDashboardPage';
import AddExpensePage from '../components/AddExpensePage';
import EditExpensePage from '../components/EditExpensePage';
import HelpPage from '../components/HelpPage';
import NotFoundPage from '../components/NotFoundPage';

//BrowserRouter -> used for creating the router once, Route is used on every single page 

//exact means, only when it is exactly that url, then serve up the component 

const AppRouter=()=>(
    <BrowserRouter> 
        <div>
            <Header/>
            <Switch> 
                <Route path='/' component={ExpenseDashboardPage} exact={true}/>
                <Route path='/create' component={AddExpensePage}/>
                <Route path='/edit/:id' component={EditExpensePage}/>
                <Route path='/help' component={HelpPage}/>
                <Route component={NotFoundPage}/>
            </Switch> 
        </div>
    </BrowserRouter>

    //switch logic is like the switch(var) { case'1': }, once a match 
    //happens , it stops looking to other routes. Matching starts in order from top to bottom
)

export default AppRouter;