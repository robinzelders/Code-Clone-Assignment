function calculateFactorial(input){
    let result = input;
    if (input > 2) {
        let offset = 1;

        while (offset < input) {
            result = result * (input - offset);
        }

    }

    return result;
}