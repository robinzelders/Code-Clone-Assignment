function calculateFactorial(input){

    if (input <= 2) {
        return input;
    }

    let factorial = input;
    let offset = 1;

    while(offset < input){
        factorial = factorial * (input - offset);
    }

    return factorial;
}