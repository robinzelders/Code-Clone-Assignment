function calculateFactorial(input){
    // We can skip a few steps if the input is <= 2
    if (input <= 2) {
        return input;
    }

    let result = input;
    let offset = 1;

    while(offset < input){
        result = result * (input - offset);
    }

    return result;
}