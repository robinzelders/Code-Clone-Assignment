function calculateFactorial(input){

    if (input <= 2) {
        return input;
    }

    let result = input;

    for (let offset = 1; offset < input; offset++){
        result = result * (input - offset);
    }

    return result;
}