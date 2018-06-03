import React from 'react';
import {Link, NavLink} from 'react-router-dom';
//NavLink allows us to do styling for it when the link was pressed
//activeClassName, when the link is 'active' , styling is applied 

const Header=()=>(
    <div> 
        <h1>Expensify</h1>
        <NavLink activeClassName='is-active' to='/' exact={true}>Dashboard<br/></NavLink>
        <NavLink activeClassName='is-active' to='/create'>Create Expense<br/></NavLink>
        <NavLink activeClassName='is-active' to='/help'>Help<br/></NavLink>
    </div>
)


export default Header;