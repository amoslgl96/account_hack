
//spread operater on array - find out after hackathon..

/********************Spread operator on object */

//ALLOWS US TO CREATE NEW OBJECTS OUT OF EXISTING ONES 
 
const user={
    name: 'Jan',
    age: 24
};


console.log({
    ...user
}
)

//the spread operator spreads out the inner components of user
//this is good as it does not change user obj , but clones them and cr8 another obj out of it

console.log({
    ...user,
    location:'sINGAPORE',
    age:22
}
)